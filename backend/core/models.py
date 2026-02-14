from django.db import models


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
    contact_address = models.CharField("Адрес", max_length=255, default="Москва, Россия")

    # Соцсети
    telegram_link = models.URLField("Telegram", default="https://t.me/espacademia", blank=True)
    whatsapp_link = models.URLField("WhatsApp", blank=True)
    instagram_link = models.URLField("Instagram", blank=True)
    youtube_link = models.URLField("YouTube", blank=True)
    
    # SEO
    meta_title = models.CharField("Meta Title главной", max_length=70, default="Онлайн курсы испанского языка — ESPacademia")
    meta_description = models.CharField("Meta Description главной", max_length=160, default="Онлайн школа испанского с носителями от А1 до С1. Заговорите за 3 месяца!")
    
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


class Review(models.Model):
    """Отзывы студентов"""
    user_name = models.CharField("Имя", max_length=100)
    user_avatar = models.ImageField("Аватар (файл)", upload_to="reviews/", blank=True)
    user_avatar_url = models.URLField("Или URL аватара", blank=True)
    
    text = models.TextField("Текст отзыва")
    rating = models.PositiveIntegerField("Рейтинг", default=5, help_text="От 1 до 5")
    
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    course_name = models.CharField("Курс", max_length=100, blank=True, help_text="Например: Курс А1, Курс B2")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_name} — {self.rating}★"

    def get_avatar(self):
        if self.user_avatar:
            return self.user_avatar.url
        return self.user_avatar_url or ''
    

class WhySpanishItem(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Изображение'),
        ('video', 'Видео'),
    ]
    
    title = models.CharField('Заголовок', max_length=200)
    emoji = models.CharField('Эмодзи', max_length=10, blank=True)
    description = models.TextField('Описание')
    media_type = models.CharField('Тип медиа', max_length=5, choices=MEDIA_TYPE_CHOICES, default='image')
    image = models.ImageField('Изображение', upload_to='why_spanish/', blank=True)
    video_url = models.URLField('Ссылка на видео (YouTube)', blank=True)
    video_poster = models.ImageField('Обложка видео', upload_to='why_spanish/posters/', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Преимущество испанского'
        verbose_name_plural = 'Преимущества испанского'

    def __str__(self):
        return self.title
    

class VideoReview(models.Model):
    """Видео-отзывы студентов"""
    COURSE_TYPE_CHOICES = [
        ('all', 'Все страницы'),
        ('activo', 'Español Activo'),
        ('intensivo', 'Español Activo Intensivo'),
        ('club', 'Разговорный клуб'),
        ('kids', 'Для детей'),
        ('individual', 'Индивидуальные занятия'),
        ('dele', 'Подготовка к DELE'),
    ]
    user_name = models.CharField("Имя", max_length=100)
    user_avatar = models.ImageField("Аватар (файл)", upload_to="video_reviews/", blank=True)
    user_avatar_url = models.URLField("Или URL аватара", blank=True)
    course_name = models.CharField("Курс", max_length=100, blank=True, help_text="Например: Курс А1")
    course_type = models.CharField(
        "Тип курса", max_length=20,
        choices=COURSE_TYPE_CHOICES, default='all',
        help_text="На какой странице курса показывать"
    )
    youtube_url = models.URLField("Ссылка на YouTube видео")
    poster = models.ImageField("Обложка (если нет — возьмётся с YouTube)", upload_to="video_reviews/posters/", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Видео-отзыв"
        verbose_name_plural = "Видео-отзывы"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.user_name} — {self.course_name}"

    def get_avatar(self):
        if self.user_avatar:
            return self.user_avatar.url
        return self.user_avatar_url or ''

    def get_youtube_id(self):
        """Извлекает YouTube ID из URL"""
        import re
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([^&\n?#]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                return match.group(1)
        return ''

    def get_poster(self):
        if self.poster:
            return self.poster.url
        yt_id = self.get_youtube_id()
        if yt_id:
            return f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
        return ''
    
