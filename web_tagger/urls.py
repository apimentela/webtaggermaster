from django.conf.urls import url, include
from django.contrib import admin
from apps.registro.urls import registro_urls
from apps.usuarios.urls import usuarios_urls
from apps.documentos.urls import documentos_urls
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^', include(registro_urls,namespace='registro_app')),
    url(r'^', include(usuarios_urls,namespace='usuarios_app')),
    url(r'^', include(documentos_urls,namespace='documentos_app')),
    url('^', include('django.contrib.auth.urls')),	
    url(r'session_security/', include('session_security.urls')),	
    url(r'^jet/', include('jet.urls', namespace='jet')),  
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  
    url(r'^admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
