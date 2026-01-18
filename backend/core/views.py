from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from django.db.models import Prefetch
from django.core.paginator import Paginator

from developers.models import Developer, DeveloperCategory, DeveloperReview
from properties.models import Property
from events.models import Event
from blog.models import BlogPost
from news.models import NewsPost
from .models import Video, FAQ, SiteSettings

from django.views.decorators.http import require_POST


def index(request):
    """Главная страница."""
    
    # Настройки сайта
    settings = SiteSettings.get()
    
    # Застройщики с фильтрацией по категориям
    categories = DeveloperCategory.objects.prefetch_related(
        Prefetch(
            'developers',
            queryset=Developer.objects.filter(is_active=True).order_by('-rating')
        )
    ).order_by('order')

    featured_developers = Developer.objects.filter(is_active=True).order_by('-rating')[:10]
    
    # Объекты недвижимости
    featured_properties = Property.objects.filter(
        is_active=True, is_featured=True
    ).select_related('developer', 'property_type', 'location')[:6]
    
    # Мероприятия
    upcoming_events = Event.objects.filter(status='upcoming').order_by('event_date')[:2]
    
    # Новости
    latest_news = NewsPost.objects.filter(status='published').order_by('-published_at')[:3]
    
    # Статьи
    latest_posts = BlogPost.objects.filter(status='published').order_by('-published_at')[:3]

    # Видео
    videos = Video.objects.filter(is_active=True).select_related('developer')[:10]
    
    # Отзывы
    reviews = DeveloperReview.objects.filter(is_approved=True).select_related('developer').order_by('-created_at')[:6]
    
    # FAQ
    faqs = FAQ.objects.filter(is_active=True)
    
    context = {
        'settings': settings,
        'categories': categories,
        'featured_developers': featured_developers,
        'featured_properties': featured_properties,
        'upcoming_events': upcoming_events,
        'latest_news': latest_news,
        'latest_posts': latest_posts,
        'videos': videos,
        'reviews': reviews,
        'faqs': faqs,
    }
    
    return render(request, "pages/index.html", context)


def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')


def terms_of_use(request):
    return render(request, 'pages/terms_of_use.html')


def developer_award_2025(request):
    return render(request, 'pages/developer_award_2025.html')

@require_POST
def contact_request(request):
    """Обработка формы заявки"""
    from .models import ContactRequest
    
    name = request.POST.get('name', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')
    telegram = request.POST.get('telegram', '')
    message = request.POST.get('message', '')
    source = request.POST.get('source', 'website')
    
    if name:
        ContactRequest.objects.create(
            name=name,
            phone=phone,
            email=email,
            telegram=telegram,
            message=message,
            source=source,
        )
        messages.success(request, 'Спасибо! Ваша заявка отправлена.')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


def video_list(request):
    videos = Video.objects.select_related('developer').order_by('-created_at')
    
    # Фильтр по застройщику
    developer_slug = request.GET.get('developer')
    if developer_slug:
        videos = videos.filter(developer__slug=developer_slug)
    
    paginator = Paginator(videos, 8)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'videos': page_obj,
        'page_obj': page_obj,
        'developers_with_videos': Developer.objects.filter(videos__isnull=False).annotate(video_count=Count('videos')).distinct(),
        'popular_videos': Video.objects.order_by('-views')[:3],
        'total_videos': Video.objects.count(),
        'current_developer': developer_slug,
    }
    return render(request, 'videos/video_list.html', context)
