# coding: utf-8


import json

from django import forms
from leon_base.base.views import BaseView
from layer_front.base import BaseForm, field_factory
from layer_business.places import PlacesBL


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


class PlaceValidatorMixin:

    @staticmethod
    def _place_id_validator(value, default):
        return value if value else default

    @staticmethod
    def _data_validator(value, default):
        return json.loads(value) if value else default


class PlaceCreateView(BaseView, PlaceValidatorMixin):

    template_popup = {}
    data_popup = {}
    context_processors = []
    template_name = 'place/place_inside.html'
    redirect_uri = '/place/list/'

    kwargs_params_slots = {
        'place_id': [None, None],
    }

    request_params_slots = {
        'data': [None, None],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'place_form': None
        }
        self.place_form = None
        super().__init__(*args, **kwargs)

    def _render_popup_response(self, data=None):
        self.data_popup = data or {}
        return self._render()

    def post(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        self._aggregate()
        return self._render()


class PlaceUpdateView(BaseView, PlaceValidatorMixin):

    template_popup = {}
    data_popup = {}
    context_processors = []
    template_name = 'place/place_inside.html'
    redirect_uri = '/place/list/'

    kwargs_params_slots = {
        'place_id': [None, None],
    }

    request_params_slots = {
        'data': [None, None],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'place_form': None
        }
        self.place_form = None
        super().__init__(*args, **kwargs)

    def _render_popup_response(self, data=None):
        self.data_popup = data or {}
        return self._render()

    def post(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        self._aggregate()
        return self._render()


class PlaceDeleteView(BaseView, PlaceValidatorMixin):

    template_popup = {}
    data_popup = {}
    context_processors = []
    template_name = 'place/place_inside.html'
    redirect_uri = '/place/list/'

    kwargs_params_slots = {
        'place_id': [None, None],
    }

    request_params_slots = {
        'data': [None, None],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'place_form': None
        }
        self.place_form = None
        super().__init__(*args, **kwargs)

    def _render_popup_response(self, data=None):
        self.data_popup = data or {}
        return self._render()

    def post(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        self._aggregate()
        return self._render()


class PlaceListView(BaseView, PlaceValidatorMixin):

    template_popup = {}
    data_popup = {}
    context_processors = []
    template_name = 'place/place_list.html'

    kwargs_params_slots = {
        'place_id': [None, None],
    }

    request_params_slots = {
        'data': [None, None],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'place_form': None
        }
        self.place_form = None
        super().__init__(*args, **kwargs)

    def _render_popup_response(self, data=None):
        self.data_popup = data or {}
        return self._render()

    def post(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        self._aggregate()
        return self._render()
