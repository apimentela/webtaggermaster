# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
import logging
import subprocess
from django.db import models
from django.conf import settings
from django.db.models.signals import (post_save, pre_save)
from django.dispatch import receiver
from utils.funciones import (acomodaTexto, marcarConsiderandos,
                             limpiarTexto, restaurarNumeros,
                             convertir_texto_a_bd, dar_formato_a_texto)
from django.contrib.postgres import fields
class Leyes(models.Model):
    nombre_oficial = models.CharField(unique=True,max_length=60, blank=False, null=False,verbose_name="Nombre Oficial")
    identificador = models.CharField(unique=True,max_length=60, blank=False, null=False,verbose_name="Identificador")
    fecha_publicacion = models.DateField(null=False, blank=False, verbose_name="Fecha de publicación")
    fecha_ultima_modificacion = models.DateField(null=False, blank=False, verbose_name="Fecha de última modificación")
    capturador = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name='ley',verbose_name="Usuario encargado de captura")
    captura_parrafos_finalizada = models.BooleanField(default=False, verbose_name="Captura finalizada?")
    visible_anotadores = models.BooleanField(default=True,verbose_name="Visible para anotadores?")
    archivo_docx = models.FileField(upload_to='media/DOCXs',null=False, blank=False,verbose_name="Archivo DOCX")
    archivo_pdf = models.FileField(upload_to='media/PDFs',null=False, blank=False,verbose_name="Archivo PDF")
    def __str__ (self):
        return self.identificador
class Parrafos(models.Model):
    ley = models.ForeignKey(Leyes,on_delete=models.CASCADE,related_name='parrafo',null=False,blank=False,verbose_name="Ley")
    capturador = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=False,on_delete=models.SET_NULL,related_name='parrafo',verbose_name="Usuario encargado de captura")
    titulo = models.CharField(max_length=60, blank=False, null=False,verbose_name="Título")
    capitulo = models.CharField(max_length=60, blank=False, null=False,verbose_name="Capítulo")
    base = models.CharField(max_length=60, blank=False, null=False,verbose_name="Base")
    apartado = models.CharField(max_length=60, blank=False, null=False,verbose_name="Apartado")
    articulo = models.CharField(max_length=60, blank=False, null=False,verbose_name="Artículo")
    fraccion = models.CharField(max_length=60, blank=False, null=False,verbose_name="Fracción")
    inciso = models.CharField(max_length=60, blank=False, null=False,verbose_name="Inciso")
    parrafo = models.PositiveIntegerField(blank=False, null=False,verbose_name="Número de Párrafo")
    texto = models.TextField(max_length=100000, blank=False, null=False,verbose_name="Texto")
    fecha_registro = models.DateTimeField(null=False, blank=False,verbose_name="Fecha de registro")
    fecha_ultima_anotacion = models.DateTimeField(null=True, blank=True,verbose_name="Fecha de última anotación")
    class Meta:
        unique_together=(("ley","titulo","capitulo","base","apartado","apartado","fraccion","inciso","parrafo"),)
    def __str__ (self):
        return self.ley.identificador+"_"+str(self.parrafo)
class Etiquetas(models.Model):
    etiqueta = models.CharField(unique=True,max_length=60, blank=False, null=False,verbose_name="Etiqueta")
    descripcion = models.TextField(max_length=3000, blank=False, null=False,verbose_name="Descripción")
    ejemplos = models.TextField(max_length=3000, blank=False, null=False,verbose_name="Ejemplos")
    visible_anotadores = models.BooleanField(default=True,verbose_name="Visible para anotadores?")
    propuesta = models.BooleanField(default=False,verbose_name="Etiqueta propuesta?")
    propuesta_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,default=None,on_delete=models.SET_NULL,related_name='propuestas',verbose_name="Propuesta por usuario")
    def __str__ (self):
        return self.etiqueta
class Etiquetado(models.Model):
    etiqueta_asignada = models.ForeignKey(Etiquetas,null=False,blank=False,on_delete=models.CASCADE,related_name='etiquetado',verbose_name="Etiqueta asignada")
    fecha_etiquetado = models.DateTimeField(auto_now=True,verbose_name="Fecha de etiquetado")
    def __str__ (self):
        return "Etiquetado_"+str(self.pk)
