# -*- coding: utf-8 -*-
from __future__ import division
import json, random
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import HiddenInput
from django.contrib import messages
from django.http import (HttpResponse)
from django.shortcuts import (render, get_object_or_404, redirect)
from django.core.urlresolvers import (reverse)
from django.views.decorators.csrf import (csrf_exempt)
from django.contrib.auth.decorators import login_required , user_passes_test
from django.utils.encoding import (smart_unicode)
from django.db.models import Q 
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from rest_framework import (viewsets)
from rest_framework.response import (Response)
from rest_framework import (status)
from .tests import en_grupo_administradores
from ..registro.models import Sesiones
from .models import (Anotacion, Documento, Parrafo, Oracion, TAG,
                     EvaluacionParrafo, Clasificacion, TAGPersonal,
                     ArgumentacionParrafo, 
                     Leyes,Parrafos,Anotaciones,Palabras,Etiquetas,Etiquetado,Revisiones
                     )
from .forms import (DocumentoForm)
from .serializers import (OracionSerializer, ParrafoSerializer,
                          TAGLeyesSerializer, AnotacionSerializer,
                          ArgumentacionParrafoSerializer, TAGPersonalSerializer)
class asigna_anotaciones_Bloque_Form(forms.Form):
    anotador = forms.ModelChoiceField(label="Anotador",
                queryset=User.objects.all())
@login_required
@user_passes_test(en_grupo_administradores, login_url='/acceso_denegado/')
def asigna_anotaciones_Bloque(request,pk):
    if request.POST:
        form=asigna_anotaciones_Bloque_Form(request.POST)
        if form.is_valid():
            anotador=form.cleaned_data["anotador"]
            parrafos=Parrafos.objects.filter(ley=pk)
            for parrafo in parrafos:
                nueva_anotacion=Anotaciones(anotador=anotador,
                                            parrafo=parrafo)
                nueva_anotacion.save()
                palabras=parrafo.texto.split()
                for numero,palabra in enumerate(palabras,1): 
                    nueva_palabra=Palabras(anotacion=nueva_anotacion,
                                            num_palabra=numero,
                                            palabra=palabra)
                    nueva_palabra.save()
            messages.success(request, 'Bloque asignado')
            return redirect(reverse('documentos_app:asigna_anotacion_leyes'))
        else:
            return render(request, 'documentos/asigna_anotaciones_Bloque.html',{'form':form})
    else:
        form=asigna_anotaciones_Bloque_Form()
        return render(request, 'documentos/asigna_anotaciones_Bloque.html',{'form':form})
class asigna_Anotacion_Form(forms.Form):
    def __init__(self, *args, **kwargs):
        ley=kwargs.pop('ley')
        super(asigna_Anotacion_Form, self).__init__(*args, **kwargs)
        self.fields['parrafos'].queryset = Parrafos.objects.filter(ley=ley,anotacion=None)
    anotador = forms.ModelChoiceField(label="Anotador",
                queryset=User.objects.all())
    parrafos = forms.ModelMultipleChoiceField(label="Parrafos",widget=forms.CheckboxSelectMultiple,
                                            queryset=Parrafos.objects.none()) 
@login_required
@user_passes_test(en_grupo_administradores, login_url='/acceso_denegado/')
def asigna_Anotacion(request,pk):
    try:
        ley=Leyes.objects.get(pk=pk)
    except Leyes.DoesNotExist:
        return HttpResponse("ERROR, la dirección no es válida")
    if request.POST:
        form=asigna_Anotacion_Form(request.POST,ley=pk)
        if form.is_valid():
            anotador=form.cleaned_data["anotador"]
            parrafos=form.cleaned_data["parrafos"]
            for parrafo in parrafos:
                nueva_anotacion=Anotaciones(anotador=anotador,
                                            parrafo=parrafo)
                nueva_anotacion.save()
                palabras=parrafo.texto.split()
                for numero,palabra in enumerate(palabras,1): 
                    nueva_palabra=Palabras(anotacion=nueva_anotacion,
                                            num_palabra=numero,
                                            palabra=palabra)
                    nueva_palabra.save()
            messages.success(request, 'Parrafos asignados')
            return redirect(reverse('documentos_app:asigna_anotacion_ley',args=(pk,)))
        else:
            return render(request, 'documentos/asigna_anotacion_ley.html',{'form':form})
    else:
        form=asigna_Anotacion_Form(ley=pk)
        return render(request, 'documentos/asigna_anotacion_ley.html',{'form':form})
