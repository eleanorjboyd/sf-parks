from django.contrib import admin

from .models import Category, Park


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    list_filter = ("categories",)
    search_fields = ("name", "address", "description")
    filter_horizontal = ("categories",)
