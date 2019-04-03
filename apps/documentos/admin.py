from django.contrib import admin
from .models import (Leyes,Parrafos,Etiquetas,Etiquetado,Anotaciones,
					Palabras,Revisiones)
class LeyesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Leyes, LeyesAdmin)
class ParrafosAdmin(admin.ModelAdmin):
    pass
admin.site.register(Parrafos, ParrafosAdmin)
class EtiquetasAdmin(admin.ModelAdmin):
    pass
admin.site.register(Etiquetas, EtiquetasAdmin)
class EtiquetadoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Etiquetado, EtiquetadoAdmin)
class AnotacionesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Anotaciones, AnotacionesAdmin)
class PalabrasAdmin(admin.ModelAdmin):
    pass
admin.site.register(Palabras, PalabrasAdmin)
class RevisionesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Revisiones, RevisionesAdmin)
