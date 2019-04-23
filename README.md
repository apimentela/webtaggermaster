# webtaggermaster

Hay un requerimiento con errores de pip, se debe instalar de la siguiente manera:

  pip install git+https://github.com/bashu/django-tracking.git

Para crear los grupos iniciales de administradores y anotadores se debe correr una sola vez:

  python manage.py makemigrations
  python manage.py makemigrations registro
  python manage.py makemigrations documentos
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py grupos_iniciales

El programa que se debe ejectuar a diario para la obtención de concordancias es:

  python manage.py concordancias_json
