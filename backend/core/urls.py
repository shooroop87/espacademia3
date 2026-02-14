from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('contact/', views.contact_request, name='contact_request'),
    path('reviews/', views.reviews, name='reviews'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('oferta/', views.oferta, name='oferta'),
    path('teachers/', views.teachers, name='teachers'),
    path('free-lesson/', views.free_lesson, name='free_lesson'),
]