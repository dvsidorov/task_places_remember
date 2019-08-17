# coding: utf-8


""" Test for layer_business.
"""


__author__ = 'Sidorov D.V.'


import django


django.setup()


import pytest
from django.conf import settings
from django.contrib.auth.models import User
from layer_business.places import PlacesBL


@pytest.fixture(scope="module")
def create_user():
    user = User.objects.first()
    if not user:
        user = User(username='TestUser')
        user.save()
    return user.pk


@pytest.mark.run(order=0)
@pytest.mark.parametrize(
    "name,comment,latitude,longitude", [
        ('Встреча выпускников', 'хорошо', '56.8908', '61.7827'),
        ('Встреча одноклассников', 'не очень', '57.8908', '61.7827'),
        ('Встреча студентов', 'было весело', '56.8908', '60.7827'),
        ('Встреча работников', 'грусть печаль', '56.8908', '60.7827'),
])
def test_place_create(create_user, name, comment, latitude, longitude):
    place = {
        'user_id': create_user,
        'name': name,
        'comment': comment,
        'latitude': latitude,
        'longitude': longitude
    }
    place_id = PlacesBL.create(**place)
    read_place = PlacesBL.read(place_id, user_id=create_user)
    del read_place['place_id']
    assert read_place == place


@pytest.mark.run(order=1)
def test_place_list(create_user):
    places = PlacesBL.list(user_id=create_user)
    assert places is not None


@pytest.mark.run(order=2)
def test_place_update(create_user):
    place_list = PlacesBL.list(user_id=create_user)
    place_id = place_list[0].pk if place_list else None
    place = PlacesBL.read(place_id=place_id, user_id=create_user)
    assert place_id is not None

    place['name'] = place['name'][::-1]
    PlacesBL.update(**place)
    del place['place_id']

    read_place = PlacesBL.read(place_id=place_id, user_id=create_user)
    del read_place['place_id']
    assert read_place == place


@pytest.mark.run(order=3)
def test_place_delete(create_user):
    place_list = PlacesBL.list(create_user)
    place_id = place_list[0].pk if place_list else None
    assert place_id is not None

    PlacesBL.remove(place_id, user_id=create_user)
    place = PlacesBL.read(place_id, user_id=create_user)
    assert place is None
