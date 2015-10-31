from django.utils import translation
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.translation import get_language_from_request


class SubdomainLanguageMiddleware(object):
    """
    Set the language for the site based on the subdomain the request
    is being served on. For example, serving on 'fr.domain.com' would
    make the language French (fr).
    """
    LANGUAGES = settings.AVAILABLE_LANGUAGES

    def redirect_homepage(self, request):
        if request.path not in settings.REDIRECTED_PATHS:
            return

        language = get_language_from_request(request)

        if language not in self.LANGUAGES:
            language = settings.DEFAULT_LANGUAGE

        querystring = request.META.get('QUERY_STRING', '')
        if querystring:
            querystring = '?' + querystring

        return HttpResponseRedirect(
            ''.join([
                'http://', language, '.', settings.BASE_DOMAIN,
                request.path, querystring
            ])
        )

    def get_language_code(self, code):
        mapping = settings.LANGUAGE_CODE_MAPPING
        return mapping.get(code, code)

    def process_request(self, request):
        host = request.get_host().split('.')
        language = host[0]

        if settings.PREVENT_LANGUAGE_REDIRECTION:
            language = settings.DEFAULT_LANGUAGE
        elif language not in self.LANGUAGES:
            return self.redirect_homepage(request)

        language_code = self.get_language_code(language)

        translation.activate(language_code)
        request.LANGUAGE_CODE = language_code


class MultipleProxyMiddleware(object):
    FORWARDED_FOR_FIELDS = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
    ]

    def process_request(self, request):
        """
        Rewrites the proxy headers so that only the most
        recent proxy is used.
        """
        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META:
                if ',' in request.META[field]:
                    parts = request.META[field].split(',')
                    request.META[field] = parts[-1].strip()
