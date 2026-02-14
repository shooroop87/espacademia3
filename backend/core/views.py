from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from django.db.models import Prefetch

from events.models import Event
from .models import FAQ, Review, SiteSettings, VideoReview, WhySpanishItem

from django.views.decorators.http import require_POST


def index(request):
    """Главная страница."""
    
    # Настройки сайта
    settings = SiteSettings.get()

    why_spanish_items = WhySpanishItem.objects.filter(is_active=True)

    # Мероприятия
    upcoming_events = Event.objects.filter(status='upcoming').order_by('event_date')[:2]

    # FAQ
    faqs = FAQ.objects.filter(is_active=True)

    context = {
        'settings': settings,
        'faqs': faqs,
        'why_spanish_items': why_spanish_items,
        'video_reviews': VideoReview.objects.filter(is_active=True),
        'reviews': Review.objects.filter(is_active=True)[:10],
    }
    
    return render(request, "pages/index.html", context)


def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')


def oferta(request):
    return render(request, 'pages/oferta.html')


def free_lesson(request):
    return render(request, 'pages/free-lesson.html')


def reviews(request):
    return render(request, 'pages/reviews.html', {
        'video_reviews': VideoReview.objects.filter(is_active=True),
        'reviews': Review.objects.filter(is_active=True),
    })


def teachers(request):
    return render(request, 'pages/teachers.html')


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