"""
Fetch park images from Wikipedia and download them to the imgs/ folder.

Usage:
    python scripts/fetch_park_images.py
"""

import glob
import os
import re
import time
import urllib.error
import urllib.request
import urllib.parse
import json

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table

console = Console()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
IMGS_DIR = os.path.join(PROJECT_ROOT, "imgs")

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "SFParksImageFetcher/1.0 (educational project)"

PARKS = [
    "Golden Gate Park",
    "Dolores Park",
    "Crissy Field",
    "Buena Vista Park",
    "Alamo Square",
    "Lands End (San Francisco)",
    "Twin Peaks (San Francisco)",
    "Bernal Heights Park",
    "Lafayette Park (San Francisco)",
    "Presidio of San Francisco",
    "McLaren Park",
    "Glen Canyon Park",
    "Ocean Beach (San Francisco)",
    "Baker Beach",
    "Corona Heights Park",
    "Stern Grove",
    "Washington Square (San Francisco)",
    "Alta Plaza Park",
    "Huntington Park (San Francisco)",
    "South Park (San Francisco)",
    "Precita Park",
    "Mountain Lake (San Francisco)",
    "Balboa Park (San Francisco)",
    "Crocker-Amazon Playground",
    "Holly Park (San Francisco)",
    "India Basin",
    "Heron's Head Park",
    "Candlestick Point State Recreation Area",
    "Ina Coolbrith Park",
    "Fort Funston",
    "Yerba Buena Gardens",
    "Civic Center, San Francisco",
    "Sue Bierman Park",
    "Justin Herman Plaza",
    "Rincon Park",
    "Potrero Hill",
    "McKinley Square (San Francisco)",
    "Grattan Playground",
    "Noe Valley",
    "Walter Haas Playground",
    "Miraloma Park, San Francisco",
    "Mount Davidson (San Francisco)",
    "John McLaren Park",
    "Garfield Square",
    "Cayuga Park",
    "Visitacion Valley, San Francisco",
    "Randall Museum",
    "Tank Hill",
    "Esprit Park",
]

# Map Wikipedia search titles to simpler filenames
def title_to_filename(title):
    """Convert a park title to a safe filename slug."""
    name = title.split("(")[0].strip()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s]+", "_", name).strip("_").lower()
    return name


MAX_RETRIES = 3
BASE_DELAY = 3  # seconds between requests


def api_request(params):
    """Make a request to the Wikipedia API and return JSON, with retry on 429."""
    params["format"] = "json"
    url = WIKIPEDIA_API + "?" + urllib.parse.urlencode(params)
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < MAX_RETRIES - 1:
                wait = BASE_DELAY * (2 ** (attempt + 1))
                console.print(f"  [yellow]Rate limited (429), retrying in {wait}s...[/yellow]")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Exhausted retries without response")


def get_page_image_url(title):
    """Get the main image (pageimage / thumbnail) URL for a Wikipedia article."""
    # Try the pageimages API first (gets the main infobox image)
    data = api_request({
        "action": "query",
        "titles": title,
        "prop": "pageimages",
        "pithumbsize": 800,
        "pilicense": "any",
        "redirects": "1",
    })
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        thumb = page.get("thumbnail", {})
        if thumb.get("source"):
            return thumb["source"]

    # Fallback: grab the first image from the page
    data = api_request({
        "action": "query",
        "titles": title,
        "prop": "images",
        "imlimit": "10",
        "redirects": "1",
    })
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        for img in page.get("images", []):
            img_title = img.get("title", "")
            # Skip icons / logos / svg / commons
            if any(ext in img_title.lower() for ext in [".svg", "icon", "logo", "flag", "commons-logo"]):
                continue
            if any(ext in img_title.lower() for ext in [".jpg", ".jpeg", ".png"]):
                return get_file_url(img_title)
    return None


def get_file_url(file_title):
    """Given a File:xxx title, return the actual image URL."""
    data = api_request({
        "action": "query",
        "titles": file_title,
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": "800",
    })
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        info = page.get("imageinfo", [{}])[0]
        return info.get("thumburl") or info.get("url")
    return None


def download_image(url, dest_path):
    """Download an image from a URL to a local path, with retry on 429."""
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as resp:
                with open(dest_path, "wb") as f:
                    f.write(resp.read())
            return
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < MAX_RETRIES - 1:
                wait = BASE_DELAY * (2 ** (attempt + 1))
                console.print(f"  [yellow]Rate limited (429), retrying in {wait}s...[/yellow]")
                time.sleep(wait)
            else:
                raise


def main():
    os.makedirs(IMGS_DIR, exist_ok=True)

    success = 0
    failed = []

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("({task.completed}/{task.total})"),
        TimeElapsedColumn(),
        console=console,
    )

    with progress:
        task = progress.add_task("Fetching parks...", total=len(PARKS))

        for title in PARKS:
            slug = title_to_filename(title)
            progress.update(task, description=f"Fetching: {title}")

            # Check if any image with this slug already exists (any extension)
            existing = glob.glob(os.path.join(IMGS_DIR, slug + ".*"))
            if existing:
                console.print(f"  [dim yellow]Already exists:[/dim yellow] {existing[0]}")
                success += 1
                progress.advance(task)
                continue

            try:
                url = get_page_image_url(title)
            except (urllib.error.URLError, OSError, json.JSONDecodeError, RuntimeError) as e:
                console.print(f"  [red]ERROR fetching metadata:[/red] {e}")
                failed.append((title, str(e)))
                time.sleep(BASE_DELAY)
                progress.advance(task)
                continue

            if not url:
                console.print(f"  [yellow]No image found on Wikipedia[/yellow] for {title}")
                failed.append((title, "no image found"))
                time.sleep(BASE_DELAY)
                progress.advance(task)
                continue

            # Determine file extension from URL
            parsed = urllib.parse.urlparse(url)
            path_lower = parsed.path.lower()
            if ".png" in path_lower:
                ext = ".png"
            elif ".jpeg" in path_lower:
                ext = ".jpeg"
            else:
                ext = ".jpg"

            dest = os.path.join(IMGS_DIR, slug + ext)

            try:
                download_image(url, dest)
                console.print(f"  [green]Saved[/green] {title} -> {dest}")
                success += 1
            except (urllib.error.URLError, OSError) as e:
                console.print(f"  [red]ERROR downloading:[/red] {e}")
                failed.append((title, str(e)))

            # Delay between requests to avoid rate limiting
            time.sleep(BASE_DELAY)
            progress.advance(task)

    console.rule("[bold]Summary")
    console.print(
        f"[green]{success} images downloaded[/green], "
        f"[red]{len(failed)} failed[/red]."
    )

    if failed:
        table = Table(title="Failed Parks", show_lines=False)
        table.add_column("Park", style="cyan", no_wrap=True)
        table.add_column("Reason", style="red")
        for name, reason in failed:
            table.add_row(name, reason)
        console.print(table)


if __name__ == "__main__":
    main()
