from forum.models import Profile
from django.conf import settings

def startup():
    create_retired_user()

def create_retired_user():
    """
        When a user is deleted, all its posts/threads/etc will be pass to this user.
        Need to make sure the user exists.
    """
    username = settings.RETIRED_USERNAME
    password = settings.RETIRED_PASSWORD

    try:
        Profile.objects.get( username= username )

    except Profile.DoesNotExist:
        user_no_more = Profile( username= username )
        user_no_more.set_password( password )
        user_no_more.save()


startup()