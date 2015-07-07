from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse


class Account( AbstractUser ):

    is_moderator = models.BooleanField( default= False )

    def get_url(self):
        return reverse( 'accounts:user_page', args= [ self.username ] )

    def get_post_count(self):
        return self.post_set.all().count()



class PrivateMessage( models.Model ):

    receiver = models.ForeignKey( settings.AUTH_USER_MODEL )
    sender = models.ForeignKey( settings.AUTH_USER_MODEL, related_name= 'sender' )
    title = models.TextField( max_length= 100 )
    content = models.TextField( max_length= 500 )
    date_created = models.DateTimeField( help_text= 'Date Created', default= timezone.now )

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse( 'accounts:message_open', args= [ self.id ] )