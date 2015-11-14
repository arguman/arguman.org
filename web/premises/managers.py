from django.db import models
from django.db.models import query
from datetime import datetime
from django.utils.translation import get_language

from i18n.utils import normalize_language_code


class DeletePreventionQueryset(query.QuerySet):
    def delete(self):
        return super(DeletePreventionQueryset, self).update(
            is_deleted=True, deleted_at=datetime.now())

    def hard_delete(self):
        return super(DeletePreventionQueryset, self).delete()


class DeletePreventionManager(models.Manager):

    def get_queryset(self):
        queryset = DeletePreventionQueryset(self.model, using=self._db)
        return queryset.filter(is_deleted=False)

    def deleted_set(self):
        queryset = DeletePreventionQueryset(self.model, using=self._db)
        return queryset.filter(is_deleted=True)

    def all_with_deleted(self):
        return DeletePreventionQueryset(self.model, using=self._db)


class LanguageManager(DeletePreventionManager):
    def language(self, language_code=None):
        if language_code is None:
            language_code = get_language()
        language_code = normalize_language_code(language_code)
        return self.filter(language=language_code)
