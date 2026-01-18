from .models import SiteSettings, CodeSnippet


def site_settings(request):
    return {
        'site_settings': SiteSettings.get()
    }

def code_snippets(request):
    """Добавляет сниппеты кода в контекст."""
    snippets = CodeSnippet.objects.filter(is_active=True)
    return {
        'snippets_head': snippets.filter(location='head'),
        'snippets_body_start': snippets.filter(location='body_start'),
        'snippets_body_end': snippets.filter(location='body_end'),
    }
