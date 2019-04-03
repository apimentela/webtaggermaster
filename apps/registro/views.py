# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect #, reverse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate, logout
from django.views.generic import TemplateView
from django.contrib.sessions.models import Session
from tracking.models import Visitor
from datetime import datetime
from models  import Sesiones
def home(request):
    print("home request")
    if request.user.is_authenticated():
        print("el usuario esta autenticado")
        return redirect(reverse('usuarios_app:perfil_home'))
    return redirect(reverse('registro_app:login'))
def do_login(request):
    template_name = "login.html"
    print("do_login request")
    if request.user.is_authenticated():
        print("el usuario esta autenticado")
        return redirect(reverse('usuarios_app:perfil_home'))
    if request.method == 'GET':
        return render(request, template_name, context={})
    elif request.method == 'POST':
        print('metodo post')
        usuario = authenticate(username=request.POST.get('username', ''),
                               password=request.POST.get('password', ''))
        if usuario:
            login(request, usuario)
            ip_address = request.META.get('REMOTE_ADDR','')
            now1=datetime.now()
            last_login = request.user.last_login
            now2=datetime.now()
            print(now1)
            if unicode(last_login)[:19] == unicode(now1)[:19] or unicode(last_login)[:19] == unicode(now2)[:19]:
                previous_visitors = Visitor.objects.filter(user=request.user).exclude(ip_address=ip_address)
                for visitor in previous_visitors:
                    Session.objects.filter(session_key=visitor.session_key).delete()
                    visitor.user = None
                    visitor.save()
            try:
                nueva_sesion=Sesiones(usuario=request.user,inicio=request.user.last_login)
                nueva_sesion.save()
                print("nueva sesión iniciada")
            except: pass
            print("login correcto")
            return redirect(reverse('usuarios_app:perfil_home'))
        else:
            return render(request, template_name,
                          context={'error':'Las claves proporcionadas son incorrectas'})
    return render(request, template_name=template_name,
                  context={})
def do_logout(request):
    print("do_logout request")
    logout(request)
    return redirect(reverse('registro_app:home'))
