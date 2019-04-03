from __future__ import unicode_literals
from django.db import models
from django.conf import settings
class Sesiones(models.Model):
    usuario=models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="Usuario",related_name="Sesiones")
    inicio=models.DateTimeField(verbose_name="Inicio")
    fin=models.DateTimeField(verbose_name="Fin",null=True)
    class Meta:
        unique_together=(("usuario","inicio"),)
