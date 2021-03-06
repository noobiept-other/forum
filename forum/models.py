from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone


def getTime():
    return timezone.localtime( timezone.now() )


class Category( models.Model ):

    name = models.CharField( max_length= 50, unique= True )
    slug = models.SlugField( max_length= 50, unique= True )

    def __str__(self):
        return self.name


class SubForum( models.Model ):

    name = models.CharField( max_length= 50, unique= True )
    slug = models.SlugField( max_length= 50, unique= True )
    category = models.ForeignKey( Category )

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse( 'subForum', args= [ self.slug, 0 ] )

    def get_last_post(self):

        try:
            latest = self.post_set.latest( 'date_created' )

        except Post.DoesNotExist:
            try:
                latest = self.thread_set.latest( 'date_created' )

            except Thread.DoesNotExist:
                return None

        return latest

    def get_threads_count(self):
        return self.thread_set.count()


class Thread( models.Model ):

    sub_forum = models.ForeignKey( SubForum )
    user = models.ForeignKey( settings.AUTH_USER_MODEL )
    title = models.CharField( max_length= 50 )
    slug = models.SlugField( max_length= 50, unique= True )    # for the url
    text = models.TextField( max_length= 1000 )
    date_created = models.DateTimeField( help_text= 'Date Created', default= getTime )
    was_edited = models.BooleanField( default= False )
    date_edited = models.DateTimeField( help_text= 'Last time the post was edited ', default= getTime )
    edited_by = models.ForeignKey( settings.AUTH_USER_MODEL, help_text= 'who edited the thread.', blank= True, null= True, related_name= 'thread_edited_by' )
    is_locked = models.BooleanField( default= False, help_text= 'if you can add new posts to the thread or not.' )

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse( 'thread', args= [ self.slug, 0 ] )

    def get_last_post(self):

        try:
            latest = self.post_set.latest( 'date_created' )

        except Post.DoesNotExist:
            latest = None

        return latest

    def get_post_count(self):
        return self.post_set.all().count()


class Post( models.Model ):

    sub_forum = models.ForeignKey( SubForum )
    thread = models.ForeignKey( Thread )
    user = models.ForeignKey( settings.AUTH_USER_MODEL )
    text = models.TextField( max_length= 1000 )
    was_edited = models.BooleanField( default= False )
    date_created = models.DateTimeField( help_text= 'Date Created', default= getTime )
    date_edited = models.DateTimeField( help_text= 'Last time the post was edited ', default= getTime )
    edited_by = models.ForeignKey( settings.AUTH_USER_MODEL, help_text= 'who edited the post.', blank= True, null= True, related_name= 'post_edited_by' )

    def __str__(self):
        return self.text[ :10 ]

    def get_url(self):
        position = 0

        for index, post in enumerate( self.thread.post_set.all() ):
            if post == self:
                position = index

        postsPerPage = settings.POSTS_PER_PAGE
        page = 0

        while position >= postsPerPage:
            position -= postsPerPage
            page += 1

        url = reverse( 'thread', args= [ self.thread.slug, page ] )

        url += '#post_' + str( position + 1 )

        return url
