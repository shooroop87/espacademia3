from django.shortcuts import render
from core.models import VideoReview, Review
from django.db.models import Q


def get_course_context(course_type):
    return {
        'video_reviews': VideoReview.objects.filter(is_active=True).filter(Q(course_type=course_type) | Q(course_type='all')),
        'reviews': Review.objects.filter(is_active=True)[:10],
    }


def espanol_activo(request):
    return render(request, 'pages/course-activo.html', get_course_context('activo'))


def espanol_activo_intensivo(request):
    return render(request, 'pages/course-activo-intensivo.html', get_course_context('intensivo'))


def club_con_nositelem(request):
    return render(request, 'pages/course-club.html', get_course_context('club'))


def kursy_dlya_detej(request):
    return render(request, 'pages/course-kids.html', get_course_context('kids'))


def individualnye_zanyatiya(request):
    return render(request, 'pages/course-individual.html', get_course_context('individual'))


def podgotovka_dele(request):
    return render(request, 'pages/course-dele.html', get_course_context('dele'))