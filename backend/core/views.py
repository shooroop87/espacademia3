from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from django.db.models import Prefetch

from events.models import Event
from .models import Video, FAQ, SiteSettings, Banner, Partner

from django.views.decorators.http import require_POST


def index(request):
    """Главная страница."""
    
    # Настройки сайта
    settings = SiteSettings.get()

    # Мероприятия
    upcoming_events = Event.objects.filter(status='upcoming').order_by('event_date')[:2]

    # FAQ
    faqs = FAQ.objects.filter(is_active=True)
    
    context = {
        'settings': settings,
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