class anotacion_Parrafo_Form(forms.Form):
    def __init__(self, *args, **kwargs):
        usuario=kwargs.pop('usuario')
        super(anotacion_Parrafo_Form, self).__init__(*args, **kwargs)
        self.fields['etiqueta'].queryset = Etiquetas.objects.filter(Q(visible_anotadores=True) & ( Q(propuesta=False) | Q(propuesta_por=usuario) ) )
    modo_texto=forms.BooleanField(widget=forms.HiddenInput(attrs={'id':'boton_texto'}),required=False)
    modo_botones=forms.BooleanField(widget=forms.HiddenInput(attrs={'id':'boton_botones'}),required=False)
    palabra_inicial=forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'palabra_inicial'}),required=False) 
    palabra_final=forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'palabra_final'}),required=False)
    etiqueta = forms.ModelChoiceField(label="Etiqueta",
                queryset=Etiquetas.objects.none()) 
@login_required
def anotacion_Parrafo(request,pk):
    try:
        anotacion=Anotaciones.objects.get(parrafo=pk,anotador=request.user)
        parrafo=Parrafos.objects.get(pk=pk)
        etiquetas=Etiquetas.objects.all()
    except Anotaciones.DoesNotExist:
        return redirect('/acceso_denegado/')
    if request.POST:
        palabras=Palabras.objects.filter(anotacion=anotacion).order_by('num_palabra')
        form=anotacion_Parrafo_Form(request.POST,usuario=request.user)
        modo_texto=int(form.data['modo_texto'])
        modo_botones=int(form.data['modo_botones'])
        print(modo_texto)
        print(modo_botones)
        if modo_texto:
            modo="modo_texto"
            no_modo="modo_botones"
            print("modo texto")
        elif modo_botones:
            modo="modo_botones"
            no_modo="modo_texto"
            print("modo botones")
        else: return render(request, 'documentos/anotacion_parrafo.html',{'form':form,'anotacion':anotacion,'palabras':palabras,'etiquetas':etiquetas,'modo_texto':False,'modo_botones':False})
        if form.is_valid():
            etiqueta=form.cleaned_data["etiqueta"]
            palabra_inicial=form.cleaned_data["palabra_inicial"]
            palabra_final=form.cleaned_data["palabra_final"]
            palabras_checked = request.POST.getlist('palabras_checked')
            if not ( palabra_inicial and palabra_final ) and not palabras_checked: 
                messages.error(request,"Se deben seleccionar palabras para hacer el etiquetado")
                return render(request, 'documentos/anotacion_parrafo.html',{'form':form,'anotacion':anotacion,'palabras':palabras,'etiquetas':etiquetas,modo:True,no_modo:False})
            if palabras_checked: 
                nuevo_grupo=Etiquetado(etiqueta_asignada=etiqueta)
                nuevo_grupo.save()
                for num_palabra in palabras_checked:
                    palabra=Palabras.objects.get(anotacion=anotacion,num_palabra=num_palabra)
                    palabra.grupo=nuevo_grupo
                    palabra.save()
                if not anotacion.anotacion_finalizada:
                    anotacion.anotacion_finalizada=True
                    anotacion.save()
                parrafo.fecha_ultima_anotacion = make_aware(datetime.now())
                parrafo.save()
                messages.success(request, 'Etiquetado guardado')
                return redirect(reverse('documentos_app:anota_parrafo',args=(pk,)))
            if palabra_inicial and palabra_final: 
                nuevo_grupo=Etiquetado(etiqueta_asignada=etiqueta)
                nuevo_grupo.save()
                for num_palabra in range(palabra_inicial,palabra_final+1):
                    palabra=Palabras.objects.get(anotacion=anotacion,num_palabra=num_palabra)
                    palabra.grupo=nuevo_grupo
                    palabra.save()
                if not anotacion.anotacion_finalizada:
                    anotacion.anotacion_finalizada=True
                    anotacion.save()
                parrafo.fecha_ultima_anotacion = make_aware(datetime.now())
                parrafo.save()
                messages.success(request, 'Etiquetado guardado')
                return redirect(reverse('documentos_app:anota_parrafo',args=(pk,)))
        else:
            messages.info(request,"Favor de llenar los datos para el etiquetado")
            return render(request, 'documentos/anotacion_parrafo.html',{'form':form,'anotacion':anotacion,'palabras':palabras,'etiquetas':etiquetas,modo:True,no_modo:False})
    else:
        print("NO POST")
        form=anotacion_Parrafo_Form(usuario=request.user)
        return render(request, 'documentos/anotacion_parrafo.html',{'form':form,'anotacion':anotacion,'modo_texto':False,'modo_botones':False})
