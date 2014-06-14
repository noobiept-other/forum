import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forum.settings")

from django.conf import settings
from forum.models import Profile

def startup():
    create_retired_user()

def create_retired_user():
    """
        When a user is deleted, all its posts/threads/etc will be pass to this user.
        Need to make sure the user exists.
    """
    username = settings.RETIRED_USERNAME
    password = settings.RETIRED_PASSWORD

    # userModel = get_user_model()

    try:
        Profile.objects.get( username= username )

    except Profile.DoesNotExist:
        user_no_more = Profile( username= username )
        user_no_more.set_password( password )
        user_no_more.save()
        print 'Retired user created: {}'.format( username )

    else:
        print 'Retired user already created: {}'.format( username )

startup()