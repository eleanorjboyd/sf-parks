from django.db import migrations


# Parks to delete (playgrounds)
PLAYGROUNDS = [
    "Cayuga Playground",
    "Crocker Amazon Playground",
    "Grattan Playground",
    "John McLaren Playground",
    "Miraloma Playground",
    "Rolph Playground",
    "Walter Haas Playground",
]

# Map park names to their new image filenames
IMAGE_MAP = {
    "Balboa Park": "balboa.jpg",
    "Bernal Heights Park": "bernal.jpg",
    "Civic Center Plaza": "civic.jpeg",
    "Esprit Park": "esprit.jpg",
    "Fort Funston": "fort-funston-beach.jpg",
    "Garfield Square": "garfield.jpeg",
    "Ina Coolbrith Park": "ina.jpg",
    "Justin Herman Plaza (Embarcadero Plaza)": "justin.jpg",
    "McKinley Square": "mckinley.jpeg",
    "McLaren Park": "mclaren.jpeg",
    "Mount Davidson Park": "mount-davidson.jpeg",
    "Noe Valley Town Square": "noe.jpg",
    "Rincon Park": "rincon-park-5.jpg",
    "South Park": "south.jpeg",
    "Sue Bierman Park": "sue.jpeg",
    "Tank Hill Park": "tank-hill-city-view.jpg",
    "Visitacion Valley Greenway": "visitacoin.jpg",
    "Yerba Buena Gardens": "yerba.jpg",
}


def forward(apps, schema_editor):
    Park = apps.get_model("parks", "Park")

    # Remove playgrounds
    Park.objects.filter(name__in=PLAYGROUNDS).delete()

    # Assign images
    for name, filename in IMAGE_MAP.items():
        Park.objects.filter(name=name).update(image=filename)


def reverse(apps, schema_editor):
    # Clear the images we set (can't recreate deleted parks)
    Park = apps.get_model("parks", "Park")
    for name in IMAGE_MAP:
        Park.objects.filter(name=name).update(image="")


class Migration(migrations.Migration):

    dependencies = [
        ("parks", "0003_populate_park_images"),
    ]

    operations = [
        migrations.RunPython(forward, reverse),
    ]
