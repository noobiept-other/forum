from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from forum.models import Category, SubForum, Thread, Post, PrivateMessage
from forum.forms import PostForm, MyUserCreationForm, PrivateMessageForm


def index( request ):

    context = {
        'categories': Category.objects.all()
    }

    return render( request, 'index.html', context )


def sub_forum( request, forumSlug ):

    try:
        forum = SubForum.objects.get( slug= forumSlug )

    except SubForum.DoesNotExist:
        raise Http404( "Sub-form doesn't exist" )

    threads = forum.thread_set.all()

    def sortThreads( aThread ):
        last = aThread.get_last_post()

        if last:
            return last.date_created

        else:
            return aThread.date_created

    ordered = sorted( threads, key= sortThreads, reverse= True )

    context = {
        'threads': ordered
    }

    return render( request, 'sub_forum.html', context )


def thread( request, forumSlug, threadSlug ):

    try:
        theThread = Thread.objects.get( slug= threadSlug )

    except Thread.DoesNotExist:
        raise Http404( "Thread doesn't exist." )

    if request.method == 'POST':
        form = PostForm( request.POST )

        if form.is_valid():
            text = form.cleaned_data[ 'text' ]

            newPost = Post( sub_forum= theThread.sub_forum, thread= theThread, user= request.user, text= text )
            newPost.save()

            return HttpResponseRedirect( reverse( 'thread', args=[ forumSlug, threadSlug ] ) )

    else:
        form = PostForm()

    context = {
        'thread': theThread,
        'forumSlug': forumSlug,
        'threadSlug': threadSlug,
        'form': form
    }

    return render( request, 'thread.html', context )



def user_page( request, username ):

    try:
        user = User.objects.get( username= username )

    except User.DoesNotExist:
        raise Http404( "User doesn't exist." )

    posts = user.post_set.order_by( '-date_created' )
    last_posts = posts[ :5 ]
    total_posts = posts.count()

    context = {
        'username': username,
        'last_posts': last_posts,
        'total_posts': total_posts
    }

    return render( request, 'accounts/user_page.html', context )



def new_account( request ):

    if request.method == 'POST':

        form = MyUserCreationForm( request.POST )

        if form.is_valid():

            form.save()
            return HttpResponseRedirect( reverse( 'login' ) )

    else:
        form = MyUserCreationForm()

    return render( request, 'accounts/new.html', { 'form': form } )


@login_required( login_url= 'login' )
def send_private_message( request, username ):

    try:
        user = User.objects.get( username= username )

    except User.DoesNotExist:
        raise Http404( 'Invalid username.' )


    if request.method == 'POST':
        form = PrivateMessageForm( request.POST )

        if form.is_valid():

            title = form.cleaned_data[ 'title' ]
            content = form.cleaned_data[ 'content' ]
            message = PrivateMessage( receiver= user, sender= request.user, title= title, content= content )
            message.save()

            return HttpResponseRedirect( reverse( 'user_page',  args= [ request.user.username ] ) )

    else:
        form = PrivateMessageForm()

    context = {
        'form': form,
        'username': username
    }

    return render( request, 'accounts/send_message.html', context )


@login_required( login_url= 'login' )
def check_message( request ):

    messages = request.user.privatemessage_set.all()
    # messages = PrivateMessage.objects.filter( receiver= request.user )

    context = {
        'messages': messages
    }

    return render( request, 'accounts/check_messages.html', context )


@login_required( login_url= 'login' )
def open_message( request, messageId ):

    try:
        message = PrivateMessage.objects.get( id= messageId )

    except PrivateMessage.DoesNotExist:
        raise Http404( "Message doesn't exist" )


    context = {
        'message': message
    }

    return render( request, 'accounts/open_message.html', context )