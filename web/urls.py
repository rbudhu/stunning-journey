from django.conf.urls import url
from web import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^tenso/(?P<pk>[0-9]+)/?$', views.TensoView.as_view(), name='tenso'),
    url(r'^privacy/?$', views.PrivacyView.as_view(), name='privacy'),
    url(r'^share_tenso/?$', views.ShareView.as_view(), name='share_tenso'),
    url(r'^js/web/urls.js', views.URLView.as_view(content_type='text/javascript'), name='urls')
]
