# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-04-23 18:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sesiones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateTimeField(verbose_name='Inicio')),
                ('fin', models.DateTimeField(null=True, verbose_name='Fin')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Sesiones', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='sesiones',
            unique_together=set([('usuario', 'inicio')]),
        ),
    ]
