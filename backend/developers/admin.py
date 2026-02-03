from django.contrib import admin
from .models import Developer, DeveloperCategory, DeveloperReview, DeveloperHighlight


@admin.register(DeveloperCategory)
class DeveloperCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order"]
    prepopulated_fields = {"slug": ("name",)}


class DeveloperHighlightInline(admin.TabularInline):
    model = DeveloperHighlight
    extra = 3


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "rating", "is_verified", "is_active"]
    list_filter = ["category", "is_verified", "is_active"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [DeveloperHighlightInline]
    
    fieldsets = (
        (None, {
            "fields": ("name", "slug", "category", "logo")
        }),
        ("Основная информация", {
            "fields": ("founded_year", "tagline", "short_description", "short_description_for_property", "description")
        }),
        ("Детальное описание", {
            "fields": ("innovations", "services"),
            "classes": ("collapse",),
        }),
        ("Статистика объектов", {
            "fields": (("completed_count", "in_progress_count"),),
            "description": "Количество объектов (вводится вручную)"
        }),
        ("Рейтинги", {
            "fields": ("rating", ("rating_deadline", "rating_premium"), ("rating_support", "rating_quality"))
        }),
        ("Контакты", {
            "fields": ("website", "telegram", "whatsapp")
        }),
        ("Статусы", {
            "fields": ("is_verified", "is_active")
        }),
    )


@admin.register(DeveloperReview)
class DeveloperReviewAdmin(admin.ModelAdmin):
    list_display = ["user_name", "developer", "rating", "is_approved", "created_at"]
    list_filter = ["is_approved", "rating", "created_at"]
    search_fields = ["user_name", "text", "developer__name"]
    
    fieldsets = (
        (None, {
            "fields": ("developer", "user_name", "user_avatar", "user_avatar_url", "rating", "text")
        }),
        ("Модерация", {
            "fields": ("is_approved", "user")
        }),
    )


@admin.register(DeveloperHighlight)
class DeveloperHighlightAdmin(admin.ModelAdmin):
    list_display = ["text", "developer", "order"]
    list_filter = ["developer"]
    search_fields = ["text"]
    raw_id_fields = ["developer"]
