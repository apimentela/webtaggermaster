from datetime import datetime
from django.utils.timezone import make_aware    # Esto es para evitar un Warning de que no se tomaba en cuenta la zona horaria
from models  import Sesiones
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
class UpdateSessionEnd(object):
    def process_request(self, request):
        if request.path.startswith(reverse('admin:index')):
            return None
        try:
            last_login = request.user.last_login
            print(last_login)
        except: return None
        try:
            sesion=Sesiones.objects.get(usuario=request.user,inicio=request.user.last_login)
            time_now=make_aware(datetime.now())
            print(time_now)
            sesion.fin=time_now
            sesion.save()
            print("sesion actualizada")
        except:
            logout(request)
            return redirect(reverse('registro_app:home'))
