from django.contrib import admin

from premises.models import Contention, Premise, Comment, Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'premise', 'contention')

admin.site.register(Report, ReportAdmin)
admin.site.register(Contention)
admin.site.register(Premise)
admin.site.register(Comment)
