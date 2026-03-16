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
                print(f"  Rate limited (429), retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise


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
                print(f"  Rate limited (429), retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise


def main():
    os.makedirs(IMGS_DIR, exist_ok=True)

    success = 0
    failed = []

    for title in PARKS:
        slug = title_to_filename(title)
        print(f"Fetching image for: {title} ...")

        # Check if any image with this slug already exists (any extension)
        existing = glob.glob(os.path.join(IMGS_DIR, slug + ".*"))
        if existing:
            print(f"  Already exists: {existing[0]}")
            success += 1
            continue

        try:
            url = get_page_image_url(title)
        except Exception as e:
            print(f"  ERROR fetching metadata: {e}")
            failed.append((title, str(e)))
            time.sleep(BASE_DELAY)
            continue

        if not url:
            print("  No image found on Wikipedia")
            failed.append((title, "no image found"))
            time.sleep(BASE_DELAY)
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
            print(f"  Saved to {dest}")
            success += 1
        except Exception as e:
            print(f"  ERROR downloading: {e}")
            failed.append((title, str(e)))

        # Delay between requests to avoid rate limiting
        time.sleep(BASE_DELAY)

    print(f"\nDone! {success} images downloaded, {len(failed)} failed.")
    if failed:
        print("\nFailed parks:")
        for name, reason in failed:
            print(f"  - {name}: {reason}")


if __name__ == "__main__":
    main()
