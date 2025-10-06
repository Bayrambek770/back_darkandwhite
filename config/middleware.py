from django.utils import translation


class QueryOrHeaderLocaleMiddleware:
    """Set language from ?lang= or Accept-Language header, default to ru.
    Should be placed before LocaleMiddleware if used.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.GET.get('lang')
        if not lang:
            header = request.META.get('HTTP_ACCEPT_LANGUAGE')
            if header:
                lang = header.split(',')[0].split(';')[0].strip()
        if not lang:
            lang = 'ru'
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        response = self.get_response(request)
        translation.deactivate()
        return response
