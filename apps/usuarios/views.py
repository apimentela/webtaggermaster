from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from .forms import CustomUserCreationForm
from .tests import en_grupo_administradores
@login_required
def PerfilView(request):
    print("Home del Usuario anotador")
    anotaciones_pendientes = request.user.anotador.filter(is_done=False)
    revisiones_pendientes = request.user.revisor.filter(is_done=False)
    return render(request, template_name='usuarios/perfil.html',)
@login_required
def AnotadorView(request):
    print("Home del Usuario anotador")
    return render(request, template_name='usuarios/anotador.html',
                  context={})
@login_required
def RevisorView(request):
    print("Home del Usuario revisor")
    return render(request, template_name='usuarios/revisor.html',
                  context={})
def acceso_denegado(request):
	return HttpResponse ("Acceso Denegado!")
@login_required
@user_passes_test(en_grupo_administradores, login_url='/acceso_denegado/')
def registro(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Cuenta de usuario creada')
            return redirect(reverse('usuarios_app:registro'))
    else:
        f = CustomUserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': f})
