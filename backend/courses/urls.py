from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('online-kurs-razgovornogo-ispanskogo-espanol-activo/', views.contact_request, name='contact_request'),
]