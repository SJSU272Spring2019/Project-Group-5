from django.contrib import admin
from .models import DeploymentDetail

class DeploymentDetailAdmin(admin.ModelAdmin):
    list_display = ['id']
    readonly_fields = ('id',)


admin.site.register(DeploymentDetail, DeploymentDetailAdmin)

