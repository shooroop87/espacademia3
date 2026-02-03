from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Property, PropertyType, Location


def property_list(request):
    properties = Property.objects.filter(is_active=True).select_related(
        'developer', 'property_type', 'location'
    )
    
    # Фильтры
    q = request.GET.get('q')
    if q:
        properties = properties.filter(name__icontains=q)
    
    location_slug = request.GET.get('location')
    if location_slug:
        properties = properties.filter(location__slug=location_slug)
    
    type_slug = request.GET.get('type')
    if type_slug:
        properties = properties.filter(property_type__slug=type_slug)
    
    rooms = request.GET.get('rooms')
    if rooms:
        if rooms == '3':
            properties = properties.filter(rooms__gte=3)
        else:
            properties = properties.filter(rooms=rooms)
    
    # Пагинация
    paginator = Paginator(properties, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'properties': page_obj,
        'page_obj': page_obj,
        'locations': Location.objects.all(),
        'property_types': PropertyType.objects.all(),
        'current_location': Location.objects.filter(slug=location_slug).first() if location_slug else None,
        'current_type': PropertyType.objects.filter(slug=type_slug).first() if type_slug else None,
    }
    
    return render(request, 'property/property_list.html', context)


def property_detail(request, slug):
    property = get_object_or_404(Property, slug=slug, is_active=True)
    similar = Property.objects.filter(
        location=property.location, is_active=True
    ).exclude(pk=property.pk)[:4]
    
    return render(request, 'property/property_details2.html', {
        'property': property,
        'similar_properties': similar,
    })