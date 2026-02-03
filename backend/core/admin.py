from django.contrib import admin
from .models import Video, CodeSnippet, ContactRequest, FAQ, SiteSettings, BannerPlacement, Banner, Partner, Popup, HeaderButton


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["title", "developer", "is_active", "created_at", "preview"]
    list_filter = ["is_active", "developer"]
    search_fields = ["title"]
    raw_id_fields = ["developer"]
    
    fieldsets = (
        (None, {
            "fields": ("title", "youtube_id", "developer", "is_active")
        }),
        ("Превью (выберите один вариант)", {
            "fields": ("thumbnail", "thumbnail_url_external"),
            "description": "Загрузите файл ИЛИ вставьте ссылку. Если оба пустые — возьмётся автоматически с YouTube."
        }),
    )
    
    def preview(self, obj):
        from django.utils.html import format_html
        return format_html('<img src="{}" width="80" height="45" style="object-fit: cover; border-radius: 4px;"/>', obj.thumbnail_url)
    preview.short_description = "Превью"


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "email", "source", "is_processed", "created_at"]
    list_filter = ["is_processed", "source", "created_at"]
    search_fields = ["name", "phone", "email"]
    readonly_fields = ["created_at"]


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


@admin.register(BannerPlacement)
class BannerPlacementAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'banners_count']
    
    def banners_count(self, obj):
        return obj.banners.filter(is_active=True).count()
    banners_count.short_description = "Активных баннеров"


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'placement', 'developer_category', 'popup', 'is_active', 'order', 'preview_desktop']
    list_filter = ['placement', 'is_active', 'developer_category']
    list_editable = ['is_active', 'order']
    search_fields = ['title']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'placement', 'developer_category')
        }),
        ('Desktop изображение', {
            'fields': ('image_desktop', 'image_desktop_url'),
        }),
        ('Mobile изображение', {
            'fields': ('image_mobile', 'image_mobile_url'),
        }),
        ('Действие при клике', {
            'fields': ('popup', 'open_popup', 'link', 'alt_text'),
            'description': 'Popup имеет приоритет над open_popup и link'
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def preview_desktop(self, obj):
        from django.utils.html import format_html
        url = obj.desktop_url
        if url:
            return format_html('<img src="{}" height="40" style="border-radius: 4px;"/>', url)
        return '-'
    preview_desktop.short_description = "Превью"


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'is_active', 'order', 'logo_preview']
    list_filter = ['is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['name']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'website')
        }),
        ('Логотип', {
            'fields': ('logo', 'logo_url'),
            'description': 'Загрузите файл ИЛИ вставьте URL'
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def logo_preview(self, obj):
        from django.utils.html import format_html
        url = obj.logo_image
        if url:
            return format_html('<img src="{}" height="30" style="background:#f5f5f5; padding:4px; border-radius:4px;"/>', url)
        return '-'
    logo_preview.short_description = "Лого"


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