from django.contrib import admin

from premises.models import Contention, Premise, Comment, Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'premise', 'contention')


class ContentionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_deleted')
    list_filter = ('is_deleted',)

    def get_queryset(self, request):
        return Contention.objects.all_with_deleted()


class PremiseAdmin(admin.ModelAdmin):
    list_display = ('text', 'argument', 'is_deleted')
    list_filter = ('is_deleted',)

    def get_queryset(self, request):
        return Premise.objects.all_with_deleted()

admin.site.register(Report, ReportAdmin)
admin.site.register(Contention, ContentionAdmin)
admin.site.register(Premise, PremiseAdmin)
admin.site.register(Comment)
