from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone

import datetime

class Category( models.Model ):

    name = models.CharField( max_length= 100, unique= True )
    slug = models.SlugField( max_length= 100, unique= True )

    def __unicode__(self):
        return self.name


class SubForum( models.Model ):

    name = models.CharField( max_length= 100, unique= True )
    slug = models.SlugField( max_length= 100, unique= True )
    category = models.ForeignKey( Category )

    def __unicode__(self):
        return self.name

    def get_url(self):
        return reverse( 'subForum', args= [ self.slug ] )

    def get_last_post(self):

        try:
            latest = self.post_set.latest( 'date_created' )

        except Post.DoesNotExist:
            try:
                latest = self.thread_set.latest( 'date_created' )

            except Thread.DoesNotExist:
                return None

        return latest



class Thread( models.Model ):

    sub_forum = models.ForeignKey( SubForum )
    user = models.ForeignKey( settings.AUTH_USER_MODEL )
    title = models.CharField( max_length= 100 )
    slug = models.SlugField( max_length= 100, unique= True )    # for the url
    text = models.TextField( max_length= 1000 )
    date_created = models.DateTimeField( help_text= 'Date Created', default= datetime.datetime.now )

    def __unicode__(self):
        return self.title

    def get_url(self):
        return reverse( 'thread', args= [ self.slug ] )

    def get_last_post(self):

        try:
            latest = self.post_set.latest( 'date_created' )

        except Post.DoesNotExist:
            latest = None

        return latest


class Post( models.Model ):

    sub_forum = models.ForeignKey( SubForum )
    thread = models.ForeignKey( Thread )
    user = models.ForeignKey( settings.AUTH_USER_MODEL )
    text = models.TextField( max_length= 1000 )
    date_created = models.DateTimeField( help_text= 'Date Created', default= datetime.datetime.now )

    def __unicode__(self):
        return self.text[:10]

    def get_url(self):
        position = 0

        for index, post in enumerate( self.thread.post_set.all() ):
            if post == self:
                position = index

        url = reverse( 'thread', args= [ self.thread.slug ] )

        url += '#post_' + str( position + 1 )

        return url

class Profile( AbstractUser ):

    is_moderator = models.BooleanField( default= False )

    def get_url(self):

        return reverse( 'user_page', args= [ self.username ] )


class PrivateMessage( models.Model ):

    receiver = models.ForeignKey( settings.AUTH_USER_MODEL )
    sender = models.ForeignKey( settings.AUTH_USER_MODEL, related_name= 'sender' )
    title = models.TextField( max_length= 100 )
    content = models.TextField( max_length= 500 )

    def __unicode__(self):
        return self.title