from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('fileuploader.views',
    url(r'^$', 'smart_search', name='index'),
    url(r'^upload$', 'upload', name='upload_form'),
    url(r'^uploads/(?P<pk>\d+)', 'dl_upload', name='upload_dl'),
    url(r'^advanced_search/$', views.UploadList.as_view(), name='advanced_search'),
    url(r'^smart_search/$', 'smart_search', name='smart_search'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
)