@login_required
@user_passes_test(en_grupo_administradores, login_url='/acceso_denegado/')
def asigna_Revisiones(request):
    return render(request, 'documentos/asigna_revisiones.html')
@login_required
@user_passes_test(en_grupo_administradores, login_url='/acceso_denegado/')
def asigna_Revisiones_Auto(request):
    etiquetados_sinRevision=Etiquetado.objects.filter(revision=None)
    anotadores=User.objects.filter(groups__name="anotadores") 
    if len(anotadores) < 2: return HttpResponse("No es posible asignar automáticamente si solo se tiene un anotador")
    for etiquetado in etiquetados_sinRevision:
        try:
            anotador=User.objects.filter(anotacion__palabras__grupo=etiquetado).distinct().get()
        except:
            continue
        revisor=random.choice(anotadores)
        while anotador == revisor:
            revisor=random.choice(anotadores)
        nueva_revision=Revisiones(etiquetado=etiquetado,revisor=revisor)
        nueva_revision.save()
    messages.success(request, 'Revisiones asignadas')
    return render(request, 'documentos/asigna_revisiones.html')
class asigna_Revision_Form(forms.Form):
    def __init__(self, *args, **kwargs):
        usuario=kwargs.pop('usuario')
        super(asigna_Revision_Form, self).__init__(*args, **kwargs)
        self.fields['revisor'].queryset = User.objects.exclude(pk=usuario.pk)
    revisor = forms.ModelChoiceField(label="Revisor",
                queryset=User.objects.none())
@login_required
@user_passes_test(en_grupo_administradores, login_url='/acceso_denegado/')
def asigna_Revision(request,pk):
    try:
        anotacion=Anotaciones.objects.get(parrafo=pk)
        ley=Leyes.objects.get(parrafo=pk)
        etiquetados=Etiquetado.objects.filter(grupo__anotacion=anotacion).distinct()
    except Anotaciones.DoesNotExist:
        return HttpResponse("ERROR, la dirección no es válida")
    if request.POST:        
        form=asigna_Revision_Form(request.POST,usuario=anotacion.anotador)
        if form.is_valid():
            revisor=form.cleaned_data["revisor"]
            for etiquetado in etiquetados:
                nueva_revision=Revisiones(etiquetado=etiquetado,revisor=revisor)
                nueva_revision.save()
            messages.success(request, 'Revisiones asignadas')
            return redirect(reverse('documentos_app:asigna_revision_ley',args=(ley.pk,)))
        else:
            messages.info(request,"Favor de llenar los datos")
            return render(request, 'documentos/asigna_revision.html',{'form':form})
    else:
        form=asigna_Revision_Form(usuario=anotacion.anotador)
        return render(request, 'documentos/asigna_revision.html',{'form':form})
class revision_Form(forms.Form):
    acuerdo=forms.BooleanField(required=False)
