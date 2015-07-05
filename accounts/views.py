from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login

from accounts.forms import MyUserCreationForm, PrivateMessageForm
from accounts.models import PrivateMessage
from accounts.decorators import must_be_staff
from forum import utilities


def new_account( request ):

    if request.method == 'POST':

        form = MyUserCreationForm( request.POST )

        if form.is_valid():

            form.save()
            utilities.set_message( request, 'User created!' )

            return HttpResponseRedirect( reverse( 'accounts:login' ) )

    else:
        form = MyUserCreationForm()

    context = {
        'form': form
    }

    return render( request, 'accounts/new_account.html', context )


def login( request ):

    context = {}
    utilities.get_message( request, context )

    return django_login( request, 'accounts/login.html', extra_context= context )


def user_page( request, username ):

    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    posts = user.post_set.order_by( '-date_created' )
    last_posts = posts[ :5 ]
    total_posts = posts.count()

    threads = user.thread_set.order_by( '-date_created' )
    last_threads = threads[ :5 ]
    total_threads = threads.count()

    context = {
        'pageUser': user,
        'last_posts': last_posts,
        'total_posts': total_posts,
        'last_threads': last_threads,
        'total_threads': total_threads,
    }

    utilities.get_message( request, context )

    return render( request, 'accounts/user_page.html', context )


@login_required
def message_send( request, username ):

    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( 'Invalid username.' )


    if request.method == 'POST':
        form = PrivateMessageForm( request.POST )

        if form.is_valid():

            title = form.cleaned_data[ 'title' ]
            content = form.cleaned_data[ 'content' ]
            message = PrivateMessage( receiver= user, sender= request.user, title= title, content= content )
            message.save()

            utilities.set_message( request, 'Private message sent!' )

            return HttpResponseRedirect( user.get_url() )

    else:
        form = PrivateMessageForm()

    context = {
        'form': form,
        'username': username
    }

    return render( request, 'accounts/send_message.html', context )


@login_required
def message_all( request ):

    messages = request.user.privatemessage_set.all()

    context = {
        'messages': messages
    }

    utilities.get_message( request, context )

    return render( request, 'accounts/check_messages.html', context )


@login_required
def message_open( request, messageId ):

    try:
        message = PrivateMessage.objects.get( id= messageId )

    except PrivateMessage.DoesNotExist:
        raise Http404( "Message doesn't exist" )

    context = {
        'private_message': message
    }

    return render( request, 'accounts/open_message.html', context )


@login_required
def message_remove_confirm( request, messageId ):

    try:
        message = request.user.privatemessage_set.get( id= messageId )

    except PrivateMessage.DoesNotExist:
        raise Http404( "Didn't find the message." )

    else:
        context = {
            'private_message': message
        }

        return render( request, 'accounts/remove_message.html', context )


@login_required
def message_remove( request, messageId ):

    try:
        message = request.user.privatemessage_set.get( id= messageId )

    except PrivateMessage.DoesNotExist:
        raise Http404( "Message doesn't exist." )

    message.delete()
    utilities.set_message( request, 'Message removed!' )

    return HttpResponseRedirect( reverse( 'accounts:message_all' ) )


@must_be_staff
def set_moderator( request, username ):

    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    user.is_moderator = not user.is_moderator
    user.save()

    utilities.set_message( request, 'Set/clear the moderator rights!' )

    return HttpResponseRedirect( user.get_url() )


def password_changed( request ):

    utilities.set_message( request, 'Password changed!' )

    return HttpResponseRedirect( reverse( 'home' ) )