# coding: utf-8


from django.forms.models import model_to_dict

from layer_model.models import Place
from .base import BaseLogicEntity


class PlacesBL(BaseLogicEntity):

    @staticmethod
    def _place_validate(**field_values):
        return field_values

    @staticmethod
    def list(user_id):
        return Place.objects.filter(user_id=user_id).all()

    @classmethod
    def create(cls, **place):
        place_fields = cls._place_validate(**place)
        place = Place(**place_fields)
        place.save()
        return place.pk

    @staticmethod
    def read(place_id, user_id):
        place = Place.objects.filter(place_id=place_id, user_id=user_id).first()
        return model_to_dict(place)

    @classmethod
    def update(cls, place_id, user_id, place=None):
        place_fields = cls._place_validate(**place)
        place = Place.objects.filter(place_id=place_id, user_id=user_id).update(**place_fields)
        return place

    @classmethod
    def remove(cls, place_id, user_id):
        Place.objects.filter(place_id=place_id, user_id=user_id).delete()
        return True
