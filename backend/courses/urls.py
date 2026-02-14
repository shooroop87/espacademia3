from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('online-kurs-razgovornogo-ispanskogo-espanol-activo/', views.espanol_activo, name='espanol_activo'),
    path('online-kurs-razgovornogo-ispanskogo-espanol-activo-intensivo/', views.espanol_activo_intensivo, name='espanol_activo_intensivo'),
    path('razgovornyj-onlajn-klub-s-nositelem/', views.club_con_nositelem, name='club_con_nositelem'),
    path('kursy-ispanskogo-yazyka-dlya-detej/', views.kursy_dlya_detej, name='kursy_dlya_detej'),
    path('individualnye-zanyatiya-po-izucheniyu-ispanskogo-yazyka/', views.individualnye_zanyatiya, name='individualnye_zanyatiya'),
    path('podgotovka-k-ekzamenu-dele/', views.podgotovka_dele, name='podgotovka_dele'),
]