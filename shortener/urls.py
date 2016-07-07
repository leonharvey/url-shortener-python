from django.conf.urls import url

from . import views

app_name = 'shortener'

urlpatterns = [
    url(r'^$', views.IndexView, name='index'),
    url(r'^add/?', views.AddLink, name='add_link'),
    url(r'^(?P<identifier>[0-9A-Za-z]+)$', views.LinkHandler, name='redirect_link'),
]