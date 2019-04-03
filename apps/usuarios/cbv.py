from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.forms import ModelForm
from django.views.generic import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .tests import en_grupo_administradores
class lista_Usuarios(UserPassesTestMixin,ListView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    model=User
    template_name = "usuarios/lista_usuarios.html"
class actualiza_Usuario_Form(ModelForm):
    class Meta:
        model=User
        fields=["username","first_name","last_name","email","groups","is_active"]
class actualiza_Usuario(UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Usuario actualizado exitosamente"
    model=User
    template_name="usuarios/actualiza_usuario.html"
    form_class=actualiza_Usuario_Form
class elimina_Usuario(UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    def test_func(self):
        return en_grupo_administradores(self.request.user)
    def get_login_url(self):
        return '/acceso_denegado/'
    success_message="Usuario eliminado exitosamente"
    model=User
    template_name="usuarios/elimina_usuario.html"
