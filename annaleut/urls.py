from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from django_notify.urls import get_pattern as get_notify_pattern
from wiki.urls import get_pattern as get_wiki_pattern


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'annaleut.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'', include('fileuploader.urls')),

    url(r'^admin/login/$', 'fileuploader.views.adminlogin'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django_cas.views.login'), 
    url(r'^logout/$', 'django_cas.views.logout'),
    
    url(r'^notify/', get_notify_pattern()),
    url(r'wiki/', get_wiki_pattern()),
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = patterns('',
    url(r'annaleut/', include(urlpatterns)),
)
