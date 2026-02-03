from django.db import models


class Video(models.Model):
    """Видео от застройщиков"""
    title = models.CharField("Название", max_length=255)
    youtube_id = models.CharField(
        "YouTube ID", 
        max_length=20,
        help_text="ID из ссылки YouTube. Пример: для https://www.youtube.com/watch?v=W7uANluGQSY&t=2s введите: W7uANluGQSY"
    )
    
    developer = models.ForeignKey(
        "developers.Developer", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="videos",
        verbose_name="Застройщик"
    )
    
    # Превью - либо файл, либо URL
    thumbnail = models.ImageField("Превью (файл)", upload_to="videos/", blank=True)
    thumbnail_url_external = models.URLField(
        "Превью (ссылка)", 
        blank=True,
        help_text="Или вставьте ссылку на изображение. Пример: https://img.youtube.com/vi/W7uANluGQSY/maxresdefault.jpg"
    )
    
    views = models.PositiveIntegerField("Просмотры", default=0)
    is_active = models.BooleanField("Активно", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def youtube_url(self):
        return f"https://www.youtube.com/watch?v={self.youtube_id}"

    @property
    def thumbnail_url(self):
        # Приоритет: загруженный файл > внешняя ссылка > автоматическая от YouTube
        if self.thumbnail:
            return self.thumbnail.url
        if self.thumbnail_url_external:
            return self.thumbnail_url_external
        return f"https://img.youtube.com/vi/{self.youtube_id}/maxresdefault.jpg"


class ContactRequest(models.Model):
    """Заявки на консультацию"""
    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    telegram = models.CharField("Telegram", max_length=100, blank=True)
    
    message = models.TextField("Сообщение", blank=True)
    source = models.CharField("Источник", max_length=100, blank=True)
    
    is_processed = models.BooleanField("Обработано", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.created_at:%d.%m.%Y}"


class FAQ(models.Model):
    """Вопросы и ответы"""
    question = models.CharField("Вопрос", max_length=500)
    answer = models.TextField("Ответ")
    
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Вопрос-ответ"
        verbose_name_plural = "Вопросы и ответы"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.question[:50]
    

class SiteSettings(models.Model):
    """Настройки сайта (singleton)"""
    
    # О нас
    about_title = models.CharField("Заголовок секции О нас", max_length=200, default="О нас")
    about_text = models.TextField("Текст О нас (HTML)", blank=True)
    
    # Контакты
    site_name = models.CharField("Название сайта", max_length=100, default="espacademia")
    contact_email = models.EmailField("Email", default="info@espacademia.com")
    contact_phone = models.CharField("Телефон", max_length=50, blank=True)
    contact_address = models.CharField("Адрес", max_length=255, default="Бали, Индонезия")
    
    # Соцсети
    telegram_link = models.URLField("Telegram", default="https://t.me/espacademia", blank=True)
    whatsapp_link = models.URLField("WhatsApp", blank=True)
    instagram_link = models.URLField("Instagram", blank=True)
    youtube_link = models.URLField("YouTube", blank=True)
    
    # SEO
    meta_title = models.CharField("Meta Title главной", max_length=70, default="espacademia - Рейтинг застройщиков Бали")
    meta_description = models.CharField("Meta Description главной", max_length=160, default="Независимый рейтинг застройщиков на Бали")
    
    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
    

class CodeSnippet(models.Model):
    """Сниппеты кода для header/footer"""
    
    LOCATION_CHOICES = [
        ('head', 'Head (перед </head>)'),
        ('body_start', 'Body Start (после <body>)'),
        ('body_end', 'Body End (перед </body>)'),
    ]
    
    name = models.CharField("Название", max_length=100, help_text="Для себя, например: Google Analytics")
    code = models.TextField("Код", help_text="HTML, JS, CSS код")
    location = models.CharField("Расположение", max_length=20, choices=LOCATION_CHOICES, default='head')
    
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Сниппет кода"
        verbose_name_plural = "Сниппеты кода"
        ordering = ["location", "order"]

    def __str__(self):
        return f"{self.name} ({self.get_location_display()})"


class BannerPlacement(models.Model):
    """Места размещения баннеров"""
    PLACEMENT_CHOICES = [
        ('banner_top', 'Верхний баннер (с табами)'),
        ('banner_middle1', 'Средний баннер 1'),
        ('banner_middle2', 'Средний баннер 2'),
        ('sidebar', 'Сайдбар'),
    ]
    
    code = models.CharField("Код", max_length=50, unique=True, choices=PLACEMENT_CHOICES)
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True)
    
    class Meta:
        verbose_name = "Место размещения"
        verbose_name_plural = "Места размещения"
    
    def __str__(self):
        return self.name


