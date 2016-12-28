from django.conf.urls import url
from web import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^tenso/(?P<pk>[0-9]+)/?$', views.TensoView.as_view(), name='tenso'),
]
