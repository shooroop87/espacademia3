from django.contrib import admin
from .models import Property, PropertyType, Location, PropertyImage


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3
    fields = ["image", "image_url", "order"]


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ["name", "developer", "property_type", "location", "price_from", "status", "is_featured"]
    list_filter = ["status", "construction_status", "property_type", "location", "is_featured"]
    search_fields = ["name", "short_description"]
    prepopulated_fields = {"slug": ("name",)}
    raw_id_fields = ["developer"]
    inlines = [PropertyImageInline]
    
    fieldsets = (
        (None, {
            "fields": ("name", "slug", "developer", "property_type", "location")
        }),
        ("Медиа", {
            "fields": ("main_image", "main_image_url"),
            "description": "Загрузите файл ИЛИ вставьте ссылку"
        }),
        ("Характеристики", {
            "fields": ("price_from", "area", "rooms", "has_garage", "roi_percent")
        }),
        ("Статусы", {
            "fields": ("status", "construction_status", "completion_date", "is_featured", "is_active")
        }),
        ("Геолокация", {
            "fields": ("address", "latitude", "longitude"),
            "classes": ("collapse",),
        }),
        ("Расстояния до объектов", {
            "fields": (
                ("distance_beach", "ocean_distance"),
                ("distance_school", "distance_supermarket"),
                ("distance_clinic", "distance_pharmacy"),
                ("distance_park", "distance_gym"),
                ("distance_cafe", "distance_shopping"),
                ("distance_center", "distance_airport"),
            ),
            "classes": ("collapse",),
        }),
        ("Описание", {
            "fields": ("short_description", "description")
        }),
    )