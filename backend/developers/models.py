from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class DeveloperCategory(models.Model):
    """Категории: Премиум, Бизнес+, Средний"""
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField("Иконка (URL)", max_length=500, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Категория девелоперов"
        verbose_name_plural = "Категории девелоперов"
        ordering = ["order"]

    def __str__(self):
        return self.name


class Developer(models.Model):
    """Застройщик"""
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    
    category = models.ForeignKey(
        DeveloperCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="developers"
    )

    short_description_for_property = models.TextField("Краткое описание", max_length=300, blank=True, 
        help_text="Для карточки на странице объекта")
    
    logo = models.ImageField("Логотип", upload_to="developers/logos/", blank=True)
    cover_image = models.ImageField("Обложка", upload_to="developers/covers/", blank=True)
    
    short_description = models.TextField("Краткое описание", max_length=500, blank=True)
    description = models.TextField("Полное описание (HTML)", blank=True)
    
    # Статистика
    completed_count = models.PositiveIntegerField("Сдано объектов", default=0)
    in_progress_count = models.PositiveIntegerField("Строится объектов", default=0)
    
    # Рейтинги (1-5)
    rating = models.DecimalField("Общий рейтинг", max_digits=2, decimal_places=1, default=5.0)
    premium_rating = models.PositiveSmallIntegerField("Премиальность", default=5)
    support_rating = models.PositiveSmallIntegerField("Поддержка", default=5)
    quality_rating = models.PositiveSmallIntegerField("Качество", default=5)
    
    # Контакты
    website = models.URLField("Сайт", blank=True)
    telegram = models.CharField("Telegram", max_length=100, blank=True)
    whatsapp = models.CharField("WhatsApp", max_length=50, blank=True)
    instagram = models.CharField("Instagram", max_length=100, blank=True)
    
    is_verified = models.BooleanField("Верифицирован", default=False)
    is_active = models.BooleanField("Активен", default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Год основания и слоган
    founded_year = models.PositiveIntegerField("Год основания", null=True, blank=True)
    tagline = models.CharField("Слоган/тип компании", max_length=255, blank=True, 
        help_text="Например: Бутик-девелопер и управляющая компания")
    
    # Детальные рейтинги (в процентах для прогресс-бара, 0-100)
    rating_deadline = models.PositiveSmallIntegerField("Рейтинг: Срок сдачи (%)", default=80)
    rating_premium = models.PositiveSmallIntegerField("Рейтинг: Премиальность (%)", default=80)
    rating_support = models.PositiveSmallIntegerField("Рейтинг: Поддержка (%)", default=80)
    rating_quality = models.PositiveSmallIntegerField("Рейтинг: Качество (%)", default=80)
    
    # Расширенное описание
    innovations = models.TextField("Инновации и устойчивое развитие", blank=True)
    services = models.TextField("Сервис и философия", blank=True)
    
    @property
    def rating_deadline_display(self):
        return f"{self.rating_deadline // 20}/5"
    
    @property
    def rating_premium_display(self):
        return f"{self.rating_premium // 20}/5"
    
    @property
    def rating_support_display(self):
        return f"{self.rating_support // 20}/5"
    
    @property
    def rating_quality_display(self):
        return f"{self.rating_quality // 20}/5"

    class Meta:
        verbose_name = "Застройщик"
        verbose_name_plural = "Застройщики"
        ordering = ["-rating", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("developers:detail", kwargs={"slug": self.slug})

    @property
    def total_objects(self):
        return self.completed_count + self.in_progress_count

    @property
    def reviews_count(self):
        return self.reviews.count()


class DeveloperReview(models.Model):
    """Отзыв о застройщике"""
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    
    user_name = models.CharField("Имя", max_length=100)
    user_avatar = models.ImageField("Аватар", upload_to="reviews/avatars/", blank=True)
    user_avatar_url = models.URLField("Или ссылка на аватар", max_length=500, blank=True)
    
    rating = models.PositiveSmallIntegerField("Оценка", choices=[(i, str(i)) for i in range(1, 6)])
    text = models.TextField("Текст отзыва")
    
    is_approved = models.BooleanField("Одобрен", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_name} → {self.developer.name}"
    
    def get_avatar(self):
        """Возвращает URL аватара."""
        if self.user_avatar:
            return self.user_avatar.url
        return self.user_avatar_url or ''
    

class DeveloperHighlight(models.Model):
    """Ключевые преимущества застройщика (буллеты)"""
    developer = models.ForeignKey(
        Developer, on_delete=models.CASCADE,
        related_name="highlights", verbose_name="Застройщик"
    )
    text = models.CharField("Текст", max_length=500)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"
        ordering = ["order"]

    def __str__(self):
        return self.text[:50]
