"""shop_ultra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf.urls import url, include
from .views import PlaceCreateView, PlaceUpdateView, PlaceDeleteView, PlaceListView, LoginView, LogoutView


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^create/popup/$', PlaceCreateView.as_view(popup=True), name='place_create_popup'),
    url(r'^create/$', PlaceCreateView.as_view(), name='place_create'),

    url(r'^update/popup/(?P<place_id>.*)/$', PlaceUpdateView.as_view(popup=True), name='place_update_popup'),
    url(r'^update/(?P<place_id>.*)/$', PlaceUpdateView.as_view(), name='place_update'),

    url(r'^delete/popup/(?P<place_id>.*)/$', PlaceDeleteView.as_view(popup=True), name='place_delete_popup'),

    url(r'^$', PlaceListView.as_view(), name='place_list'),
    url(r'', include('social_django.urls', namespace='social')),
]
