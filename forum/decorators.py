from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def must_be_moderator( function ):

    @login_required( login_url= 'login' )
    def func_wrapper( request, *args, **kwargs ):
        if not request.user.is_moderator:
            return HttpResponseForbidden( 'Not a moderator.' )

        return function( request, *args, **kwargs )

    return func_wrapper
