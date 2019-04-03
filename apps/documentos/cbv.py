# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.forms import ModelForm
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from datetime import datetime, timedelta
from django.utils.timezone import make_aware    
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .tests import en_grupo_administradores
from .models import (Leyes,Parrafos,Etiquetas,Anotaciones,Etiquetado,Revisiones)
class registra_Ley_Form(ModelForm):
    class Meta:
        model=Leyes
        fields=["nombre_oficial","identificador","fecha_publicacion","fecha_ultima_modificacion","capturador","archivo_docx","archivo_pdf"]
        help_texts = {
            'fecha_publicacion': "YYYY-MM-DD",
            'fecha_ultima_modificacion': "YYYY-MM-DD",
        }
class registra_Ley(UserPassesTestMixin,SuccessMessageMixin,CreateView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Ley registrada exitosamente"
    model=Leyes
    template_name="documentos/registrar_ley.html"
    form_class=registra_Ley_Form
class lista_Leyes(UserPassesTestMixin,ListView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Leyes
    template_name = "documentos/lista_leyes.html"
class actualiza_Ley_Form(ModelForm):
    class Meta:
        model=Leyes
        fields=["nombre_oficial","identificador","fecha_publicacion","fecha_ultima_modificacion","capturador","captura_parrafos_finalizada","visible_anotadores","archivo_docx","archivo_pdf"]
class actualiza_Ley(UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Ley actualizada exitosamente"
    model=Leyes
    template_name="documentos/actualiza_ley.html"
    form_class=actualiza_Ley_Form
class registra_Etiqueta_Form(ModelForm):
    class Meta:
        model=Etiquetas
        fields=["etiqueta","descripcion","ejemplos","visible_anotadores"]
class registra_Etiqueta(UserPassesTestMixin,SuccessMessageMixin,CreateView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Etiqueta registrada exitosamente"
    model=Etiquetas
    template_name="documentos/registrar_etiqueta.html"
    form_class=registra_Etiqueta_Form
class proponer_Etiqueta_Form(ModelForm):
    class Meta:
        model=Etiquetas
        fields=["etiqueta","descripcion","ejemplos"]
class proponer_Etiqueta(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    success_message="Etiqueta propuesta exitosamente"
    model=Etiquetas
    template_name="documentos/proponer_etiqueta.html"
    form_class=proponer_Etiqueta_Form
    def form_valid(self, form): 
        if form.is_valid(): 
            etiqueta=form.cleaned_data["etiqueta"]
            descripcion=form.cleaned_data["descripcion"]
            ejemplos=form.cleaned_data["ejemplos"]
            propuesta=True
            propuesta_por=self.request.user
            obj=Etiquetas(etiqueta=etiqueta,
                        descripcion=descripcion,
                        ejemplos=ejemplos,
                        propuesta=propuesta,
                        propuesta_por=propuesta_por)
            try:
                obj.save()
                messages.success(self.request, "Etiqueta propuesta exitosamente")
            except IntegrityError as e:
                messages.error(self.request, "Los datos que proporcionó colisionan con datos ya existentes")
        else:
            messages.error(self.request, "Los datos no son válidos")
class lista_Etiquetas(UserPassesTestMixin,ListView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Etiquetas
    template_name = "documentos/lista_etiquetas.html"
    def get_queryset(self):
        queryset=Etiquetas.objects.filter(propuesta=False)
        return queryset
class lista_Etiquetas_Propuestas(UserPassesTestMixin,ListView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Etiquetas
    template_name = "documentos/lista_etiquetas.html"
    def get_queryset(self):
        queryset=Etiquetas.objects.filter(propuesta=True)
        return queryset
class actualiza_Etiqueta_Form(ModelForm):
    class Meta:
        model=Etiquetas
        fields=["etiqueta","descripcion","ejemplos","visible_anotadores"]
class actualiza_Etiqueta(UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Etiqueta actualizada exitosamente"
    model=Etiquetas
    template_name="documentos/actualiza_etiqueta.html"
    form_class=actualiza_Etiqueta_Form
class elimina_Etiqueta(UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Etiqueta eliminada exitosamente"
    model=Etiquetas
    template_name="documentos/elimina_etiqueta.html"
class registra_Parrafos(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Leyes
    template_name = "documentos/registra_parrafos.html"
    def get_queryset(self): 
        queryset=Leyes.objects.filter(capturador=self.request.user,visible_anotadores=True)
        return queryset
class registra_Parrafo_Form(ModelForm):
    class Meta:
        model=Parrafos
        fields=["titulo","capitulo","base","apartado","articulo","fraccion","inciso","parrafo","texto"]
class registra_Parrafo(UserPassesTestMixin,CreateView): 
    def test_func(self):
        self.ley=Leyes.objects.get(pk=self.kwargs['pk'])    
        if (self.ley.capturador == self.request.user and self.ley.visible_anotadores):
            return True
        else:
            return False
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Parrafos
    template_name="documentos/registrar_parrafo.html"
    form_class=registra_Parrafo_Form
    def get_context_data(self,**kwargs):    
        parrafos_capturados=Parrafos.objects.filter(ley=self.ley).only("parrafo")
        context=super(registra_Parrafo,self).get_context_data(**kwargs)
        context.update({'ley':self.ley,"parrafos_capturados":parrafos_capturados})
        return context
    def get_initial(self):
        query_parrafos = Parrafos.objects.filter(ley=self.ley,capturador=self.request.user).order_by('-fecha_registro') 
        query_ultimo_parrafo = query_parrafos[:1]
        if query_ultimo_parrafo:
            ultimo_parrafo=query_ultimo_parrafo.get()
            return {
                "titulo":ultimo_parrafo.titulo,
                "capitulo":ultimo_parrafo.capitulo,
                "base":ultimo_parrafo.base,
                "apartado":ultimo_parrafo.apartado,
                "articulo":ultimo_parrafo.articulo,
                "fraccion":ultimo_parrafo.fraccion,
                "inciso":ultimo_parrafo.inciso,
                "parrafo":ultimo_parrafo.parrafo+1,
            }
        else:
            return {"parrafo":1,}
    def form_valid(self, form): 
        if form.is_valid(): 
            titulo=form.cleaned_data["titulo"]
            capitulo=form.cleaned_data["capitulo"]
            base=form.cleaned_data["base"]
            apartado=form.cleaned_data["apartado"]
            articulo=form.cleaned_data["articulo"]
            fraccion=form.cleaned_data["fraccion"]
            inciso=form.cleaned_data["inciso"]
            parrafo=form.cleaned_data["parrafo"]
            texto=form.cleaned_data["texto"]
            ley = self.ley 
            capturador = self.request.user
            fecha_registro = make_aware(datetime.now())
            obj=Parrafos(titulo=titulo,
                        capitulo=capitulo,
                        base=base,
                        apartado=apartado,
                        articulo=articulo,
                        fraccion=fraccion,
                        inciso=inciso,
                        parrafo=parrafo,
                        texto=texto,
                        ley=ley,
                        capturador=capturador,
                        fecha_registro=fecha_registro)
            try:
                obj.save()
                messages.success(self.request, "Parrafo registrado exitosamente")
                return HttpResponseRedirect(reverse('documentos_app:registra_parrafo',args=(self.kwargs['pk'],)))
            except IntegrityError as e:
                messages.error(self.request, "Los datos que proporcionó colisionan con datos ya existentes")
                return HttpResponseRedirect(reverse('documentos_app:registra_parrafo',args=(self.kwargs['pk'],)))
        else:
            messages.error(self.request, "Los datos no son válidos")
            return HttpResponseRedirect(reverse('documentos_app:registra_parrafo',args=(self.kwargs['pk'],)))
class detalles_Parrafo(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Parrafos
    template_name = "documentos/detalles_parrafos.html"
class lista_Parrafos_Leyes(UserPassesTestMixin,ListView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Leyes
    template_name = "documentos/lista_parrafos_leyes.html"
    def get_queryset(self):
        queryset=Leyes.objects.exclude(parrafo=None).distinct()
        return queryset
class lista_Parrafos_Ley(UserPassesTestMixin,ListView):
    def test_func(self):
        self.ley=Leyes.objects.get(pk=self.kwargs['pk'])
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Parrafos
    template_name = "documentos/lista_parrafos_ley.html"
    def get_queryset(self):
        queryset=Parrafos.objects.filter(ley=self.ley).distinct()
        return queryset
class actualiza_Parrafo_Form(ModelForm):
    class Meta:
        model=Parrafos
        fields=["ley","capturador","titulo","capitulo","base","apartado","articulo","fraccion","inciso","parrafo"]
class actualiza_Parrafo(UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Párrafo actualizado exitosamente"
    model=Parrafos
    template_name="documentos/actualiza_parrafo.html"
    form_class=actualiza_Parrafo_Form
class elimina_Parrafo(UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Párrafo eliminada exitosamente"
    model=Parrafos
    template_name="documentos/elimina_parrafo.html"
class asigna_Anotacion_Leyes(UserPassesTestMixin,ListView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Leyes
    template_name = "documentos/asigna_anotaciones_leyes.html"
    def get_queryset(self): 
        parrafos_sinAnotacion_asignada=Parrafos.objects.filter(anotacion=None)
        queryset=Leyes.objects.filter(parrafo__in=parrafos_sinAnotacion_asignada).distinct()
        return queryset
class lista_Anotaciones_Leyes(UserPassesTestMixin,ListView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Leyes
    template_name = "documentos/lista_anotaciones_leyes.html"
    def get_queryset(self): 
        anotaciones_asignadas=Anotaciones.objects.all()
        queryset=Leyes.objects.filter(parrafo__anotacion__in=anotaciones_asignadas).distinct()
        return queryset
class lista_Anotaciones_Ley(UserPassesTestMixin,ListView):
    def test_func(self):
        self.ley=Leyes.objects.get(pk=self.kwargs['pk'])
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Anotaciones
    template_name = "documentos/lista_anotaciones_ley.html"
    def get_queryset(self):
        queryset=Anotaciones.objects.filter(parrafo__ley=self.ley).distinct()
        return queryset
class actualiza_Anotacion_Form(ModelForm):
    class Meta:
        model=Anotaciones
        fields=["parrafo","anotador","anotacion_finalizada"]
class actualiza_Anotacion(UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Anotación actualizada exitosamente"
    model=Anotaciones
    template_name="documentos/actualiza_anotacion.html"
    form_class=actualiza_Anotacion_Form
class elimina_Anotacion(UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Anotacion eliminada exitosamente"
    model=Anotaciones
    template_name="documentos/elimina_anotacion.html"
class asigna_Revision_Leyes(UserPassesTestMixin,ListView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Leyes
    template_name = "documentos/asigna_revision_leyes.html"
    def get_queryset(self): 
        etiquetado_sinRevision=Etiquetado.objects.filter(revision=None)
        queryset=Leyes.objects.filter(parrafo__anotacion__palabras__grupo__in=etiquetado_sinRevision).distinct()
        return queryset
class asigna_Revision_Ley(UserPassesTestMixin,ListView):
    def test_func(self):
        self.ley=Leyes.objects.get(pk=self.kwargs['pk'])
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Parrafos
    template_name = "documentos/asigna_revision_ley.html"
    def get_queryset(self):
        etiquetado_sinRevision=Etiquetado.objects.filter(revision=None)
        queryset=Parrafos.objects.filter(ley=self.ley,anotacion__palabras__grupo__in=etiquetado_sinRevision).distinct()
        return queryset
class asigna_Revision_Usuarios(UserPassesTestMixin,ListView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=User
    template_name = "documentos/asigna_revision_usuarios.html"
    def get_queryset(self): 
        etiquetado_sinRevision=Etiquetado.objects.filter(revision=None)
        queryset=User.objects.filter(anotacion__palabras__grupo__in=etiquetado_sinRevision).distinct()
        return queryset
class asigna_Revision_Usuario(UserPassesTestMixin,ListView):
    def test_func(self):
        self.usuario=User.objects.get(pk=self.kwargs['pk'])
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Parrafos
    template_name = "documentos/asigna_revision_usuario.html"
    def get_queryset(self):
        etiquetado_sinRevision=Etiquetado.objects.filter(revision=None)
        queryset=Parrafos.objects.filter(anotacion__anotador=self.usuario,anotacion__palabras__grupo__in=etiquetado_sinRevision).distinct()
        return queryset
class lista_Revisiones_Leyes(UserPassesTestMixin,ListView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Leyes
    template_name = "documentos/lista_revisiones_leyes.html"
    def get_queryset(self): 
        revisiones_asignadas=Revisiones.objects.all()
        queryset=Leyes.objects.filter(parrafo__anotacion__palabras__grupo__revision__in=revisiones_asignadas).distinct()
        return queryset
class lista_Revisiones_Ley(UserPassesTestMixin,ListView):
    def test_func(self):
        self.ley=Leyes.objects.get(pk=self.kwargs['pk'])
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Revisiones
    template_name = "documentos/lista_revisiones_ley.html"
    def get_queryset(self):
        queryset=Revisiones.objects.filter(etiquetado__grupo__anotacion__parrafo__ley=self.ley).distinct()
        return queryset
class actualiza_Revision_Form(ModelForm):
    class Meta:
        model=Revisiones
        fields=["revisor","revision_finalizada"]
class actualiza_Revision(UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Revisión actualizada exitosamente"
    model=Revisiones
    template_name="documentos/actualiza_revision.html"
    form_class=actualiza_Revision_Form
class elimina_Revision(UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Revisión eliminada exitosamente"
    model=Revisiones
    template_name="documentos/elimina_revision.html"
class anotacion_Leyes(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Leyes
    template_name = "documentos/anota_leyes.html"
    def get_queryset(self): 
        queryset=Leyes.objects.filter(parrafo__anotacion__anotador=self.request.user,visible_anotadores=True).distinct()
        return queryset
class anotacion_Ley(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Anotaciones
    template_name = "documentos/anota_ley.html"
    def get_queryset(self):
        self.ley=Leyes.objects.get(pk=self.kwargs['pk'])
        queryset=Anotaciones.objects.filter(parrafo__ley=self.ley,anotador=self.request.user,parrafo__ley__visible_anotadores=True).distinct()
        return queryset
class descripcion_etiquetas(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Etiquetas
    template_name = "documentos/descripcion_etiquetas.html"
    def get_queryset(self):
        queryset=Etiquetas.objects.filter(visible_anotadores=True,propuesta=False)
        return queryset
class descripcion_etiqueta(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Etiquetas
    template_name = "documentos/descripcion_etiqueta.html"
class revision_Leyes(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Leyes
    template_name = "documentos/revisa_leyes.html"
    def get_queryset(self): 
        queryset=Leyes.objects.filter(parrafo__anotacion__palabras__grupo__revision__revisor=self.request.user,parrafo__anotacion__palabras__grupo__revision__revision_finalizada=False,visible_anotadores=True).distinct()
        return queryset
class revision_Ley(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Revisiones
    template_name = "documentos/revisa_ley.html"
    def get_queryset(self):
        self.ley=Leyes.objects.get(pk=self.kwargs['pk'])
        queryset=Revisiones.objects.filter(revision_finalizada=False,etiquetado__grupo__anotacion__parrafo__ley=self.ley,etiquetado__grupo__anotacion__parrafo__ley__visible_anotadores=True,revisor=self.request.user).distinct()
        return queryset
class revision_Form(ModelForm):
    class Meta:
        model=Revisiones
        fields=["acuerdo"]
class revision(UserPassesTestMixin,SuccessMessageMixin,UpdateView): 
    def test_func(self):
        self.revision=Revisiones.objects.get(pk=self.kwargs['pk'])    
        self.ley=Leyes.objects.filter(parrafo__anotacion__palabras__grupo__etiquetado__revision__revisor=self.request.user).distinct()
        if (self.revision.revisor == self.request.user and self.ley.visible_anotadores):
            return True
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Revisión exitosa"
    model=Revisiones
    template_name="documentos/revision.html"
    form_class=revision_Form
class estadisticas_Usuarios(UserPassesTestMixin,ListView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=User
    template_name = "documentos/estadisticas_usuarios.html"
class registro_Actividad_Parrafos(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Parrafos
    template_name = "documentos/lista_parrafos_registro_actividad.html"
    def get_queryset(self):
        time_threshold = datetime.now() - timedelta(hours=96)
        queryset=Parrafos.objects.filter(capturador=self.request.user,fecha_registro__gt=time_threshold).order_by('-fecha_registro')
        return queryset
class registro_Actividad_Administra_Parrafo_Form(ModelForm):
    class Meta:
        model=Parrafos
        fields=["titulo","capitulo","base","apartado","articulo","fraccion","inciso","parrafo","texto"]
class registro_Actividad_Administra_Parrafo(UserPassesTestMixin,CreateView): 
    def test_func(self):
        try:
            time_threshold = datetime.now() - timedelta(hours=96)
            self.parrafo=Parrafos.objects.get(pk=self.kwargs['pk'],capturador=self.request.user,fecha_registro__gt=time_threshold)
            self.ley=self.parrafo.ley
            return True
        except Parrafos.DoesNotExist:
            return False
    def get_login_url(self):
        return '/acceso_denegado/'
    model=Parrafos
    template_name="documentos/registrar_parrafo.html"
    form_class=registro_Actividad_Administra_Parrafo_Form
    def get_context_data(self,**kwargs):    
        parrafos_capturados=Parrafos.objects.filter(ley=self.ley).only("parrafo")
        context=super(registro_Actividad_Administra_Parrafo,self).get_context_data(**kwargs)
        context.update({'ley':self.ley,"parrafos_capturados":parrafos_capturados})
        return context
    def get_initial(self):
        return {
            "titulo":self.parrafo.titulo,
            "capitulo":self.parrafo.capitulo,
            "base":self.parrafo.base,
            "apartado":self.parrafo.apartado,
            "articulo":self.parrafo.articulo,
            "fraccion":self.parrafo.fraccion,
            "inciso":self.parrafo.inciso,
            "parrafo":self.parrafo.parrafo,
        }
    def form_valid(self, form): 
        if form.is_valid(): 
            if self.parrafo.texto == form.cleaned_data["texto"]:
                self.parrafo.titulo=form.cleaned_data["titulo"]
                self.parrafo.capitulo=form.cleaned_data["capitulo"]
                self.parrafo.base=form.cleaned_data["base"]
                self.parrafo.apartado=form.cleaned_data["apartado"]
                self.parrafo.articulo=form.cleaned_data["articulo"]
                self.parrafo.fraccion=form.cleaned_data["fraccion"]
                self.parrafo.inciso=form.cleaned_data["inciso"]
                self.parrafo.parrafo=form.cleaned_data["parrafo"]
                self.parrafo.fecha_registro = make_aware(datetime.now())
                obj=self.parrafo
            else:
                try:
                    parrafo_test=Parrafos.objects.get(ley=self.ley,parrafo=form.cleaned_data["parrafo"])
                    if parrafo_test != self.parrafo:
                        messages.error(self.request, "Los datos que proporcionó colisionan con datos ya existentes")
                        return HttpResponseRedirect(reverse('documentos_app:registra_parrafo',args=(self.ley.pk,)))
                except: pass
                self.parrafo.delete()
                titulo=form.cleaned_data["titulo"]
                capitulo=form.cleaned_data["capitulo"]
                base=form.cleaned_data["base"]
                apartado=form.cleaned_data["apartado"]
                articulo=form.cleaned_data["articulo"]
                fraccion=form.cleaned_data["fraccion"]
                inciso=form.cleaned_data["inciso"]
                parrafo=form.cleaned_data["parrafo"]
                fecha_registro = make_aware(datetime.now())
                texto=form.cleaned_data["texto"]
                ley = self.ley 
                capturador = self.request.user
                obj=Parrafos(titulo=titulo,
                        capitulo=capitulo,
                        base=base,
                        apartado=apartado,
                        articulo=articulo,
                        fraccion=fraccion,
                        inciso=inciso,
                        parrafo=parrafo,
                        texto=texto,
                        ley=ley,
                        capturador=capturador,
                        fecha_registro=fecha_registro)
            try:
                obj.save()
                messages.success(self.request, "Parrafo actualizado exitosamente")
                return HttpResponseRedirect(reverse('documentos_app:registra_parrafo',args=(self.ley.pk,)))
            except IntegrityError as e:
                messages.error(self.request, "Los datos que proporcionó colisionan con datos ya existentes")
                return HttpResponseRedirect(reverse('documentos_app:registra_parrafo',args=(self.ley.pk,)))
        else:
            messages.error(self.request, "Los datos no son válidos")
            return HttpResponseRedirect(reverse('documentos_app:registra_parrafo',args=(self.ley.pk,)))
class registro_Actividad_Elimina_Parrafo(UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    def test_func(self):
        try:
            time_threshold = datetime.now() - timedelta(hours=96)
            self.parrafo=Parrafos.objects.get(pk=self.kwargs['pk'],capturador=self.request.user,fecha_registro__gt=time_threshold)
            return True
        except Parrafos.DoesNotExist:
            return False
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Párrafo eliminado exitosamente"
    model=Parrafos
    template_name="documentos/elimina_parrafo.html"
class registro_Actividad_Anotaciones(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Anotaciones
    template_name = "documentos/lista_anotaciones_registro_actividad.html"
    def get_queryset(self):
        time_threshold = datetime.now() - timedelta(hours=96)
        queryset=Anotaciones.objects.filter(anotador=self.request.user,palabras__grupo__fecha_etiquetado__gt=time_threshold).distinct()
        return queryset
class registro_Actividad_Administra_Anotacion(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Etiquetado
    template_name = "documentos/lista_etiquetado_registro_actividad.html"
    def get_queryset(self):
        time_threshold = datetime.now() - timedelta(hours=96)
        queryset=Etiquetado.objects.filter(grupo__anotacion=self.kwargs['pk'],grupo__anotacion__anotador=self.request.user,fecha_etiquetado__gt=time_threshold).distinct()
        return queryset
class registro_Actividad_Elimina_Anotacion(UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    def test_func(self):
        try:
            time_threshold = datetime.now() - timedelta(hours=96)
            self.anotacion=Anotaciones.objects.filter(pk=self.kwargs['pk'],anotador=self.request.user,palabras__grupo__fecha_etiquetado__gt=time_threshold).distinct()[:1].get()
            return True
        except Anotaciones.DoesNotExist:
            return False
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Anotacion eliminada exitosamente"
    model=Anotaciones
    template_name="documentos/elimina_anotacion.html"
class registro_Actividad_Elimina_Etiquetado(UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    def test_func(self):
        try:
            time_threshold = datetime.now() - timedelta(hours=96)
            self.etiquetado=Etiquetado.objects.get(pk=self.kwargs['pk'],grupo__anotacion__anotador=self.request.user,fecha_revision__gt=time_threshold).distinct()[:1].get()
            return True
        except Etiquetado.DoesNotExist:
            return False
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Etiquetado eliminado exitosamente"
    model=Etiquetado
    template_name="documentos/elimina_etiquetado.html"
class registro_Actividad_Revisiones(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Revisiones
    template_name = "documentos/lista_revisiones_registro_actividad.html"
    def get_queryset(self):
        time_threshold = datetime.now() - timedelta(hours=96)
        queryset=Revisiones.objects.filter(revisor=self.request.user,fecha_revision__gt=time_threshold).order_by('-fecha_revision')
        return queryset
class registro_Actividad_Elimina_Revision(UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    def test_func(self):
        try:
            time_threshold = datetime.now() - timedelta(hours=96)
            self.revision=Revisiones.objects.get(pk=self.kwargs['pk'],revisor=self.request.user,fecha_revision__gt=time_threshold)
            return True
        except Parrafos.DoesNotExist:
            return False
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Revision eliminada exitosamente"
    model=Parrafos
    template_name="documentos/elimina_revision.html"
class consulta_Documentos(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Leyes
    template_name = "documentos/consulta_documentos.html"
    def get_queryset(self):
        queryset=Leyes.objects.filter(captura_parrafos_finalizada=True)
        return queryset
class consulta_Documentos_Ley(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Parrafos
    template_name = "documentos/consulta_documentos_ley.html"
    def get_queryset(self):
        titulos=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=self.kwargs['pk']).values_list("titulo",flat=True).distinct()
        queryset=[]
        for titulo in titulos:
            try:
                parrafo_muestra=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=self.kwargs['pk'],titulo=titulo)[:1].get()
            except:
                continue
            queryset.append(parrafo_muestra)
        return queryset
class consulta_Documentos_Titulo(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Parrafos
    template_name = "documentos/consulta_documentos_titulo.html"
    def get_queryset(self):
        parrafo_base=Parrafos.objects.get(pk=self.kwargs['pk'])
        capitulos=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=parrafo_base.ley,titulo=parrafo_base.titulo).values_list("capitulo",flat=True).distinct()
        queryset=[]
        for capitulo in capitulos:
            try:
                parrafo_muestra=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=parrafo_base.ley,titulo=parrafo_base.titulo,capitulo=capitulo)[:1].get()
            except:
                continue
            queryset.append(parrafo_muestra)
        return queryset
class consulta_Documentos_Capitulo(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Parrafos
    template_name = "documentos/consulta_documentos_capitulo.html"
    def get_queryset(self):
        parrafo_base=Parrafos.objects.get(pk=self.kwargs['pk'])
        bases=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=parrafo_base.ley,titulo=parrafo_base.titulo,capitulo=parrafo_base.capitulo).values_list("base",flat=True).distinct()
        queryset=[]
        for base in bases:
            try:
                parrafo_muestra=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=parrafo_base.ley,titulo=parrafo_base.titulo,capitulo=parrafo_base.capitulo,base=base)[:1].get()
            except:
                continue
            queryset.append(parrafo_muestra)
        return queryset
class consulta_Documentos_Base(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Parrafos
    template_name = "documentos/consulta_documentos_base.html"
    def get_queryset(self):
        parrafo_base=Parrafos.objects.get(pk=self.kwargs['pk'])
        apartados=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=parrafo_base.ley,titulo=parrafo_base.titulo,capitulo=parrafo_base.capitulo,base=parrafo_base.base).values_list("apartado",flat=True).distinct()
        queryset=[]
        for apartado in apartados:
            try:
                parrafo_muestra=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=parrafo_base.ley,titulo=parrafo_base.titulo,capitulo=parrafo_base.capitulo,base=parrafo_base.base,apartado=apartado)[:1].get()
            except:
                continue
            queryset.append(parrafo_muestra)
        return queryset
class consulta_Documentos_Apartado(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Parrafos
    template_name = "documentos/consulta_documentos_apartado.html"
    def get_queryset(self):
        parrafo_base=Parrafos.objects.get(pk=self.kwargs['pk'])
        articulos=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=parrafo_base.ley,titulo=parrafo_base.titulo,capitulo=parrafo_base.capitulo,base=parrafo_base.base,apartado=parrafo_base.apartado).values_list("articulo",flat=True).distinct()
        queryset=[]
        for articulo in articulos:
            try:
                parrafo_muestra=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=parrafo_base.ley,titulo=parrafo_base.titulo,capitulo=parrafo_base.capitulo,base=parrafo_base.base,apartado=parrafo_base.apartado,articulo=articulo)[:1].get()
            except:
                continue
            queryset.append(parrafo_muestra)
        return queryset
class consulta_Documentos_Articulo(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Parrafos
    template_name = "documentos/consulta_documentos_articulo.html"
    def get_queryset(self):
        parrafo_base=Parrafos.objects.get(pk=self.kwargs['pk'])
        fracciones=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=parrafo_base.ley,titulo=parrafo_base.titulo,capitulo=parrafo_base.capitulo,base=parrafo_base.base,apartado=parrafo_base.apartado,articulo=parrafo_base.articulo).values_list("fraccion",flat=True).distinct()
        queryset=[]
        for fraccion in fracciones:
            try:
                parrafo_muestra=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=parrafo_base.ley,titulo=parrafo_base.titulo,capitulo=parrafo_base.capitulo,base=parrafo_base.base,apartado=parrafo_base.apartado,articulo=parrafo_base.articulo,fraccion=fraccion)[:1].get()
            except:
                continue
            queryset.append(parrafo_muestra)
        return queryset
class consulta_Documentos_Fraccion(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Parrafos
    template_name = "documentos/consulta_documentos_fraccion.html"
    def get_queryset(self):
        parrafo_base=Parrafos.objects.get(pk=self.kwargs['pk'])
        incisos=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=parrafo_base.ley,titulo=parrafo_base.titulo,capitulo=parrafo_base.capitulo,base=parrafo_base.base,apartado=parrafo_base.apartado,articulo=parrafo_base.articulo,fraccion=parrafo_base.fraccion).values_list("inciso",flat=True).distinct()
        queryset=[]
        for inciso in incisos:
            try:
                parrafo_muestra=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=parrafo_base.ley,titulo=parrafo_base.titulo,capitulo=parrafo_base.capitulo,base=parrafo_base.base,apartado=parrafo_base.apartado,articulo=parrafo_base.articulo,fraccion=parrafo_base.fraccion,inciso=inciso)[:1].get()
            except:
                continue
            queryset.append(parrafo_muestra)
        return queryset
class consulta_Documentos_Inciso(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model=Parrafos
    template_name = "documentos/consulta_documentos_inciso.html"
    def get_queryset(self):
        parrafo_base=Parrafos.objects.get(pk=self.kwargs['pk'])
        parrafos=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=parrafo_base.ley,titulo=parrafo_base.titulo,capitulo=parrafo_base.capitulo,base=parrafo_base.base,apartado=parrafo_base.apartado,articulo=parrafo_base.articulo,fraccion=parrafo_base.fraccion,inciso=parrafo_base.inciso).values_list("parrafo",flat=True).distinct()
        queryset=[]
        for parrafo in parrafos:
            try:
                parrafo_muestra=Parrafos.objects.filter(ley__captura_parrafos_finalizada=True,ley=parrafo_base.ley,titulo=parrafo_base.titulo,capitulo=parrafo_base.capitulo,base=parrafo_base.base,apartado=parrafo_base.apartado,articulo=parrafo_base.articulo,fraccion=parrafo_base.fraccion,inciso=parrafo_base.inciso,parrafo=parrafo)[:1].get()
            except:
                continue
            queryset.append(parrafo_muestra)
        return queryset
