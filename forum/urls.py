from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url( r'^$', 'forum.views.index', name= 'index' ),
    url( r'^forum/(?P<forumSlug>[\w-]+)/(?P<page>[0-9]+)$', 'forum.views.sub_forum', name= 'subForum' ),
    url( r'^thread/(?P<threadSlug>[\w-]+)/(?P<page>[0-9]+)$', 'forum.views.open_thread', name= 'thread' ),

    url( r'^new_thread/(?P<forumSlug>[\w-]+)$', 'forum.views.new_thread', name= 'new_thread' ),
    url( r'^new_category$', 'forum.views.new_category', name= 'new_category' ),
    url( r'^new_sub_forum/(?P<categorySlug>[\w-]+)$', 'forum.views.new_sub_forum', name= 'new_sub_forum' ),

    url( r'^edit_post/(?P<postId>\w+)$', 'forum.views.edit_post', name= 'edit_post' ),
    url( r'^edit_thread/(?P<threadSlug>[\w-]+)$', 'forum.views.edit_thread', name= 'edit_thread' ),
    url( r'^edit_category/(?P<categorySlug>[\w-]+)$', 'forum.views.edit_category', name= 'edit_category' ),
    url( r'^edit_sub_forum/(?P<forumSlug>[\w-]+)$', 'forum.views.edit_sub_forum', name= 'edit_sub_forum' ),

    url( r'^remove/post_confirm/(?P<postId>\w+)$', 'forum.views.remove_post_confirm', name= 'remove_post_confirm' ),
    url( r'^remove/post/(?P<postId>\w+)$', 'forum.views.remove_post', name= 'remove_post' ),
    url( r'^remove/thread_confirm/(?P<threadSlug>[\w-]+)$', 'forum.views.remove_thread_confirm', name= 'remove_thread_confirm' ),
    url( r'^remove/thread/(?P<threadSlug>[\w-]+)$', 'forum.views.remove_thread', name= 'remove_thread' ),
    url( r'^remove/sub_forum_confirm/(?P<forumSlug>[\w-]+)$', 'forum.views.remove_sub_forum_confirm', name= 'remove_sub_forum_confirm' ),
    url( r'^remove/sub_forum/(?P<forumSlug>[\w-]+)$', 'forum.views.remove_sub_forum', name= 'remove_sub_forum' ),
    url( r'^remove/category_confirm/(?P<categorySlug>[\w-]+)$', 'forum.views.remove_category_confirm', name= 'remove_category_confirm' ),
    url( r'^remove/category/(?P<categorySlug>[\w-]+)$', 'forum.views.remove_category', name= 'remove_category' ),
    url( r'^remove/user_confirm/(?P<username>\w+)$', 'forum.views.remove_user_confirm', name= 'remove_user_confirm' ),
    url( r'^remove/user/(?P<username>\w+)$', 'forum.views.remove_user', name= 'remove_user' ),

    url( r'^accounts/login$', 'django.contrib.auth.views.login', { 'template_name': 'accounts/login.html' }, name= 'login' ),
    url( r'^accounts/logout$', 'django.contrib.auth.views.logout', name= 'logout' ),
    url( r'^accounts/new$', 'forum.views.new_account', name= 'new_account' ),
    url( r'^accounts/change_password$', 'django.contrib.auth.views.password_change', { 'template_name': 'accounts/change_password.html', 'post_change_redirect': '/' }, name= 'change_password' ),

    url( r'^accounts/user/(?P<username>\w+)$', 'forum.views.user_page', name= 'user_page' ),

    url( r'^accounts/send_message/(?P<username>\w+)$', 'forum.views.send_private_message', name= 'send_message' ),

    url( r'^accounts/check_message/$', 'forum.views.check_message', name='check_message'),

    url( r'^accounts/check_message/(?P<messageId>\w+)$', 'forum.views.open_message', name= 'open_message' ),
    url( r'^accounts/remove_message/(?P<messageId>\w+)$', 'forum.views.remove_message', name= 'remove_message' ),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
