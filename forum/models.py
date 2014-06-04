from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import datetime

class Category( models.Model ):

    name = models.CharField( max_length= 100, unique= True )

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
            latest = self.thread_set.latest( 'date_created' )

        return latest



class Thread( models.Model ):

    sub_forum = models.ForeignKey( SubForum )
    user = models.ForeignKey( User )
    title = models.CharField( max_length= 100 )
    slug = models.SlugField( max_length= 100, unique= True )    # for the url
    text = models.TextField( max_length= 1000 )
    date_created = models.DateTimeField( help_text= 'Date Created', default= datetime.datetime.now )

    def __unicode__(self):
        return self.title

    def get_url(self):
        return reverse( 'thread', args= [ self.sub_forum.slug, self.slug ] )

    def get_last_post(self):

        try:
            latest = self.post_set.latest( 'date_created' )

        except Post.DoesNotExist:
            latest = None

        return latest


class Post( models.Model ):

    sub_forum = models.ForeignKey( SubForum )
    thread = models.ForeignKey( Thread )
    user = models.ForeignKey( User )
    text = models.TextField( max_length= 1000 )
    date_created = models.DateTimeField( help_text= 'Date Created', default= datetime.datetime.now )

    def __unicode__(self):
        return self.text[:10]