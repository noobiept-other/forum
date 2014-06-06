from django.contrib import admin

from forum.models import Category, SubForum, Thread, Post, Profile, PrivateMessage

class CategoryAdmin( admin.ModelAdmin ):

    list_display = ( 'name', )

admin.site.register( Category, CategoryAdmin )


class SubForumAdmin( admin.ModelAdmin ):

    list_display = ( 'name', 'category' )
    prepopulated_fields = { 'slug': ( 'name', ) }

admin.site.register( SubForum, SubForumAdmin )


class ThreadAdmin( admin.ModelAdmin ):

    list_display = ( 'sub_forum', 'user', 'title', 'text', 'date_created' )
    prepopulated_fields = { 'slug': ( 'title', ) }

admin.site.register( Thread, ThreadAdmin )



class PostAdmin( admin.ModelAdmin ):

    list_display = ( 'thread', 'user', 'text', 'date_created' )

admin.site.register( Post, PostAdmin )


class ProfileAdmin( admin.ModelAdmin ):

    list_display = ( 'user', 'email' )

admin.site.register( Profile, ProfileAdmin )


class PrivateMessageAdmin( admin.ModelAdmin ):

    list_display = ( 'receiver', 'sender', 'title', 'content' )

admin.site.register( PrivateMessage, PrivateMessageAdmin )