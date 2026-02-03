from django.shortcuts import render, get_object_or_404
from .models import Developer, DeveloperCategory, DeveloperReview
from properties.models import Property

def developer_list(request):
    developers = Developer.objects.filter(is_active=True).select_related('category')
    categories = DeveloperCategory.objects.all()
    
    # Фильтр по категории
    category_slug = request.GET.get('category')
    if category_slug:
        developers = developers.filter(category__slug=category_slug)
    
    return render(request, 'developers/developer_list.html', {
        'developers': developers,
        'categories': categories,
        'current_category': category_slug,
    })


def developer_detail(request, slug):
    developer = get_object_or_404(
        Developer.objects.prefetch_related('highlights'),
        slug=slug,
        is_active=True
    )
    
    # Объекты застройщика
    properties = Property.objects.filter(
        developer=developer, is_active=True
    ).select_related('property_type', 'location')[:6]
    
    # Статистика
    completed_count = Property.objects.filter(
        developer=developer, construction_status='completed'
    ).count()
    in_progress_count = Property.objects.filter(
        developer=developer, construction_status='in_progress'
    ).count()
    total_count = Property.objects.filter(developer=developer).count()
    
    # Отзывы только этого застройщика
    reviews = DeveloperReview.objects.filter(
        developer=developer, is_approved=True
    ).order_by('-created_at')[:10]
    
    context = {
        'developer': developer,
        'properties': properties,
        'reviews': reviews,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'total_count': total_count,
    }
    
    return render(request, 'developers/developer_detail.html', context)