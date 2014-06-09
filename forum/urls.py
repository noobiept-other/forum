from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url( r'^$', 'forum.views.index', name= 'index' ),

    url( r'^forum/(?P<forumSlug>[\w-]+)$', 'forum.views.sub_forum', name= 'subForum' ),

    url( r'^thread/(?P<threadSlug>[\w-]+)$', 'forum.views.thread', name= 'thread' ),

    url( r'new_thread/(?P<forumSlug>[\w-]+)', 'forum.views.new_thread', name= 'new_thread' ),
    url( r'new_category', 'forum.views.new_category', name= 'new_category' ),
    url( r'new_sub_forum/(?P<categorySlug>[\w-]+)', 'forum.views.new_sub_forum', name= 'new_sub_forum' ),


    url( r'^accounts/login$', 'django.contrib.auth.views.login', { 'template_name': 'accounts/login.html', 'redirect_field_name': '/' }, name= 'login' ),
    url( r'^accounts/logout$', 'django.contrib.auth.views.logout', { 'next_page': '/' }, name= 'logout' ),
    url( r'^accounts/new$', 'forum.views.new_account', name= 'new_account' ),

    url( r'^accounts/user/(?P<username>\w+)$', 'forum.views.user_page', name= 'user_page' ),

    url( r'^accounts/send_message/(?P<username>\w+)$', 'forum.views.send_private_message', name= 'send_message' ),

    url( r'^accounts/check_message/$', 'forum.views.check_message', name='check_message'),

    url( r'^accounts/check_message/(?P<messageId>\w+)$', 'forum.views.open_message', name= 'open_message' ),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
