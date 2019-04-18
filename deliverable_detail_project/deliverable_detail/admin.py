from django.contrib import admin
from .models import Deliverable


class DeliverableAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Deliverable, DeliverableAdmin)