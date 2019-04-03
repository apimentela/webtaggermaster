from __future__ import unicode_literals
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
Group.objects.get_or_create(name='anotadores') 
Group.objects.get_or_create(name='administradores') 
class Command(BaseCommand):
    help = 'Crea los grupos por defecto'
    def handle(self, *args, **options):
        Group.objects.get_or_create(name='anotadores') 
        Group.objects.get_or_create(name='administradores') 
        print("Grupos creados")
