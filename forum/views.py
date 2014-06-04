from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

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


    context = {
        'threads': forum.thread_set.all()
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

            newPost = Post( thread= theThread, user= request.user, text= text )
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




def new_account( request ):

    pass