@login_required
def revision(request,pk):
    try:
        revision=Revisiones.objects.get(pk=pk,revisor=request.user)
        anotaciones=Anotaciones.objects.filter(palabras__grupo__revision=revision).distinct()
        anotacion=anotaciones[:1].get()
        palabras=Palabras.objects.filter(anotacion=anotacion).order_by('num_palabra')
    except Revisiones.DoesNotExist:
        return redirect('/acceso_denegado/')
    if request.POST:
        form=revision_Form(request.POST)
        if form.is_valid():
            acuerdo=form.cleaned_data["acuerdo"]
            revision.acuerdo=acuerdo
            revision.revision_finalizada=True
            revision.fecha_revision=make_aware(datetime.now())
            revision.save()
            messages.success(request, 'Revisiones registrada')
            return redirect(reverse('documentos_app:revisa_ley',args=(anotacion.parrafo.ley.pk,)))
        else:
            messages.info(request,"Favor de responder")
            return render(request, 'documentos/revision.html',{'form':form,'palabras':palabras,'anotacion':anotacion,'revision':revision})
    else:
        form=revision_Form()
        return render(request, 'documentos/revision.html',{'form':form,'palabras':palabras,'anotacion':anotacion,'revision':revision})
class estadisticas_Usuario_Form(forms.Form):
    def __init__(self, *args, **kwargs):
        usuario=kwargs.pop('usuario')
        super(estadisticas_Usuario_Form, self).__init__(*args, **kwargs)
        self.fields['revisor'].queryset = User.objects.exclude(pk=usuario.pk)
    revisor = forms.ModelChoiceField(label="Concordancia con",
                queryset=User.objects.none())
@login_required
@user_passes_test(en_grupo_administradores, login_url='/acceso_denegado/')
def estadisticas_Usuario(request,pk):
    try:
        usuario=User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse("ERROR, la dirección no es válida")
    sesiones=Sesiones.objects.filter(usuario=usuario)
    num_sesiones=sesiones.count()
    duracion_sesiones=make_aware(datetime.now())-make_aware(datetime.now()) 
    for sesion in sesiones:
        duracion_sesiones+=sesion.fin-sesion.inicio
    try:
        duracion_promedio=(duracion_sesiones.total_seconds())/num_sesiones
    except:
        duracion_promedio=0
    num_parrafos=Parrafos.objects.filter(capturador=usuario).count()
    num_etiquetados=Etiquetado.objects.filter(grupo__anotacion__anotador=usuario).distinct().count()
    num_revisiones=Revisiones.objects.filter(revisor=usuario,revision_finalizada=True).count()
    if request.POST:
        form=estadisticas_Usuario_Form(request.POST,usuario=usuario)
        if form.is_valid():
            revisor=form.cleaned_data["revisor"]
            return redirect(reverse('documentos_app:concordancia_usuarios',args=(usuario.pk,revisor.pk,)))
        else:
            messages.info(request,"Favor de responder para continuar")
            return render(request, 'documentos/estadisticas_usuario.html',{'form':form,'usuario':usuario,'num_sesiones':num_sesiones,'duracion_promedio':duracion_promedio,'num_parrafos':num_parrafos,'num_etiquetados':num_etiquetados,'num_revisiones':num_revisiones})
    else:
        form=estadisticas_Usuario_Form(usuario=usuario)
        return render(request, 'documentos/estadisticas_usuario.html',{'form':form,'usuario':usuario,'num_sesiones':num_sesiones,'duracion_promedio':duracion_promedio,'num_parrafos':num_parrafos,'num_etiquetados':num_etiquetados,'num_revisiones':num_revisiones})
