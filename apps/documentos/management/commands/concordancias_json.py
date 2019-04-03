from __future__ import unicode_literals
from __future__ import division
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from ...models import (Etiquetado,Etiquetas,Revisiones)
from django.db.models import Q
from datetime import datetime
import json
import os
class Command(BaseCommand):
    help = 'Agrega valores de concordacias al json de media'
    def handle(self, *args, **options):
        now=datetime.now().strftime("%Y-%m-%d")
        diccionario={}
        diccionario[now]=[]
        usuarios=[i for i in User.objects.all()]
        for i1 in range(len(usuarios)):
            usuario1=usuarios[i1]
            etiquetados1=Etiquetado.objects.filter(grupo__anotacion__anotador=usuario1).distinct()
            cuenta_etiquetados1=etiquetados1.count()
            for i2 in range(i1+1,len(usuarios)):
                usuario2=usuarios[i2]
                etiquetados2=Etiquetado.objects.filter(grupo__anotacion__anotador=usuario2).distinct()
                cuenta_etiquetados2=etiquetados2.count()
                revisiones1=Revisiones.objects.filter(revisor=usuario1,revision_finalizada=True,etiquetado__in=etiquetados2)
                revisiones2=Revisiones.objects.filter(revisor=usuario2,revision_finalizada=True,etiquetado__in=etiquetados1)
                etiquetas=Etiquetas.objects.filter( Q(etiquetado__in=etiquetados1) | Q(etiquetado__in=etiquetados2) ).distinct()
                try:
                    pr_acuerdo=( revisiones1.filter(acuerdo=True).count() + revisiones2.filter(acuerdo=True).count() ) / ( revisiones1.count() + revisiones2.count() )
                except ZeroDivisionError:
                    continue
                pr_azar=0
                for etiqueta in etiquetas:
                    try:
                        pr_e1=( etiquetados1.filter(etiqueta_asignada=etiqueta).count() ) / ( cuenta_etiquetados1 )
                    except ZeroDivisionError:
                        continue
                    try:
                        pr_e2=( etiquetados2.filter(etiqueta_asignada=etiqueta).count() ) / ( cuenta_etiquetados2 )
                    except ZeroDivisionError:
                        continue
                    pr_azar+=pr_e1*pr_e2
                kappa=( pr_acuerdo - pr_azar ) / ( 1 - pr_azar )
                diccionario[now].append({'usuarioA':usuario1.username,'usuarioB':usuario2.username,'coeficiente':kappa})
        with open(os.path.join(os.path.dirname(__file__),'../../../../media/concordancia_diaria'), 'a') as fout:
            json.dump(diccionario, fout)
            fout.write("\n")
