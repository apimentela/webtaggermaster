from django.conf.urls import url
from django.contrib import admin
from .views import (PerfilView, AnotadorView, RevisorView,registro,acceso_denegado)
from .cbv import (lista_Usuarios,actualiza_Usuario,elimina_Usuario)
usuarios_urls = [
    url(r'^perfil$', PerfilView, name='perfil_home'),
    url(r'^anotador$', AnotadorView, name='anotador_home'),
    url(r'^revisor$', RevisorView, name='revisor_home'),
    url(r'^registro/$', registro, name='registro'),
    url(r'^acceso_denegado/$', acceso_denegado, name='acceso_denegado'),
    url(r'^administra_usuarios$', lista_Usuarios.as_view(), name='administra_usuarios'),
    url(r'^administra_usuario_(?P<pk>\d+)$', actualiza_Usuario.as_view(success_url="/administra_usuarios"), name='administra_usuario'),
    url(r'^elimina_usuario_(?P<pk>\d+)$', elimina_Usuario.as_view(success_url="/administra_usuarios"), name='elimina_usuario'),
]