class Anotaciones(models.Model):
    anotador = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name='anotacion',verbose_name="Usuario anotador")
    parrafo = models.ForeignKey(Parrafos,unique=True,null=False,blank=False,on_delete=models.CASCADE,related_name='anotacion',verbose_name="Párrafo")
    anotacion_finalizada = models.BooleanField(default=False,verbose_name="Anotación finalizada?")
    def __str__ (self):
        return "Anotacion_"+self.parrafo.ley.identificador+"_"+str(self.parrafo.parrafo)
class Palabras(models.Model):
    grupo = models.ForeignKey(Etiquetado,null=True,blank=True,on_delete=models.SET_NULL,related_name='grupo',verbose_name="Grupo etiquetada")
    anotacion = models.ForeignKey(Anotaciones,null=False,blank=False,on_delete=models.CASCADE,related_name='palabras',verbose_name="Anotación")
    num_palabra = models.PositiveIntegerField(blank=False, null=False,verbose_name="Número de palabra")
    palabra = models.CharField(max_length=60, blank=False, null=False,verbose_name="Palabra")
    class Meta:
        unique_together=(("anotacion","num_palabra"),)
    def __str__ (self):
        return self.anotacion.parrafo.ley.identificador+"_"+str(self.anotacion.parrafo.parrafo)+"_"+str(self.num_palabra)
class Revisiones(models.Model):
    etiquetado = models.ForeignKey(Etiquetado,null=False,blank=False,on_delete=models.CASCADE,related_name='revision',verbose_name="Etiquetado")
    revisor = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name='revision',verbose_name="Usuario revisor")
    acuerdo = models.NullBooleanField(null=True,blank=False,verbose_name="De acuerdo con el etiquetado?")
    revision_finalizada = models.BooleanField(default=False,verbose_name="Revisión finalizada?")
    fecha_revision = models.DateTimeField(null=True, blank=True,verbose_name="Fecha de revision")
    class Meta:
        unique_together=(("etiquetado","revisor"),)
    def __str__ (self):
        return "Revision_"+str(self.pk)
logger = logging.getLogger('modelos')
def get_documento_path(instance, filename):
    return 'documentos/{0}'.format(filename)
class Documento(models.Model):
    tipo_asunto = models.CharField(max_length=60, blank=True, default="")
    materia = models.CharField(max_length=60, blank=True, default="")
    organo_jurisdiccional = models.CharField(max_length=60, blank=True, default="")
    texto_html = models.TextField(max_length=300000, blank=True,
                                  null=True, default="")
    archivo = models.FileField(upload_to=get_documento_path)
    juez = models.CharField(max_length=80, blank=True, default="")
    secretario = models.CharField(max_length=80, blank=True, default="")
    preambulo = models.CharField(max_length=80, blank=True, default="")
    resultandos = models.CharField(max_length=80, blank=True, default="")
    considerandos = models.CharField(max_length=80, blank=True, default="")
    puntos_resolutivos = models.CharField(max_length=80, blank=True, default="")
    nombre_publico = models.CharField(max_length=60, blank=True, default="")
    def __str__(self):
        return "Documento {0} - {1}".format(self.id, self.archivo)
    def get_path(self):
        return self.archivo.url
    def crear_parrafo(self, numero_inicial, numero_final, parrafo_actual):
        Parrafo.objects.create(documento=self, numero_inicial=numero_inicial,
                               numero_final=numero_final,texto=parrafo_actual,
                               tipo='inicio')
        try:
            DummyParrafo.objects.create(
                texto={'1':'hola',
                       '2':'nanoz'}
            )
        except Exception as e:
            print("fallo tercero dummy ")
            print(e)
    def get_siguiente_parrafo(self):
        return self.parrafo.exclude(ha_sido_evaluado=True).first()
    def get_dummy_parrafo(self):
        return DummyParrafo.objects.first()
class Parrafo(models.Model):
    documento = models.ForeignKey(Documento, related_name='parrafo')
    numero_inicial=models.IntegerField(blank=True, null=True,
        help_text="Indice de inicio delas palabras")
    numero_final = models.IntegerField(blank=True, null=True,
        help_text="Indice de inicio delas palabras")
    texto = fields.JSONField()
    ha_sido_evaluado = models.BooleanField(
        help_text='Marcar cuando un parrafo ya ha sido evaluado',
        default=False)
    tipo = models.CharField(
        help_text="Saber si es considerando, resultando, resuelve, etc.",
        max_length=40, blank=True, null=True)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return "{0}: {1} {2}".format(self.id, self.numero_inicial, self.numero_final)
    def get_next_parrafo(self):
        return Parrafo.objects.filter(id__gt=self.id, documento=self.documento).first()
    def get_prev_parrafo(self):
        return Parrafo.objects.filter(id__lt=self.id, documento=self.documento).last()
