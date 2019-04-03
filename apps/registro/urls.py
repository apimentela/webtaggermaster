from django.conf.urls import url,include
from .views import (home, do_login, do_logout)
registro_urls = [
    url(r'^$', home, name='home'),
    url(r'^index$', home, name='home'),
    url(r'^login$', do_login, name='login'),
    url(r'^accounts/login/$', do_login, name='login'),
    url(r'^logout$', do_logout, name='logout')
]