@login_required
@user_passes_test(en_grupo_administradores, login_url='/acceso_denegado/')
def concordancia_Usuarios(request,pk1,pk2):
    try:
        usuario1=User.objects.get(pk=pk1)
        usuario2=User.objects.get(pk=pk2)
    except User.DoesNotExist:
        return HttpResponse("ERROR, la dirección no es válida")
    etiquetados1=Etiquetado.objects.filter(grupo__anotacion__anotador=usuario1).distinct()
    etiquetados2=Etiquetado.objects.filter(grupo__anotacion__anotador=usuario2).distinct()
    etiquetas=Etiquetas.objects.filter( Q(etiquetado__in=etiquetados1) | Q(etiquetado__in=etiquetados2) ).distinct()
    revisiones1=Revisiones.objects.filter(revisor=usuario1,revision_finalizada=True,etiquetado__in=etiquetados2)
    revisiones2=Revisiones.objects.filter(revisor=usuario2,revision_finalizada=True,etiquetado__in=etiquetados1)
    try:
        pr_acuerdo=( revisiones1.filter(acuerdo=True).count() + revisiones2.filter(acuerdo=True).count() ) / ( revisiones1.count() + revisiones2.count() )
    except ZeroDivisionError:
        return HttpResponse("No hay revisiones para hacer el cálculo")
    pr_azar=0
    cuenta_etiquetados1=etiquetados1.count()
    cuenta_etiquetados2=etiquetados2.count()
    for etiqueta in etiquetas:
        try:
            pr_e1=( etiquetados1.filter(etiqueta_asignada=etiqueta).count() ) / ( cuenta_etiquetados1 )
        except ZeroDivisionError:
            return HttpResponse("No hay anotaciones para hacer el cálculo")
        try:
            pr_e2=( etiquetados2.filter(etiqueta_asignada=etiqueta).count() ) / ( cuenta_etiquetados2 )
        except ZeroDivisionError:
            return HttpResponse("No hay anotaciones para hacer el cálculo")
        pr_azar+=pr_e1*pr_e2
    kappa=( pr_acuerdo - pr_azar ) / ( 1 - pr_azar )
    return render(request, 'documentos/concordancia_usuarios.html',{'kappa':kappa,'usuario1':usuario1,'usuario2':usuario2})
@login_required
def registro_Actividad(request):
    return render(request, 'documentos/registro_actividad.html',{'usuario':request.user})
@login_required
def registro_Actividad_Administra_Revision(request,pk):
    try:
        time_threshold = datetime.now() - timedelta(hours=96)
        revision=Revisiones.objects.get(pk=pk,revisor=request.user,fecha_revision__gt=time_threshold)
        anotaciones=Anotaciones.objects.filter(palabras__grupo__revision=revision).distinct()
        anotacion=anotaciones[:1].get()
        palabras=Palabras.objects.filter(anotacion=anotacion).order_by('num_palabra')
    except Revisiones.DoesNotExist:
        return redirect('/acceso_denegado/')
    if request.POST:
        form=revision_Form(request.POST)
        if form.is_valid():
            acuerdo=form.cleaned_data["acuerdo"]
            revision.acuerdo=acuerdo
            revision.revision_finalizada=True
            revision.fecha_revision=make_aware(datetime.now())
            revision.save()
            messages.success(request, 'Revisiones actualizada')
            return redirect(reverse('documentos_app:revisa_ley',args=(anotacion.parrafo.ley.pk,)))
        else:
            messages.info(request,"Favor de responder")
            return render(request, 'documentos/revision.html',{'form':form,'palabras':palabras,'anotacion':anotacion,'revision':revision})
    else:
        form=revision_Form(initial={'acuerdo':revision.acuerdo})
        return render(request, 'documentos/revision.html',{'form':form,'palabras':palabras,'anotacion':anotacion,'revision':revision})
@login_required
def registro_Actividad_Administra_Etiquetado(request,pk):
    try:
        time_threshold = datetime.now() - timedelta(hours=96)
        etiquetado=Etiquetado.objects.get(pk=pk,fecha_etiquetado__gt=time_threshold)
        anotaciones=Anotaciones.objects.filter(palabras__grupo=etiquetado).distinct()
        anotacion=anotaciones[:1].get()
        palabras=Palabras.objects.filter(anotacion=anotacion).order_by('num_palabra')
    except Revisiones.DoesNotExist:
        return redirect('/acceso_denegado/')
    return render(request, 'documentos/registro_actividad_administra_etiquetado.html',{'palabras':palabras,'anotacion':anotacion,'etiquetado':etiquetado})
@login_required
def consulta_Documentos_Parrafo(request,pk):
    try:
        parrafo=Parrafos.objects.get(pk=pk,ley__captura_parrafos_finalizada=True)
    except:
        return HttpResponse("Dirección incorrecta")
    try:
        anotable=Parrafos.objects.get(pk=pk,anotacion__anotador=request.user)
        anotable=True
    except:
        anotable=False
    return render(request, 'documentos/consulta_documentos_parrafo.html',{'parrafo':parrafo,'anotable':anotable})