class Banner(models.Model):
    """Рекламный баннер"""
    title = models.CharField("Название (для админки)", max_length=255)
    
    placement = models.ForeignKey(
        BannerPlacement, on_delete=models.CASCADE,
        related_name='banners', verbose_name="Место размещения"
    )
    
    # Привязка к категории девелоперов (только для banner_top)
    developer_category = models.ForeignKey(
        'developers.DeveloperCategory', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='banners',
        verbose_name="Категория девелоперов",
        help_text="Только для верхнего баннера с табами"
    )
    
    # Desktop изображения
    image_desktop = models.ImageField(
        "Изображение Desktop", upload_to="banners/desktop/", blank=True
    )
    image_desktop_url = models.URLField(
        "Или URL Desktop", blank=True,
        help_text="Внешняя ссылка на изображение (если не загружаете файл)"
    )
    
    # Mobile изображения
    image_mobile = models.ImageField(
        "Изображение Mobile", upload_to="banners/mobile/", blank=True
    )
    image_mobile_url = models.URLField(
        "Или URL Mobile", blank=True,
        help_text="Внешняя ссылка на мобильное изображение"
    )
    
    # Ссылка и настройки
    link = models.URLField("Ссылка при клике", blank=True)
    open_popup = models.BooleanField(
        "Открывать popup заявки", default=True,
        help_text="Если включено, при клике откроется форма заявки вместо перехода по ссылке"
    )
    alt_text = models.CharField("Alt текст", max_length=255, default="Баннер")
    
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    popup = models.ForeignKey(
        'Popup', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='banners',
        verbose_name="Popup окно",
        help_text="Кастомный popup при клике (вместо стандартного)"
    )
    
    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
        ordering = ['placement', 'order']
    
    def __str__(self):
        return f"{self.title} ({self.placement})"
    
    @property
    def desktop_url(self):
        if self.image_desktop:
            return self.image_desktop.url
        return self.image_desktop_url or ''
    
    @property
    def mobile_url(self):
        if self.image_mobile:
            return self.image_mobile.url
        return self.image_mobile_url or self.desktop_url  # fallback на desktop
    
    @property
    def click_action(self):
        """Возвращает атрибуты для клика"""
        if self.open_popup:
            return 'data-popup="#popup-lead"'
        elif self.link:
            return f'href="{self.link}" target="_blank"'
        return 'href="#"'
    

class Partner(models.Model):
    """Официальные партнеры"""
    name = models.CharField("Название", max_length=100)
    
    logo = models.ImageField("Логотип (файл)", upload_to="partners/", blank=True)
    logo_url = models.URLField("Или URL логотипа", blank=True)
    
    website = models.URLField("Сайт партнера", blank=True)
    
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def logo_image(self):
        if self.logo:
            return self.logo.url
        return self.logo_url or ''


class Popup(models.Model):
    """Кастомные popup окна"""
    name = models.CharField("Название (для админки)", max_length=100)
    slug = models.SlugField("Код popup", unique=True, help_text="Используется в data-popup='#popup-{slug}'")
    
    # Логотипы (2 штуки как на примере)
    logo_left = models.ImageField("Логотип слева", upload_to="popups/", blank=True)
    logo_left_url = models.URLField("Или URL логотипа слева", blank=True)
    logo_right = models.ImageField("Логотип справа", upload_to="popups/", blank=True)
    logo_right_url = models.URLField("Или URL логотипа справа", blank=True)
    
    # Акционный бейдж
    badge_text = models.CharField("Текст бейджа", max_length=50, blank=True, help_text="Например: До 31 декабря!")
    badge_color = models.CharField("Цвет бейджа", max_length=20, default="#BFFF00")
    
    # Заголовок
    title = models.CharField("Заголовок", max_length=255)
    title_highlight = models.CharField(
        "Выделенная часть заголовка", max_length=255, blank=True,
        help_text="Эта часть будет жирной"
    )
    
    # Фон
    background_image = models.ImageField("Фоновая картинка", upload_to="popups/", blank=True)
    background_image_url = models.URLField("Или URL фона", blank=True)
    background_color = models.CharField("Цвет фона", max_length=20, default="#1a1a2e")
    
    # Форма
    input_placeholder = models.CharField("Placeholder поля ввода", max_length=100, default="Введите Ваш WhatsApp")
    button_text = models.CharField("Текст кнопки", max_length=100, default="Получить консультацию")
    button_color = models.CharField("Цвет кнопки", max_length=20, default="#BFFF00")
    
    # Уведомления
    telegram_bot_token = models.CharField("Telegram Bot Token", max_length=100, blank=True)
    telegram_chat_id = models.CharField("Telegram Chat ID", max_length=50, blank=True)
    notification_email = models.EmailField("Email для уведомлений", blank=True)
    
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Popup окно"
        verbose_name_plural = "Popup окна"
    
    def __str__(self):
        return self.name
    
    @property
    def logo_left_image(self):
        if self.logo_left:
            return self.logo_left.url
        return self.logo_left_url or ''
    
    @property
    def logo_right_image(self):
        if self.logo_right:
            return self.logo_right.url
        return self.logo_right_url or ''
    
    @property
    def background_url(self):
        if self.background_image:
            return self.background_image.url
        return self.background_image_url or ''
    
    @property
    def popup_id(self):
        return f"popup-{self.slug}"
    

class HeaderButton(models.Model):
    """Кнопки в header с popup"""
    name = models.CharField("Название кнопки", max_length=100)
    button_text = models.CharField("Текст на кнопке", max_length=100)
    
    popup = models.ForeignKey(
        Popup, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='header_buttons',
        verbose_name="Popup окно"
    )
    
    # Или просто ссылка
    link = models.URLField("Или ссылка", blank=True)
    
    position = models.CharField("Позиция", max_length=20, choices=[
        ('header_main', 'Header основная'),
        ('header_mobile', 'Header мобильная'),
    ], default='header_main')
    
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активна", default=True)
    
    class Meta:
        verbose_name = "Кнопка Header"
        verbose_name_plural = "Кнопки Header"
        ordering = ['position', 'order']
    
    def __str__(self):
        return self.name
