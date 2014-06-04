from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from forum.models import Category, SubForum, Thread, Post
from forum.forms import PostForm


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

    last_posts = user.post_set.order_by( '-date_created' )[ :5 ]

    context = {
        'username': username,
        'last_posts': last_posts
    }

    return render( request, 'accounts/user_page.html', context )



def new_account( request ):

    pass