@login_required
def AnotacionGeneralView(request, anotacion_id):
    print("AnotacionView")
    print(anotacion_id)
    template_name='documentos/generar_anotacion_2.html'
    anotacion = get_object_or_404(Anotacion, id=anotacion_id)
    documento = anotacion.documento
    if request.method == 'POST':
        return render(request, template_name=template_name,
                      context={'anotacion':anotacion,
                               'palabras': json.dumps(json.loads(anotacion.get_texto())[:500]),
                               })
    parrafo = documento.get_siguiente_parrafo()
    print("parrafo: {0} ".format(parrafo))
    return redirect(reverse('documentos_app:anotacion-especifica',
                            kwargs={'anotacion_id':anotacion_id, 'parrafo_id':parrafo.id})
                    )
    tags_leyes={}
    try:
        tags_leyes = TAG.objects.filter(subtag=TAG.objects.get(texto="leyes")).count()
    except Exception as e:
        print("error al intentar obtener tags de leyes: {0}".format(e))
    return render(request, template_name=template_name,
                  context={'anotacion':anotacion,
                           'palabras': parrafo.texto,
                           'parrafo_id':parrafo.id,
                           'tags_leyes':tags_leyes,
                           'tags_usuario': request.user.tags.all()
                           })
@login_required
def AnotacionView(request, anotacion_id, parrafo_id):
    print("AnotacionView")
    print(anotacion_id, parrafo_id)
    template_name='documentos/generar_anotacion_2.html'
    anotacion = get_object_or_404(Anotacion, id=anotacion_id, anotador=request.user)
    if anotacion.is_done:
        print("ya se marco como terminada la anotacion, redirijimos a perfil")
        return redirect(reverse('usuarios_app:perfil_home'))
    parrafo = get_object_or_404(Parrafo, id=parrafo_id, documento__id=anotacion.documento.id)
    documento = anotacion.documento
    print("parrafo: {0} ".format(parrafo))
    tags_leyes={}
    try:
        tags_leyes = TAG.objects.filter(subtag=TAG.objects.get(texto="leyes")).values('id','texto')
    except Exception as e:
        print("error al intentar obtener tags de leyes: {0}".format(e))
    has_argumentacion=False
    if (ArgumentacionParrafo.objects.filter(autor=request.user, parrafo=parrafo).exists()):
        print("ya tiene argumentacion el parrafo")
        has_argumentacion=True
    return render(request, template_name=template_name,
                  context={'anotacion':anotacion,
                           'get_next_parrafo': parrafo.get_next_parrafo(),
                           'get_prev_parrafo': parrafo.get_prev_parrafo(),
                           'palabras': parrafo.texto,
                           'parrafo_id':parrafo.id,
                           'tags_leyes':tags_leyes,
                           'parrafo':parrafo,
                           'has_argumentacion':has_argumentacion,
                           'tags_usuario': request.user.tags.all().values('tag__texto','alias')
                           })
@login_required
def TerminarDocumentoView(request, anotacion_id):
    print("TerminarDocumentoView")
    print(anotacion_id)
    documento = get_object_or_404(Documento, id=anotacion_id)
    documento_form = DocumentoForm(instance=documento)
    if 'anotacion_id' in request.session:
        anotacion_id = request.session['anotacion_id']
    return render(request, template_name='documentos/terminar_documento.html',
                  context={'documento':documento,
                           'documento_form':documento_form,
                           'anotacion_id':anotacion_id})
@csrf_exempt
def guardar_anotacion(request):
    if request.method == 'POST':
        print("funcion guardar_anotacion")
        print("Validando que venga request.POST")
        print(request.method, request.POST)
        is_valid=True
        if request.POST:
            informacion = json.loads(json.dumps(request.POST))
        else:
            return HttpResponse("POST vacio")
        if not 'id_anotacion' in informacion:
            is_valid=False
            print("Falta el ID de anotacion")
        if not 'tipo_anotacion' in informacion:
            is_valid=False
            print("Falta el tipo de anotacion")
        if not 'clasificacion' in informacion:
            is_valid=False
            print("Falta la clasificacion de la anotacion")
        if not 'informacion' in informacion:
            is_valid=False
            print("Falta la informacion de la anotacion")
        if is_valid:
            print("PROCESAMOS/ GUARDAMOS LA ANOTACION")
            return HttpResponse("EXITO !! :D")
        return HttpResponse("ERROR, no se envio la informacion completa")
    return HttpResponse("Metodo GET  no permitido")
