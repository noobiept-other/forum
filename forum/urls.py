from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url( r'^$', 'forum.views.index', name= 'index' ),

    url( r'^forum/(?P<forumSlug>[\w-]+)/?$', 'forum.views.sub_forum', name= 'subForum' ),

    url( r'^forum/(?P<forumSlug>[\w-]+)/(?P<threadSlug>[\w-]+)/?$', 'forum.views.thread', name= 'thread' ),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
