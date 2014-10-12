from django.contrib import admin

from premises.models import Contention, Premise, Comment


admin.site.register(Contention)
admin.site.register(Premise)
admin.site.register(Comment)
