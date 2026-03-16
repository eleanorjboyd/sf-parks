# SF Parks Explorer

A Django web app for discovering and filtering San Francisco's parks.

## Features

- Browse 50 San Francisco parks with photos, descriptions, and category tags
- Filter parks by category (Good View, Dog Play Area, Bathrooms, Tennis Courts, etc.)
- Interactive Leaflet map on each park's detail page
- Admin interface for managing parks and categories

## Requirements

- Python 3.10+ but prefer higher

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
