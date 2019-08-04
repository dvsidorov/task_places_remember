# coding: utf-8


""" Test for layer_business.
"""


__author__ = 'Sidorov D.V.'


import django


django.setup()


import pytest
from layer_business.places import PlacesBL


@pytest.mark.run(order=0)
def test_place_create():
    place = {
        'name': 'Встреча выпускников',
        'comment': 'Комментарий',
        'latitude': '56.8908',
        'longitude': '61.7827'
    }
    place_id = PlacesBL.create(**place)
    read_place = PlacesBL.read(place_id)
    del read_place['place_id']
    assert read_place == place


@pytest.mark.run(order=1)
def test_place_list():
    places = PlacesBL.list()
    assert places is not None


@pytest.mark.run(order=2)
def test_place_update():
    place = {
        'name': 'Встреча выпускников',
        'comment': 'Комментарий',
        'latitude': '82.8908',
        'longitude': '61.7827'
    }

    place_list = PlacesBL.list()
    place_id = place_list[0].pk if place_list else None
    assert place_id is not None

    PlacesBL.update(place_id, **place)

    read_place = PlacesBL.read(place_id)
    del read_place['place_id']
    assert read_place == place


@pytest.mark.run(order=3)
def test_place_delete():
    place_list = PlacesBL.list()
    place_id = place_list[0].pk if place_list else None
    assert place_id is not None

    PlacesBL.remove(place_id)
    place = PlacesBL.read(place_id)
    assert place is None