class OracionViewSet(viewsets.ModelViewSet):
    queryset = Oracion.objects.all()
    serializer_class = OracionSerializer
    def create(self, request, *args, **kwargs):
        print("METODO CREATE OracionViewSet")
        clasificacion = ""
        informacion_tags = {}
        if request.data.get('clasificacion', False):
            print(request.data['clasificacion'])
            clasificacion = request.data['clasificacion']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        oracion = serializer.instance
        if clasificacion == 'referencia_articulo':
            print("Anotacion de referencia a articulo")
            print(oracion)
            tag_ley = request.data.get("tag_ley", "")
            tag_numero_articulo = request.data.get("tag_numero_articulo", "")
            tag_apartado = request.data.get("tag_apartado", "")
            tag_fraccion = request.data.get("tag_fraccion", "")
            tag_inciso = request.data.get("tag_inciso", "")
            tag_parrafo = request.data.get("tag_parrafo", "")
            custom_classificacion = Clasificacion.objects.get(key='creada_por_usuario')
            if tag_numero_articulo:
                tna, creado = TAG.objects.get_or_create(subtag=TAG.objects.get(texto='numero_articulo'), texto=tag_numero_articulo)
                oracion.tags.add(tna)
            if tag_apartado:
                ta, creado = TAG.objects.get_or_create(subtag=TAG.objects.get(texto='apartado'), texto=tag_apartado)
                oracion.tags.add(ta)
                TAGPersonal.objects.get_or_create(tag=ta, alias='default')
            if tag_fraccion:
                tf, creado = TAG.objects.get_or_create(subtag=TAG.objects.get(texto='fraccion'), texto=tag_fraccion)
                oracion.tags.add(tf)
            if tag_inciso:
                ti, creado = TAG.objects.get_or_create(subtag=TAG.objects.get(texto='inciso'), texto=tag_inciso)
                oracion.tags.add(ti)
            if tag_parrafo:
                tp, creado = TAG.objects.get_or_create(subtag=TAG.objects.get(texto='parrafo'), texto=tag_parrafo)
                oracion.tags.add(tp)
            oracion.save()
        if clasificacion == 'palabra':
            print("Anotacion de referencia a articulo")
            tag_palabra = request.data.get("tag_palabra", "")
            if tag_palabra:
                tp, creado = TAG.objects.get_or_create(subtag=TAG.objects.get(texto='palabra'), texto=tag_palabra)
                oracion.tags.add(tp)
        self.generar_evaluacion_parrafo(request, oracion)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def generar_evaluacion_parrafo(self, request, oracion):
        evaluacion = EvaluacionParrafo.objects.create(
            autor=request.user,oracion=oracion, texto=oracion.texto,
            tipo_anotacion=oracion.tipo_anotacion,
            clasificacion=oracion.clasificacion,
        )
        if oracion.tags.all():
            evaluacion.tags.add(*oracion.tags.all())
class ParrafoViewSet(viewsets.ModelViewSet):
    queryset = Parrafo.objects.all()
    serializer_class = ParrafoSerializer
    def create(self, request, *args, **kwargs):
        print("METODO CREATE ParrafoViewSet")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def update(self, request, *args, **kwargs):
        print("update de ParrafoViewSet")
        return super(ParrafoViewSet, self).update(request, *args, **kwargs)
    def guardar_argumentacion(self, request, *args, **kwargs):
        print("guardar_argumentacion de ParrafoViewSet")
        argumentacion = ArgumentacionParrafoSerializer(data=request.POST, context={'request':request})
        if argumentacion.is_valid():
            print("argumentacion valida")
            print(argumentacion.validated_data)
            argumentacion.save()
        return super(ParrafoViewSet, self).update(request, *args, **kwargs)
