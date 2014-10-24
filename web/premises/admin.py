from django.contrib import admin

from premises.models import Contention, Premise, Comment, Vote


class PremiseAdmin(admin.ModelAdmin):
    list_display = ("text", "like_count", "unlike_count")


admin.site.register(Contention)
admin.site.register(Premise, PremiseAdmin)
admin.site.register(Comment)
admin.site.register(Vote)
