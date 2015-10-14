from django.contrib import admin
from django.db.models import Count

from premises.models import Contention, Premise, Comment, Report, Channel


class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'premise', 'contention')


class ContentionAdmin(admin.ModelAdmin):
    list_display = ('title', 'channel', 'is_featured', 
    				'is_published', 'premise_count')
    list_editable = ('channel', 'is_featured', )
    search_fields = ('title', )
    list_per_page = 10

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
admin.site.register(Comment)
admin.site.register(Channel)
