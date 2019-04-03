# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
class CustomUserCreationForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    sudo = forms.BooleanField(label='Es administrador',required=False)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("E-mail ya existe")
        return email
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden")
        return password2
    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        if self.cleaned_data.get('sudo'):
            group = Group.objects.get(name='administradores')
        else:
            group = Group.objects.get(name='anotadores')
        user.groups.add(group)
        return user
