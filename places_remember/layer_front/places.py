# coding: utf-8


import json

from django import forms
from django.conf import settings
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
    def _place_data_validator(value, default):
        return json.loads(value) if value else default


class PlaceBaseViewMixin:

    @staticmethod
    def _form_data_to_dict(form):
        return {k: form.data.get(k) for k, v in form.fields.items()}

    @staticmethod
    def _validate_form(forms=None):
        validate = True
        for form in forms:
            validate = validate and form.is_valid()
        return validate

    def _render_popup_response(self, data=None):
        self.data_popup = data or {}
        return self._render()

    @staticmethod
    def _set_form_attr(data=None, initial=None, readonly=None):
        options = {}
        if data:
            options.update({'data': data})
        if initial:
            options.update({'initial': initial})
        if readonly:
            options.update({'readonly': True})
        return options

    def _set_place_form(self, data=None, initial=None, readonly=None):
        options = self._set_form_attr(data=data, initial=initial, readonly=readonly)
        self.place_form = PlaceForm(**options)

    @staticmethod
    def _read_place(place_id):
        data = None
        if place_id:
            data = PlacesBL.read(place_id=place_id)
        return data


class PlaceCreateView(BaseView, PlaceBaseViewMixin, PlaceValidatorMixin):

    template_popup = {}
    data_popup = {}
    context_processors = []
    template_name = 'layer_front/place_inside.html'
    redirect_uri = '/place/list/'
    action = 'create'

    kwargs_params_slots = {}

    request_params_slots = {
        'place_data': [None, None],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'place_form': None,
            'maps_key': None,
            'action': None
        }
        self.place_form = None
        super().__init__(*args, **kwargs)

    def _set_maps_key(self):
        self.maps_key = settings.YANDEX_MAPS_KEY

    def post(self, *args, **kwargs):
        self._set_place_form(data=(self.params_storage['place_data'] or {}))
        if self._validate_form([self.place_form]):
            place = self._form_data_to_dict(self.place_form)
            PlacesBL.create(**place)
            return self._render_popup_response(data={'status': 302, 'redirect_uri': self.redirect_uri})
        self._aggregate()
        return self._render()

    def get(self, *args, **kwargs):
        self._set_place_form(data=(self.params_storage['place_data'] or {}))
        self._aggregate()
        return self._render()


class PlaceUpdateView(BaseView, PlaceBaseViewMixin, PlaceValidatorMixin):

    template_popup = {}
    data_popup = {}
    context_processors = []
    template_name = 'layer_front/place_inside.html'
    redirect_uri = '/place/list/'
    action = 'update'

    kwargs_params_slots = {
        'place_id': [None, None],
    }

    request_params_slots = {
        'place_data': [None, None],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'place_form': None,
            'maps_key': None
        }
        self.place_form = None
        self.place_id = None
        super().__init__(*args, **kwargs)

    def _render_popup_response(self, data=None):
        self.data_popup = data or {}
        return self._render()

    def post(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        data = self._read_place(self.params_storage['place_id'])
        self.place_id = data.get('place_id')

        self._set_place_form(initial=data)
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
        'place_data': [None, None],
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
    template_name = 'layer_front/place_list.html'

    kwargs_params_slots = {}

    request_params_slots = {}

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'place_list': None
        }
        self.place_form = None
        super().__init__(*args, **kwargs)

    def _render_popup_response(self, data=None):
        self.data_popup = data or {}
        return self._render()

    def _set_place_list(self):
        self.place_list = PlacesBL.list()

    def post(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        self._set_place_list()
        self._aggregate()
        return self._render()