class DummyParrafo(models.Model):
    texto = fields.JSONField()
class Anotacion(models.Model):
    documento = models.ForeignKey(Documento,
                                related_name='anotacion')
    revisor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='revisor')
    anotador = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='anotador')
    is_done = models.BooleanField(default=False)
    def __str__(self):
        return "Anotacion {0} - {1}".format(self.id, self.documento)
    def get_url_file(self):
        return self.documento.get_path()
    def get_texto(self):
        return self.documento.texto_html
    def set_texto(self, texto):
        self.documento.texto_html = texto
    def save_documento(self):
        self.documento.save()
class Clasificacion(models.Model):
    key = models.CharField(max_length=60, blank=True,
                             null=True, default="")
    nombre_publico = models.CharField(max_length=60, blank=True,
                                      null=True, default="")
    def __str__(self):
        return "{0}".format(self.key)
class TAG(models.Model):
    texto = models.CharField(max_length=1000, blank=True,
                             null=True, default="")
    is_active = models.BooleanField(default=True)
    subtag = models.ForeignKey('self', blank=True, null=True)
    def __str__(self):
        return "{0}".format(self.texto).encode('utf-8')
    def as_dict(self):
        return {"key": self.id, "value": self.texto}
        return "{0} - {1}".format(self.autor, self.calificacion)
class Oracion(models.Model):
    tags = models.ManyToManyField(TAG, related_name='oraciones', null=True, blank=True)
    clasificacion = models.ForeignKey(Clasificacion)
    anotacion = models.ForeignKey(Anotacion, related_name='oraciones')
    parrafo = models.ForeignKey(Parrafo, related_name='oraciones')
    tipo_anotacion = models.CharField(max_length=100, blank=True,
                                      null=True, default="")
    texto = models.CharField(max_length=2000, blank=True,
                             null=True, default="")
    evaluado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE,
                                     related_name='etiquetador')
    is_correcta = models.BooleanField(default=True)
    def __str__(self):
        return "Oracion {0}".format(self.id)
    def __unicode__(self):
        return u"Oracion {0}".format(self.id)
class EstadoEtiquetado(object):
    pass
class EvaluacionParrafo(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='evaluacion_parrado')
    oracion = models.ForeignKey(Oracion, related_name='evaluacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True,
                                          verbose_name='Fecha de creacion/actualizacion de la oracion')
    tags = models.ManyToManyField(TAG, related_name='tags_evaluacion', null=True, blank=True)
    tipo_anotacion = models.CharField(max_length=100, blank=True,
                                      null=True, default="")
    texto = models.CharField(max_length=2000, blank=True,
                             null=True, default="")
    clasificacion = models.ForeignKey(Clasificacion)
    def __str__(self):
        return "{0} - {1}".format(self.autor, self.clasificacion)
class ArgumentacionParrafo(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name='argumento')
    parrafo = models.OneToOneField(Parrafo, related_name='argumentacion')
    calificacion = models.PositiveSmallIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True,
                                          verbose_name='Fecha de la evaluacion')
    def __str__(self):
        return "{0} - {1}".format(self.autor, self.calificacion)
class TAGPersonal(models.Model):
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name='tags')
    tag = models.ForeignKey(TAG)
    alias = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return "{0} - {1}".format(self.id, self.alias)
    pass
@receiver(post_save, sender=Documento)
def crear_ticket_cepra(sender, **kwargs):
    if kwargs['created']:
        logger.debug("Documento guardado, procedemos a guardar informacion")
        filepath =  kwargs['instance'].get_path()
        _path_ = filepath.split('/')
        print(os.getcwd())
        root_path = os.getcwd() + "/".join(_path_[:len(_path_)-1])
        filepath_prov = os.path.join(root_path, _path_[-1].
                                     replace('.PDF','.txt').replace('.pdf','.txt'))
        print("PATHS: ")
        print(filepath)
        print(_path_)
        print(filepath_prov)
        command = ["pdftotext", "-layout", "-raw", "-q",
                   os.getcwd()+filepath, filepath_prov
                   ]
        print(" ".join(command))
        proceso = subprocess.Popen(command, stdout=subprocess.PIPE)
        exit_code = proceso.wait()
        print(exit_code)
        texto = dar_formato_a_texto(filepath_prov, new_path=None)
        print("termino de dar formato...")
        all_words = convertir_texto_a_bd(texto, kwargs['instance'])
    else:
        pass
