from django.contrib import admin
from .models import (Sesiones)
class SesionesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Sesiones, SesionesAdmin)
