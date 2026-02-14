from django.contrib import admin
from .models import CodeSnippet, ContactRequest, FAQ, SiteSettings, Popup, HeaderButton, Review, WhySpanishItem
from .models import VideoReview


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "email", "source", "is_processed", "created_at"]
    list_filter = ["is_processed", "source", "created_at"]
    search_fields = ["name", "phone", "email"]
    readonly_fields = ["created_at"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'rating', 'is_active', 'created_at']
    list_filter = ['is_active', 'rating']
    list_editable = ['is_active']
    search_fields = ['user_name', 'text']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "order", "is_active"]
    list_filter = ["is_active"]
    list_editable = ["order", "is_active"]
    search_fields = ["question", "answer"]
    ordering = ["order"]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("О нас", {
            "fields": ("about_title", "about_text")
        }),
        ("Контакты", {
            "fields": ("site_name", "contact_email", "contact_phone", "contact_address")
        }),
        ("Соцсети", {
            "fields": ("telegram_link", "whatsapp_link", "instagram_link", "youtube_link")
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description")
        }),
    )
    
    def has_add_permission(self, request):
        # Только одна запись
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
    

@admin.register(VideoReview)
class VideoReviewAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'course_name', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'course_name']
    search_fields = ['user_name']


@admin.register(WhySpanishItem)
class WhySpanishItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'emoji', 'title', 'media_type', 'is_active']
    list_editable = ['order', 'is_active']
    list_display_links = ['title']


@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "order", "is_active", "updated_at"]
    list_filter = ["location", "is_active"]
    list_editable = ["order", "is_active"]
    search_fields = ["name", "code"]
    ordering = ["location", "order"]
    
    fieldsets = (
        (None, {
            "fields": ("name", "location", "is_active", "order")
        }),
        ("Код", {
            "fields": ("code",),
            "description": "Вставьте полный код включая теги <script>, <style> и т.д."
        }),
    )


@admin.register(Popup)
class PopupAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'badge_text', 'is_active', 'has_telegram', 'has_email']
    list_filter = ['is_active']
    search_fields = ['name', 'title']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'is_active')
        }),
        ('Логотипы', {
            'fields': (('logo_left', 'logo_left_url'), ('logo_right', 'logo_right_url')),
        }),
        ('Бейдж акции', {
            'fields': ('badge_text', 'badge_color'),
        }),
        ('Заголовок', {
            'fields': ('title', 'title_highlight'),
            'description': 'title_highlight будет выделен жирным внутри заголовка'
        }),
        ('Фон', {
            'fields': ('background_image', 'background_image_url', 'background_color'),
        }),
        ('Форма', {
            'fields': ('input_placeholder', 'button_text', 'button_color'),
        }),
        ('Уведомления', {
            'fields': ('telegram_bot_token', 'telegram_chat_id', 'notification_email'),
            'description': 'Куда отправлять заявки'
        }),
    )
    
    def has_telegram(self, obj):
        return bool(obj.telegram_bot_token and obj.telegram_chat_id)
    has_telegram.boolean = True
    has_telegram.short_description = "TG"
    
    def has_email(self, obj):
        return bool(obj.notification_email)
    has_email.boolean = True
    has_email.short_description = "Email"


@admin.register(HeaderButton)
class HeaderButtonAdmin(admin.ModelAdmin):
    list_display = ['name', 'button_text', 'position', 'popup', 'is_active', 'order']
    list_filter = ['position', 'is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['name', 'button_text']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'button_text', 'position')
        }),
        ('Действие', {
            'fields': ('popup', 'link'),
            'description': 'Выберите popup ИЛИ укажите ссылку'
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
    )