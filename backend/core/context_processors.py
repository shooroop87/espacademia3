from .models import SiteSettings, CodeSnippet


def site_settings(request):
    """Добавляет настройки сайта и сниппеты во все шаблоны"""
    try:
        snippets = CodeSnippet.objects.filter(is_active=True)
        snippets_head = list(snippets.filter(location='head'))
        snippets_body_start = list(snippets.filter(location='body_start'))
        snippets_body_end = list(snippets.filter(location='body_end'))
    except Exception:
        snippets_head = []
        snippets_body_start = []
        snippets_body_end = []
    
    return {
        'settings': SiteSettings.get(),
        'snippets_head': snippets_head,
        'snippets_body_start': snippets_body_start,
        'snippets_body_end': snippets_body_end,
    }