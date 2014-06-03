from django.shortcuts import render
from django.http import Http404

from forum.models import Category, SubForum, Thread

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

    context = {
        'thread': theThread
    }

    return render( request, 'thread.html', context )