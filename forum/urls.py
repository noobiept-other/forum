"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [

    url( r'^$', 'forum.views.index', name= 'index' ),
    url( r'^forum/(?P<forumSlug>[\w-]+)/(?P<page>[0-9]+)$', 'forum.views.sub_forum', name= 'subForum' ),
    url( r'^thread/(?P<threadSlug>[\w-]+)/(?P<page>[0-9]+)$', 'forum.views.open_thread', name= 'thread' ),

    url( r'^new_thread/(?P<forumSlug>[\w-]+)$', 'forum.views.new_thread', name= 'new_thread' ),
    url( r'^new_category$', 'forum.views.new_category', name= 'new_category' ),
    url( r'^new_sub_forum/(?P<categorySlug>[\w-]+)$', 'forum.views.new_sub_forum', name= 'new_sub_forum' ),

    url( r'^lock_thread/(?P<threadSlug>[\w-]+)$', 'forum.views.lock_thread', name= 'lock_thread' ),

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

    url( r'^users_list$', 'forum.views.users_list', name= 'users_list' ),

    url( r'^accounts/', include( 'accounts.urls', namespace= 'accounts', app_name= 'accounts' ) ),
    url( r'^admin/', include( admin.site.urls ) ),
]


    # Serve static files when debug false
if not settings.DEBUG:
    urlpatterns += [
        url( r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT } ),
    ]