class TAGSLeyesViewSet(viewsets.ModelViewSet):
    queryset = TAG.objects.all()
    serializer_class = TAGLeyesSerializer
class AnotacionViewSet(viewsets.ModelViewSet):
    queryset = Anotacion.objects.all()
    serializer_class = AnotacionSerializer
    def create(self, request, *args, **kwargs):
        print("METODO CREATE AnotacionViewSet")
        request = super(AnotacionViewSet, self).create(request, *args, **kwargs)
class ArgumentacionParrafoViewSet(viewsets.ModelViewSet):
    queryset = ArgumentacionParrafo.objects.all()
    serializer_class = ArgumentacionParrafoSerializer
    def create(self, request, *args, **kwargs):
        print("METODO CREATE ArgumentacionParrafo")
        request = super(ArgumentacionParrafoViewSet, self).create(request, *args, **kwargs)
        return request
class TAGPersonalViewSet(viewsets.ModelViewSet):
    queryset = TAGPersonal.objects.all()
    serializer_class = TAGPersonalSerializer
    def create(self, request, *args, **kwargs):
        print("METODO CREATE TAGPersonalViewSet")
        return super(TAGPersonalViewSet, self).create(request, *args, **kwargs)
@login_required
def RevisionGeneralView(request, anotacion_id):
    print("RevisionGeneralView")
    print(anotacion_id)
    template_name='documentos/revisar_anotacion.html'
    anotacion = get_object_or_404(Anotacion, id=anotacion_id)
    documento = anotacion.documento
    if request.method == 'POST':
        return render(request, template_name=template_name,
                      context={'anotacion':anotacion,
                               'palabras': json.dumps(json.loads(anotacion.get_texto())[:500]),
                               })
    parrafo = documento.get_siguiente_parrafo()
    print("parrafo: {0} ".format(parrafo))
    return redirect(reverse('documentos_app:revision-especifica',
                            kwargs={'anotacion_id':anotacion_id, 'parrafo_id':parrafo.id})
                    )
    tags_leyes={}
    try:
        tags_leyes = TAG.objects.filter(subtag=TAG.objects.get(texto="leyes")).count()
    except Exception as e:
        print("error al intentar obtener tags de leyes: {0}".format(e))
    return render(request, template_name=template_name,
                  context={'anotacion':anotacion,
                           'palabras': parrafo.texto,
                           'parrafo_id':parrafo.id,
                           'tags_leyes':tags_leyes,
                           'tags_usuario': request.user.tags.all()
                           })
@login_required
def RevisionView(request, anotacion_id, parrafo_id):
    print("RevisionView")
    print(anotacion_id, parrafo_id)
    template_name='documentos/revisar_anotacion.html'
    anotacion = get_object_or_404(Anotacion, id=anotacion_id, revisor=request.user)
    parrafo = get_object_or_404(Parrafo, id=parrafo_id, documento__id=anotacion.documento.id)
    documento = anotacion.documento
    oraciones = Oracion.objects.filter(parrafo=parrafo)
    tags_leyes={}
    try:
        ids_tags = request.user.tags.all().values_list('tag')
        tags_leyes = TAG.objects.exclude(id__in=ids_tags).filter(subtag=TAG.objects.get(texto="leyes")).values('id','texto')
    except Exception as e:
        print("error al intentar obtener tags de leyes: {0}".format(e))
    has_argumentacion=False
    if (ArgumentacionParrafo.objects.filter(autor=request.user, parrafo=parrafo).exists()):
        print("ya tiene argumentacion el parrafo")
        has_argumentacion=True
    return render(request, template_name=template_name,
                  context={'anotacion':anotacion,
                           'get_next_parrafo': parrafo.get_next_parrafo(),
                           'get_prev_parrafo': parrafo.get_prev_parrafo(),
                           'palabras': parrafo.texto,
                           'parrafo_id':parrafo.id,
                           'tags_leyes':tags_leyes,
                           'parrafo':parrafo,
                           'has_argumentacion':has_argumentacion,
                           'tags_usuario': request.user.tags.all().values('tag__texto','alias','tag'),
                           'oraciones':oraciones
                           })
