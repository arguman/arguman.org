from . import DeletePreventionManager

from django.utils.translation import get_language


class ContentionManager(DeletePreventionManager):
    def language(self, language_code=None):
        if language_code is None:
            language_code = get_language()
        return self.filter(language=language_code)