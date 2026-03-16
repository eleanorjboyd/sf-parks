import json

from django.core.management.base import BaseCommand

from parks.models import Category, Park

PARKS_DATA = [
    {
        "name": "Golden Gate Park",
        "address": "501 Stanyan St, San Francisco, CA 94117",
        "latitude": 37.7694,
        "longitude": -122.4862,
        "description": "San Francisco's premier urban park spanning over 1,000 acres with gardens, museums, and recreational facilities.",
        "image_url": "https://picsum.photos/seed/golden-gate-park/800/400",
        "categories": ["good_view", "dog_play_area", "bathrooms", "playground", "picnic_area"],
    },
    {
        "name": "Dolores Park",
        "address": "19th & Dolores St, San Francisco, CA 94114",
        "latitude": 37.7596,
        "longitude": -122.4269,
        "description": "Popular park in the Mission District with stunning city views, tennis courts, and a vibrant social scene.",
        "image_url": "https://picsum.photos/seed/dolores-park/800/400",
        "categories": ["good_view", "tennis_courts", "bathrooms", "playground", "dog_play_area", "picnic_area"],
    },
    {
        "name": "Crissy Field",
        "address": "603 Mason St, San Francisco, CA 94129",
        "latitude": 37.8039,
        "longitude": -122.4653,
        "description": "Former military airfield turned waterfront park with stunning Golden Gate Bridge views.",
        "image_url": "https://picsum.photos/seed/crissy-field/800/400",
        "categories": ["good_view", "dog_play_area", "bathrooms", "picnic_area"],
    },
    {
        "name": "Buena Vista Park",
        "address": "Buena Vista Ave, San Francisco, CA 94117",
        "latitude": 37.7688,
        "longitude": -122.4416,
        "description": "One of San Francisco's oldest parks, offering forested trails and panoramic city views.",
        "image_url": "https://picsum.photos/seed/buena-vista-park/800/400",
        "categories": ["good_view", "dog_play_area", "hiking_trails"],
    },
    {
        "name": "Alamo Square",
        "address": "Hayes St & Steiner St, San Francisco, CA 94117",
        "latitude": 37.7764,
        "longitude": -122.4349,
        "description": "Famous for the Painted Ladies Victorian houses with downtown skyline backdrop.",
        "image_url": "https://picsum.photos/seed/alamo-square/800/400",
        "categories": ["good_view", "dog_play_area", "playground", "picnic_area"],
    },
    {
        "name": "Lands End",
        "address": "680 Point Lobos Ave, San Francisco, CA 94121",
        "latitude": 37.7879,
        "longitude": -122.5105,
        "description": "Rugged coastal trail park with dramatic views of the Golden Gate Bridge and Marin Headlands.",
        "image_url": "https://picsum.photos/seed/lands-end/800/400",
        "categories": ["good_view", "hiking_trails"],
    },
    {
        "name": "Twin Peaks",
        "address": "501 Twin Peaks Blvd, San Francisco, CA 94114",
        "latitude": 37.7544,
        "longitude": -122.4477,
        "description": "Two prominent hills offering 360-degree panoramic views of the San Francisco Bay Area.",
        "image_url": "https://picsum.photos/seed/twin-peaks/800/400",
        "categories": ["good_view", "hiking_trails"],
    },
    {
        "name": "Bernal Heights Park",
        "address": "Bernal Heights Blvd, San Francisco, CA 94110",
        "latitude": 37.7427,
        "longitude": -122.4153,
        "description": "Hilltop park known for off-leash dog walking and sweeping city views.",
        "image_url": "https://picsum.photos/seed/bernal-heights/800/400",
        "categories": ["good_view", "dog_play_area", "hiking_trails"],
    },
    {
        "name": "Lafayette Park",
        "address": "Washington St & Laguna St, San Francisco, CA 94115",
        "latitude": 37.7914,
        "longitude": -122.4283,
        "description": "Pacific Heights hilltop park with city views, tennis courts, and a playground.",
        "image_url": "https://picsum.photos/seed/lafayette-park/800/400",
        "categories": ["good_view", "tennis_courts", "playground", "dog_play_area", "picnic_area"],
    },
    {
        "name": "Presidio",
        "address": "103 Montgomery St, San Francisco, CA 94129",
        "latitude": 37.7989,
        "longitude": -122.4662,
        "description": "Former military base turned national park with forests, trails, coastal bluffs, and historic buildings.",
        "image_url": "https://picsum.photos/seed/presidio-sf/800/400",
        "categories": ["good_view", "hiking_trails", "dog_play_area", "bathrooms", "picnic_area", "playground"],
    },
    {
        "name": "McLaren Park",
        "address": "100 John F Shelley Dr, San Francisco, CA 94134",
        "latitude": 37.7186,
        "longitude": -122.4205,
        "description": "San Francisco's second largest park with trails, meadows, and a golf course.",
        "image_url": "https://picsum.photos/seed/mclaren-park/800/400",
        "categories": ["hiking_trails", "dog_play_area", "playground", "bathrooms", "picnic_area"],
    },
    {
        "name": "Glen Canyon Park",
        "address": "Bosworth St & O'Shaughnessy Blvd, San Francisco, CA 94127",
        "latitude": 37.7396,
        "longitude": -122.4408,
        "description": "Hidden canyon with a creek, native plants, and hiking trails in the heart of the city.",
        "image_url": "https://picsum.photos/seed/glen-canyon/800/400",
        "categories": ["hiking_trails", "dog_play_area", "playground"],
    },
    {
        "name": "Ocean Beach",
        "address": "Great Hwy, San Francisco, CA 94122",
        "latitude": 37.7594,
        "longitude": -122.5107,
        "description": "Miles of sandy beach along the Pacific coast, popular for surfing and bonfires.",
        "image_url": "https://picsum.photos/seed/ocean-beach-sf/800/400",
        "categories": ["good_view", "dog_play_area"],
    },
    {
        "name": "Baker Beach",
        "address": "1504 Pershing Dr, San Francisco, CA 94129",
        "latitude": 37.7935,
        "longitude": -122.4835,
        "description": "Sandy beach in the Presidio with iconic views of the Golden Gate Bridge.",
        "image_url": "https://picsum.photos/seed/baker-beach/800/400",
        "categories": ["good_view", "bathrooms", "picnic_area"],
    },
    {
        "name": "Corona Heights Park",
        "address": "Roosevelt Way & Museum Way, San Francisco, CA 94114",
        "latitude": 37.7654,
        "longitude": -122.4392,
        "description": "Rocky hilltop park with panoramic views, a dog play area, and the Randall Museum.",
        "image_url": "https://picsum.photos/seed/corona-heights/800/400",
        "categories": ["good_view", "dog_play_area", "hiking_trails"],
    },
    {
        "name": "Stern Grove",
        "address": "19th Ave & Sloat Blvd, San Francisco, CA 94132",
        "latitude": 37.7348,
        "longitude": -122.4745,
        "description": "A natural amphitheater in a eucalyptus grove famous for free summer concerts.",
        "image_url": "https://picsum.photos/seed/stern-grove/800/400",
        "categories": ["dog_play_area", "picnic_area", "hiking_trails"],
    },
    {
        "name": "Washington Square",
        "address": "Filbert St & Stockton St, San Francisco, CA 94133",
        "latitude": 37.8003,
        "longitude": -122.4103,
        "description": "Charming North Beach park with views of Saints Peter and Paul Church.",
        "image_url": "https://picsum.photos/seed/washington-square/800/400",
        "categories": ["playground", "picnic_area"],
    },
    {
        "name": "Alta Plaza Park",
        "address": "Jackson St & Steiner St, San Francisco, CA 94115",
        "latitude": 37.7909,
        "longitude": -122.4363,
        "description": "Terraced Pacific Heights park with tennis courts, a playground, and city views.",
        "image_url": "https://picsum.photos/seed/alta-plaza/800/400",
        "categories": ["good_view", "tennis_courts", "playground", "dog_play_area"],
    },
    {
        "name": "Huntington Park",
        "address": "1000 California St, San Francisco, CA 94108",
        "latitude": 37.7921,
        "longitude": -122.4118,
        "description": "Elegant Nob Hill park with a playground and replica of a Roman fountain.",
        "image_url": "https://picsum.photos/seed/huntington-park/800/400",
        "categories": ["playground", "good_view"],
    },
    {
        "name": "South Park",
        "address": "64 South Park Ave, San Francisco, CA 94107",
        "latitude": 37.7828,
        "longitude": -122.3934,
        "description": "Cozy oval park in the SoMa neighborhood surrounded by tech offices and residences.",
        "image_url": "https://picsum.photos/seed/south-park-sf/800/400",
        "categories": ["playground", "picnic_area"],
    },
    {
        "name": "Precita Park",
        "address": "Precita Ave & Folsom St, San Francisco, CA 94110",
        "latitude": 37.7479,
        "longitude": -122.4127,
        "description": "Neighborhood park in Bernal Heights with a playground and community garden.",
        "image_url": "https://picsum.photos/seed/precita-park/800/400",
        "categories": ["playground", "picnic_area", "dog_play_area"],
    },
    {
        "name": "Mountain Lake Park",
        "address": "Lake St & 12th Ave, San Francisco, CA 94118",
        "latitude": 37.7872,
        "longitude": -122.4722,
        "description": "Park surrounding a natural spring-fed lake at the edge of the Presidio.",
        "image_url": "https://picsum.photos/seed/mountain-lake/800/400",
        "categories": ["playground", "dog_play_area", "picnic_area", "bathrooms"],
    },
    {
        "name": "Balboa Park",
        "address": "San Jose Ave & Ocean Ave, San Francisco, CA 94112",
        "latitude": 37.7247,
        "longitude": -122.4414,
        "description": "Community park in the Excelsior with sports facilities, pool, and playground.",
        "image_url": "https://picsum.photos/seed/balboa-park-sf/800/400",
        "categories": ["playground", "bathrooms", "tennis_courts", "picnic_area"],
    },
    {
        "name": "Crocker Amazon Playground",
        "address": "Moscow St & Geneva Ave, San Francisco, CA 94112",
        "latitude": 37.7103,
        "longitude": -122.4315,
        "description": "Large park with sports fields, tennis courts, and a playground in the Excelsior.",
        "image_url": "https://picsum.photos/seed/crocker-amazon/800/400",
        "categories": ["playground", "tennis_courts", "bathrooms", "dog_play_area"],
    },
    {
        "name": "Holly Park",
        "address": "Holly Park Cir, San Francisco, CA 94110",
        "latitude": 37.7392,
        "longitude": -122.4110,
        "description": "Hilltop park in Bernal Heights with city views and grassy areas.",
        "image_url": "https://picsum.photos/seed/holly-park/800/400",
        "categories": ["good_view", "dog_play_area", "picnic_area"],
    },
    {
        "name": "India Basin Shoreline Park",
        "address": "900 Innes Ave, San Francisco, CA 94124",
        "latitude": 37.7355,
        "longitude": -122.3753,
        "description": "Bayfront park with shoreline trails and bay views in the Bayview-Hunters Point neighborhood.",
        "image_url": "https://picsum.photos/seed/india-basin/800/400",
        "categories": ["good_view", "hiking_trails"],
    },
    {
        "name": "Heron's Head Park",
        "address": "32 Jennings St, San Francisco, CA 94124",
        "latitude": 37.7398,
        "longitude": -122.3719,
        "description": "Wetland park and nature area along the bay, great for birdwatching.",
        "image_url": "https://picsum.photos/seed/herons-head/800/400",
        "categories": ["good_view", "hiking_trails"],
    },
    {
        "name": "Candlestick Point State Recreation Area",
        "address": "100 Hunters Point Expy, San Francisco, CA 94124",
        "latitude": 37.7133,
        "longitude": -122.3798,
        "description": "Bayfront state park with fishing piers, trails, and bay views near the old stadium site.",
        "image_url": "https://picsum.photos/seed/candlestick-point/800/400",
        "categories": ["good_view", "hiking_trails", "bathrooms", "picnic_area"],
    },
    {
        "name": "Ina Coolbrith Park",
        "address": "1795 Taylor St, San Francisco, CA 94133",
        "latitude": 37.7985,
        "longitude": -122.4131,
        "description": "Tiny terraced park near Russian Hill with spectacular views of the Bay Bridge and skyline.",
        "image_url": "https://picsum.photos/seed/ina-coolbrith/800/400",
        "categories": ["good_view"],
    },
    {
        "name": "Fort Funston",
        "address": "Fort Funston Rd, San Francisco, CA 94132",
        "latitude": 37.7136,
        "longitude": -122.5027,
        "description": "Coastal bluff park popular for hang gliding and off-leash dog walking.",
        "image_url": "https://picsum.photos/seed/fort-funston/800/400",
        "categories": ["good_view", "dog_play_area", "hiking_trails", "bathrooms"],
    },
    {
        "name": "Yerba Buena Gardens",
        "address": "750 Howard St, San Francisco, CA 94103",
        "latitude": 37.7852,
        "longitude": -122.4026,
        "description": "Downtown park and cultural center with gardens, public art, and an ice rink.",
        "image_url": "https://picsum.photos/seed/yerba-buena/800/400",
        "categories": ["playground", "bathrooms", "picnic_area"],
    },
    {
        "name": "Civic Center Plaza",
        "address": "335 McAllister St, San Francisco, CA 94102",
        "latitude": 37.7793,
        "longitude": -122.4182,
        "description": "Formal plaza in the civic center surrounded by City Hall and cultural institutions.",
        "image_url": "https://picsum.photos/seed/civic-center/800/400",
        "categories": ["bathrooms"],
    },
    {
        "name": "Sue Bierman Park",
        "address": "1 Ferry Building, San Francisco, CA 94111",
        "latitude": 37.7953,
        "longitude": -122.3961,
        "description": "Downtown park near the Ferry Building with trees, benches, and parrot colonies.",
        "image_url": "https://picsum.photos/seed/sue-bierman/800/400",
        "categories": ["picnic_area"],
    },
    {
        "name": "Justin Herman Plaza (Embarcadero Plaza)",
        "address": "1 Market St, San Francisco, CA 94105",
        "latitude": 37.7944,
        "longitude": -122.3947,
        "description": "Waterfront plaza at the foot of Market Street near the Ferry Building.",
        "image_url": "https://picsum.photos/seed/embarcadero-plaza/800/400",
        "categories": ["good_view"],
    },
    {
        "name": "Rincon Park",
        "address": "The Embarcadero & Folsom St, San Francisco, CA 94105",
        "latitude": 37.7900,
        "longitude": -122.3883,
        "description": "Waterfront park with the Cupid's Span sculpture and Bay Bridge views.",
        "image_url": "https://picsum.photos/seed/rincon-park/800/400",
        "categories": ["good_view", "picnic_area"],
    },
    {
        "name": "Potrero Hill Recreation Center",
        "address": "801 Arkansas St, San Francisco, CA 94107",
        "latitude": 37.7597,
        "longitude": -122.3979,
        "description": "Neighborhood recreation center with sports facilities and panoramic views.",
        "image_url": "https://picsum.photos/seed/potrero-hill/800/400",
        "categories": ["good_view", "tennis_courts", "playground", "bathrooms"],
    },
    {
        "name": "McKinley Square",
        "address": "20th & Vermont St, San Francisco, CA 94107",
        "latitude": 37.7598,
        "longitude": -122.4040,
        "description": "Small hilltop park on Potrero Hill with dog play area and downtown views.",
        "image_url": "https://picsum.photos/seed/mckinley-square/800/400",
        "categories": ["good_view", "dog_play_area"],
    },
    {
        "name": "Grattan Playground",
        "address": "Grattan St & Stanyan St, San Francisco, CA 94117",
        "latitude": 37.7636,
        "longitude": -122.4549,
        "description": "Cole Valley playground with a climbing structure and basketball court.",
        "image_url": "https://picsum.photos/seed/grattan-playground/800/400",
        "categories": ["playground", "bathrooms"],
    },
    {
        "name": "Noe Valley Town Square",
        "address": "3861 24th St, San Francisco, CA 94114",
        "latitude": 37.7511,
        "longitude": -122.4310,
        "description": "Community gathering space in the heart of Noe Valley with seating and events.",
        "image_url": "https://picsum.photos/seed/noe-valley/800/400",
        "categories": ["picnic_area"],
    },
    {
        "name": "Walter Haas Playground",
        "address": "Diamond St & 30th St, San Francisco, CA 94131",
        "latitude": 37.7412,
        "longitude": -122.4344,
        "description": "Renovated playground in Diamond Heights with modern play structures.",
        "image_url": "https://picsum.photos/seed/walter-haas/800/400",
        "categories": ["playground", "bathrooms", "picnic_area"],
    },
    {
        "name": "Miraloma Playground",
        "address": "Omar Way & Sequoia Way, San Francisco, CA 94127",
        "latitude": 37.7386,
        "longitude": -122.4554,
        "description": "Neighborhood playground near Mount Davidson with a play area and tennis courts.",
        "image_url": "https://picsum.photos/seed/miraloma/800/400",
        "categories": ["playground", "tennis_courts"],
    },
    {
        "name": "Mount Davidson Park",
        "address": "125 Dalewood Way, San Francisco, CA 94127",
        "latitude": 37.7379,
        "longitude": -122.4546,
        "description": "The highest natural point in San Francisco, topped with a large cross and surrounded by forest.",
        "image_url": "https://picsum.photos/seed/mount-davidson/800/400",
        "categories": ["good_view", "hiking_trails"],
    },
    {
        "name": "John McLaren Playground",
        "address": "John McLaren Playground, San Francisco, CA 94110",
        "latitude": 37.7444,
        "longitude": -122.4177,
        "description": "Community park in the Mission with baseball fields and play areas.",
        "image_url": "https://picsum.photos/seed/mclaren-playground/800/400",
        "categories": ["playground", "bathrooms"],
    },
    {
        "name": "Garfield Square",
        "address": "26th St & Harrison St, San Francisco, CA 94110",
        "latitude": 37.7497,
        "longitude": -122.4147,
        "description": "Active community park in the Mission with a pool, gym, and sports fields.",
        "image_url": "https://picsum.photos/seed/garfield-square/800/400",
        "categories": ["playground", "bathrooms", "picnic_area"],
    },
    {
        "name": "Cayuga Playground",
        "address": "301 Naglee Ave, San Francisco, CA 94112",
        "latitude": 37.7217,
        "longitude": -122.4437,
        "description": "Neighborhood park in the Outer Mission with a playground and community garden.",
        "image_url": "https://picsum.photos/seed/cayuga/800/400",
        "categories": ["playground", "picnic_area"],
    },
    {
        "name": "Rolph Playground",
        "address": "Potrero Ave & Army St, San Francisco, CA 94110",
        "latitude": 37.7486,
        "longitude": -122.4067,
        "description": "Large playground with sports facilities in the Potrero district.",
        "image_url": "https://picsum.photos/seed/rolph-playground/800/400",
        "categories": ["playground", "tennis_courts", "bathrooms"],
    },
    {
        "name": "Visitacion Valley Greenway",
        "address": "Leland Ave & Visitacion Ave, San Francisco, CA 94134",
        "latitude": 37.7128,
        "longitude": -122.4116,
        "description": "Series of connected green spaces running through the Visitacion Valley neighborhood.",
        "image_url": "https://picsum.photos/seed/visitacion-valley/800/400",
        "categories": ["picnic_area", "playground"],
    },
    {
        "name": "Randall Museum",
        "address": "199 Museum Way, San Francisco, CA 94114",
        "latitude": 37.7649,
        "longitude": -122.4381,
        "description": "Free children's museum adjacent to Corona Heights with nature exhibits and a petting zoo.",
        "image_url": "https://picsum.photos/seed/randall-museum/800/400",
        "categories": ["good_view", "bathrooms"],
    },
    {
        "name": "Tank Hill Park",
        "address": "Twin Peaks, San Francisco, CA 94114",
        "latitude": 37.7571,
        "longitude": -122.4481,
        "description": "Small hidden park near Twin Peaks with sweeping views of downtown and the bay.",
        "image_url": "https://picsum.photos/seed/tank-hill/800/400",
        "categories": ["good_view", "hiking_trails"],
    },
    {
        "name": "Esprit Park",
        "address": "Minnesota St & 19th St, San Francisco, CA 94107",
        "latitude": 37.7612,
        "longitude": -122.3898,
        "description": "Small peaceful park in Dogpatch with gardens and seating areas.",
        "image_url": "https://picsum.photos/seed/esprit-park/800/400",
        "categories": ["picnic_area", "dog_play_area"],
    },
]


