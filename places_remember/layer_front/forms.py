# coding: utf-8


import json

from django import forms
from layer_front.base import BaseForm, field_factory


class PlaceForm(BaseForm):

    name = field_factory(forms.CharField(label='Название',
                                         required=True,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'Введите название места'}),
                                         error_messages={'required': "Введите название места"}),
                         'text')
    comment = field_factory(forms.CharField(label='Комментарий',
                                            required=False,
                                            widget=forms.Textarea(attrs={'class': 'form-control',
                                                                         'placeholder': 'Введите комментарий'}),
                                            error_messages={'required': "Введите комментарий"}),
                            'text')
    latitude = forms.CharField(label='Широта',
                               required=True,
                               widget=forms.HiddenInput)
    longitude = forms.CharField(label='Долгота',
                                required=True,
                                widget=forms.HiddenInput)

    field_order = ['name', 'comment', 'latitude', 'longitude']
