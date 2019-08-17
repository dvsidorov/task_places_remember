# coding: utf-8


from django.db import models
from django.conf import settings


USER_MODEL = getattr(settings, 'USER_MODEL', None) or \
             getattr(settings, 'AUTH_USER_MODEL', None) or \
             'auth.User'


class Place(models.Model):

    place_id = models.AutoField(primary_key=True, auto_created=True)

    user = models.ForeignKey(USER_MODEL, null=False, blank=False,
                             related_name='user_places', on_delete=models.CASCADE)

    name = models.CharField(verbose_name='Название', max_length=150)
    comment = models.TextField(verbose_name='Комментарий', max_length=250, null=True, blank=True)
    latitude = models.CharField(verbose_name='Широта', max_length=20, null=False, blank=False)
    longitude = models.CharField(verbose_name='Долгота', max_length=20, null=False, blank=False)
