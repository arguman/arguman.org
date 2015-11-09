from django.conf import settings


def normalize_language_code(code):
    mapping = settings.LANGUAGE_CODE_MAPPING_REVERSED
    return mapping.get(code.lower(), code)
