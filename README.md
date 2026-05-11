# SF Parks Explorer

A Django web app for discovering and filtering San Francisco's parks.

## Repo Layout: Two Projects, Two Environments

This workspace is a Django app (`sf-parks`) with a nested utility project, each with its own Python environment:

| Project | Location | Virtual env | Purpose | Dependencies |
| --- | --- | --- | --- | --- |
| **Root project** | workspace root | root-level `.venv` | The Django site itself — `parks/`, `sf_parks/`, `templates/`, `manage.py`, and the SQLite DB. | App runtime deps (Django, etc.) |
| **`scripts/` sub-project** | `scripts/` | `scripts/`-level venv | One-off tooling (e.g. [`fetch_park_images.py`](scripts/fetch_park_images.py)). | Script-only deps (HTTP clients, image libs, etc.) — intentionally *not* part of the Django app's dependency graph. |

**Why two environments?** Keeping them separate keeps the web app's runtime deps lean and prevents ad-hoc scripting tools from polluting it (and vice versa).

**How it stays ergonomic in one window.** The **Python Environments extension** makes this seamless:

- It detects both environments automatically.
- It binds the right interpreter to each folder/file.
- It clearly shows which env is active for whichever file we're editing.

So running `manage.py` uses the root venv, and running `scripts/fetch_park_images.py` uses the scripts venv — automatically.

## Features

- Browse 50 San Francisco parks with photos, descriptions, and category tags
- Filter parks by category (Good View, Dog Play Area, Bathrooms, Tennis Courts, etc.)
- Interactive Leaflet map on each park's detail page
- Admin interface for managing parks and categories

## Requirements

- Python 3.10+

## Setup

```bash
# Clone the repo and enter the directory
cd sf-parks

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install django django-filter djangorestframework psycopg2-binary

# Run migrations
python manage.py migrate

# Seed the database with 50 SF parks
python manage.py seed_parks

# (Optional) Create an admin superuser
python manage.py createsuperuser
```

## Running the Server

```bash
source .venv/bin/activate
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to browse parks.

Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Loading Data from Fixture

If you'd rather load from the fixture instead of running the seed command:

```bash
python manage.py loaddata parks/fixtures/parks.json
```

## Project Structure

```
sf-parks/
├── sf_parks/           # Django project settings & root URL config
├── parks/              # Main app
│   ├── models.py       # Category and Park models
│   ├── views.py        # park_list and park_detail views
│   ├── urls.py         # App URL routes
│   ├── admin.py        # Admin configuration
│   ├── fixtures/       # JSON fixture data
│   └── management/
│       └── commands/
│           └── seed_parks.py  # Database seed command
├── templates/
│   ├── base.html              # Base layout (Tailwind CDN)
│   └── parks/
│       ├── park_list.html     # Park listing with filter sidebar
│       └── park_detail.html   # Park detail with Leaflet map
└── manage.py
```
