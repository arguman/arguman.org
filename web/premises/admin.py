from django.contrib import admin

from premises.models import Contention, Premise, Comment, Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'premise', 'contention')


class ContentionAdmin(admin.ModelAdmin):
    list_filter = ('is_deleted',)

admin.site.register(Report, ReportAdmin)
admin.site.register(Contention, ContentionAdmin)
admin.site.register(Premise)
admin.site.register(Comment)
