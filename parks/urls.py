from django.urls import path

from . import views

app_name = "parks"

urlpatterns = [
    path("", views.park_list, name="park_list"),
    path("park/<int:pk>/", views.park_detail, name="park_detail"),
]
