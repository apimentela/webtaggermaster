from django.test import TestCase
def en_grupo_administradores(user):
    if user:
        return user.groups.filter(name='administradores').exists()
    return False
