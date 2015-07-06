from django.apps import AppConfig
from django.conf import settings
from django.contrib.auth import get_user_model


class ForumConfig( AppConfig ):

    name = 'forum'

    def ready(self):

        self.create_retired_user()


    def create_retired_user(self):
        """
            When a user is deleted, all its posts/threads/etc will be pass to this user.
            Need to make sure the user exists.
        """
        username = settings.RETIRED_USERNAME
        password = settings.RETIRED_PASSWORD

        userModel = get_user_model()

        try:
            userModel.objects.get( username= username )

        except userModel.DoesNotExist:
            user_no_more = userModel( username= username )
            user_no_more.set_password( password )
            user_no_more.save()
            print( 'Retired user created: {}'.format( username ) )