class Command(BaseCommand):
    help = "Seed the database with SF parks and categories"

    def handle(self, *args, **options):
        self.stdout.write("Seeding categories...")
        category_map = {}
        category_slugs = set()
        for park_data in PARKS_DATA:
            for slug in park_data["categories"]:
                category_slugs.add(slug)

        for slug in sorted(category_slugs):
            name = slug.replace("_", " ").title()
            cat, created = Category.objects.get_or_create(
                slug=slug, defaults={"name": name}
            )
            category_map[slug] = cat
            status = "created" if created else "exists"
            self.stdout.write(f"  Category '{name}' ({status})")

        self.stdout.write(f"\nSeeding {len(PARKS_DATA)} parks...")
        for park_data in PARKS_DATA:
            cat_slugs = park_data.pop("categories")
            park, created = Park.objects.get_or_create(
                name=park_data["name"], defaults=park_data
            )
            park.categories.set([category_map[s] for s in cat_slugs])
            status = "created" if created else "exists"
            self.stdout.write(f"  Park '{park.name}' ({status})")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! {Park.objects.count()} parks, {Category.objects.count()} categories."
            )
        )

        # Export fixture
        fixture = []
        for cat in Category.objects.all():
            fixture.append(
                {
                    "model": "parks.category",
                    "pk": cat.pk,
                    "fields": {"name": cat.name, "slug": cat.slug},
                }
            )
        for park in Park.objects.prefetch_related("categories").all():
            fixture.append(
                {
                    "model": "parks.park",
                    "pk": park.pk,
                    "fields": {
                        "name": park.name,
                        "address": park.address,
                        "latitude": park.latitude,
                        "longitude": park.longitude,
                        "description": park.description,
                        "image_url": park.image_url,
                        "categories": list(
                            park.categories.values_list("pk", flat=True)
                        ),
                    },
                }
            )

        import os

        fixture_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "fixtures",
        )
        os.makedirs(fixture_dir, exist_ok=True)
        fixture_path = os.path.join(fixture_dir, "parks.json")
        with open(fixture_path, "w") as f:
            json.dump(fixture, f, indent=2)
        self.stdout.write(self.style.SUCCESS(f"Fixture written to {fixture_path}"))
