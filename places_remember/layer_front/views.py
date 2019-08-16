# coding: utf-8


import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, redirect
from leon_base.base.views import BaseView
from layer_front.forms import PlaceForm
from layer_business.places import PlacesBL


class LoginViewMixin(LoginRequiredMixin):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'


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


class PlaceCreateView(LoginRequiredMixin, BaseView, PlaceBaseViewMixin, PlaceValidatorMixin):

    template_popup = {
        'tbody': 'layer_front/popup/place_inside_popup_form.html'
    }
    data_popup = {}
    context_processors = []
    template_name = 'layer_front/place_inside.html'
    redirect_uri = '/'
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

    template_popup = {
        'tbody': 'layer_front/popup/place_inside_popup_form.html'
    }
    data_popup = {}
    context_processors = []
    template_name = 'layer_front/place_inside.html'
    redirect_uri = '/'
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
            'action': None,
            'place_id': None,
        }
        self.place_form = None
        self.place_id = None
        super().__init__(*args, **kwargs)

    def _render_popup_response(self, data=None):
        self.data_popup = data or {}
        return self._render()

    def post(self, *args, **kwargs):
        data = self._read_place(self.params_storage['place_id'])
        self.place_id = data.get('place_id')
        self._set_place_form(data=(self.params_storage['place_data'] or {}), initial=data, readonly=False)
        if self._validate_form([self.place_form]):
            place = self._form_data_to_dict(self.place_form)
            PlacesBL.update(place_id=self.place_id,
                            place=place)
            return self._render_popup_response(data={'status': 302, 'redirect_uri': self.redirect_uri})
        self._aggregate()
        return self._render()

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
    redirect_uri = '/'

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

    @staticmethod
    def _remove_place(place_id):
        return PlacesBL.remove(place_id=place_id)

    def post(self, *args, **kwargs):
        if self._remove_place(self.params_storage['place_id']):
            return self._render_popup_response(data={'status': 302, 'redirect_uri': self.redirect_uri})
        return self._render_popup_response(data={'status': 400})


class PlaceListView(LoginViewMixin, BaseView, PlaceValidatorMixin):

    template_popup = {}
    data_popup = {}
    context_processors = []
    template_name = 'layer_front/place_list.html'

    kwargs_params_slots = {}

    request_params_slots = {}

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'place_list': None,
            'request': None,
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


class LoginView(BaseView):

    template_popup = {}
    data_popup = {}
    context_processors = []
    template_name = 'layer_front/login.html'

    kwargs_params_slots = {}

    request_params_slots = {}

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
        }
        self.place_form = None
        super().__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        self._aggregate()
        return self._render()


class LogoutView(BaseView):

    template_popup = {}
    data_popup = {}
    context_processors = []
    kwargs_params_slots = {}
    request_params_slots = {}

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
        }
        self.place_form = None
        super().__init__(*args, **kwargs)

    def _clean_session(self):
        self.request.session.flush()

    def get(self, *args, **kwargs):
        self._clean_session()
        return redirect('place_list')
