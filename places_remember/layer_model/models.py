# coding: utf-8


from django.db import models


class Place(models.Model):

    place_id = models.AutoField(primary_key=True, auto_created=True)

    name = models.CharField(verbose_name='Название', max_length=150)
    comment = models.TextField(verbose_name='Комментарий', max_length=250, null=True, blank=True)
    latitude = models.CharField(verbose_name='Широта', max_length=10, null=False, blank=False)
    longitude = models.CharField(verbose_name='Долгота', max_length=10, null=False, blank=False)
