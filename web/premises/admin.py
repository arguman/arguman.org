from django.contrib import admin
from django.db import models
from django.db.models import Count
from django.forms import Textarea

from premises.models import Contention, Premise, Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'premise', 'contention')


class PremiseInline(admin.TabularInline):
    model = Premise
    extra = 0
    fields = ('user', 'premise_type',
              'text', 'sources', 'is_approved')
    fk_name = "argument"
    raw_id_fields = ('user', )
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(
                attrs={'rows': 2, 'cols': 40}
            )},
    }


class ContentionAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'is_featured',
                    'is_published', 'premise_count')
    list_editable = ('language', 'is_featured',)
    search_fields = ('title', 'nouns__text')
    list_per_page = 100
    list_filter = ('language', 'is_featured',)
    filter_horizontal = ('nouns', 'related_nouns')
    inlines = [PremiseInline]

    def premise_count(self, obj):
        return obj.premises.count()


class PremiseAdmin(admin.ModelAdmin):
    list_display = ('text', 'argument', 'is_deleted')
    list_filter = ('is_deleted',)

    def get_queryset(self, request):
        return Premise.objects.all_with_deleted()


admin.site.register(Report, ReportAdmin)
admin.site.register(Contention, ContentionAdmin)
admin.site.register(Premise, PremiseAdmin)

