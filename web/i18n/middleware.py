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
                'http://',
                language,
                '.',
                settings.BASE_DOMAIN,
                request.path,
                querystring
            ])
        )

    def process_request(self, request):
        host = request.get_host().split('.')
        language = host[0]

        if language not in self.LANGUAGES:
            return self.redirect_homepage(request)

        translation.activate(language)
        request.LANGUAGE_CODE = language
