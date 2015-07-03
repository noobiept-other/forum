from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

import math

from forum.models import Category, SubForum, Thread, Post
from forum.forms import PostForm, ThreadForm, CategoryForm, SubForumForm
import forum.utilities as utilities
from forum.decorators import must_be_moderator, must_be_staff

def index( request ):

    categories = []

    for category in Category.objects.all():

        stuff = {
            'name': category.name,
            'slug': category.slug,
            'subforum': []
        }

        for subForum in category.subforum_set.all():

            lastPost = subForum.get_last_post()

            stuff[ 'subforum' ].append({
                'name': subForum.name,
                'url': subForum.get_url(),
                'threads_count': len( subForum.thread_set.all() ),
                'last_post': lastPost
            })

        categories.append( stuff )

    context = {
        'categories': categories
    }

    return render( request, 'index.html', context )


def sub_forum( request, forumSlug, page= 0 ):

    try:
        forum = SubForum.objects.get( slug= forumSlug )

    except SubForum.DoesNotExist:
        raise Http404( "Sub-form doesn't exist" )

    threads = forum.thread_set.all()

    def sortThreads( aThread ):
        last = aThread.get_last_post()

        if last:
            return last.date_edited

        else:
            return aThread.date_edited

    ordered = sorted( threads, key= sortThreads, reverse= True )

    threadsPerPage = settings.THREADS_PER_PAGE
    page = int( page )
    startThread = page * threadsPerPage
    totalThreads = len( ordered )
    totalPages = int( math.ceil( float(totalThreads) / float(threadsPerPage) ) )

    if page != 0 and startThread >= totalThreads:
        raise Http404( "Invalid sub-forum page." )

    pageThreads = ordered[ startThread : startThread + threadsPerPage ]

    context = {
        'threads': pageThreads,
        'forumSlug': forumSlug,
        'page': page,
        'pages': range( 0, totalPages ),
        'paths': [ forum ]
    }

    return render( request, 'sub_forum.html', context )


def open_thread( request, threadSlug, page= 0 ):

    try:
        theThread = Thread.objects.get( slug= threadSlug )

    except Thread.DoesNotExist:
        raise Http404( "Thread doesn't exist." )

    if request.method == 'POST' and not theThread.is_locked:
        form = PostForm( request.POST )

        if form.is_valid():
            text = form.cleaned_data[ 'text' ]

            newPost = Post( sub_forum= theThread.sub_forum, thread= theThread, user= request.user, text= text )
            newPost.save()

            return HttpResponseRedirect( newPost.get_url() )

    else:
        form = PostForm()

    postPerPage = settings.POSTS_PER_PAGE
    page = int( page )
    startPost = page * postPerPage

    allPosts = theThread.post_set.all()
    totalPosts = allPosts.count()
    totalPages = int( math.ceil( float(totalPosts) / float(postPerPage) ) )

    if page != 0 and startPost >= totalPosts:
        raise Http404( "Invalid thread page." )

    pagePosts = allPosts[ startPost : startPost + postPerPage ]

    context = {
        'thread': theThread,
        'posts': pagePosts,
        'threadSlug': threadSlug,
        'page': page,
        'pages': range( 0, totalPages ),
        'form': form,
        'paths': [ theThread.sub_forum, theThread ]
    }

    return render( request, 'thread.html', context )


@login_required( login_url= 'login' )
def new_thread( request, forumSlug ):

    try:
        forum = SubForum.objects.get( slug= forumSlug )

    except SubForum.DoesNotExist:
        raise Http404( "Sub-forum doesn't exist." )


    if request.method == 'POST':
        form = ThreadForm( request.POST )

        if form.is_valid():

            title = form.cleaned_data[ 'title' ]
            content = form.cleaned_data[ 'content' ]

            theThread = Thread( sub_forum= forum, user= request.user, title= title, slug= '', text= content )
            utilities.unique_slugify( theThread, title )
            theThread.save()

            return HttpResponseRedirect( theThread.get_url() )

    else:
        form = ThreadForm()


    context = {
        'forumSlug': forumSlug,
        'form': form
    }

    return render( request, 'new/new_thread.html', context )


@must_be_moderator
def new_category( request ):

    if request.method == 'POST':
        form = CategoryForm( request.POST )

        if form.is_valid():

            categoryName = form.cleaned_data[ 'category' ]
            category = Category( name= categoryName, slug= '' )
            utilities.unique_slugify( category, categoryName )
            category.save()

            return HttpResponseRedirect( reverse( 'index' ) )

    else:
        form = CategoryForm()

    context = {
        'form': form
    }

    return render( request, 'new/new_category.html', context )


@must_be_moderator
def new_sub_forum( request, categorySlug ):

    try:
        category = Category.objects.get( slug= categorySlug )

    except Category.DoesNotExist:
        raise Http404( "Wrong category." )


    if request.method == 'POST':

        form = SubForumForm( request.POST )

        if form.is_valid():

            forumName = form.cleaned_data[ 'forumName' ]

            forum = SubForum( name= forumName, slug= '', category= category )
            utilities.unique_slugify( forum, forumName )
            forum.save()

            return HttpResponseRedirect( reverse( 'index' ) )

    else:
        form = SubForumForm()

    context = {
        'categorySlug': categorySlug,
        'form': form
    }

    return render( request, 'new/new_sub_forum.html', context )


@login_required( login_url= 'login' )
def edit_post( request, postId ):

    try:
        post = Post.objects.get( id= postId )

    except Post.DoesNotExist:
        raise Http404( "Post doesn't exist." )

    if request.user != post.user and not request.user.is_moderator:
        return HttpResponseForbidden( "Not your post (and not a moderator)." )


    if request.method == 'POST':

        form = PostForm( request.POST )

        if form.is_valid():
            text = form.cleaned_data[ 'text' ]

            post.text = text
            post.was_edited = True
            post.date_edited = timezone.localtime( timezone.now() )
            post.edited_by = request.user
            post.save()

            return HttpResponseRedirect( post.get_url() )

    else:
        form = PostForm( initial= { 'text': post.text } )

    context = {
        'form': form,
        'post': post
    }

    return render( request, 'edit/edit_post.html', context )


@login_required( login_url= 'login' )
def edit_thread( request, threadSlug ):

    try:
        theThread = Thread.objects.get( slug= threadSlug )

    except Thread.DoesNotExist:
        raise Http404( "Thread doesn't exist." )

    if request.user != theThread.user and not request.user.is_moderator:
        return HttpResponseForbidden( "Not your thread (and not a moderator)." )


    if request.method == 'POST':
        form = ThreadForm( request.POST )

        if form.is_valid():
            title = form.cleaned_data[ 'title' ]
            content = form.cleaned_data[ 'content' ]

            theThread.title = title
            theThread.text = content
            theThread.was_edited = True
            theThread.date_edited = timezone.localtime( timezone.now() )
            theThread.edited_by = request.user
            utilities.unique_slugify( theThread, title )
            theThread.save()

            return HttpResponseRedirect( theThread.get_url() )

    else:
        form = ThreadForm( initial= { 'title': theThread.title, 'content': theThread.text } )

    context = {
        'form': form,
        'thread': theThread
    }

    return render( request, 'edit/edit_thread.html', context )


@must_be_moderator
def edit_category( request, categorySlug ):

    try:
        category = Category.objects.get( slug= categorySlug )

    except Category.DoesNotExist:
        raise Http404( "Category doesn't exist." )

    if request.method == 'POST':
        form = CategoryForm( request.POST )

        if form.is_valid():
            categoryName = form.cleaned_data[ 'category' ]

            category.name = categoryName
            utilities.unique_slugify( category, categoryName )
            category.save()

            return HttpResponseRedirect( reverse( 'index' ) )

    else:
        form = CategoryForm( initial= { 'category': category.name } )

    context = {
        'form': form,
        'category': category
    }

    return render( request, 'edit/edit_category.html', context )


@must_be_moderator
def edit_sub_forum( request, forumSlug ):

    try:
        forum = SubForum.objects.get( slug= forumSlug )

    except SubForum.DoesNotExist:
        raise Http404( "Sub-forum doesn't exist." )

    if request.method == 'POST':
        form = SubForumForm( request.POST )

        if form.is_valid():
            forumName = form.cleaned_data[ 'forumName' ]

            forum.name = forumName
            utilities.unique_slugify( forum, forumName )
            forum.save()

            return HttpResponseRedirect( forum.get_url() )

    else:
        form = SubForumForm( initial= { 'forumName': forum.name } )

    context = {
        'form': form,
        'sub_forum': forum
    }

    return render( request, 'edit/edit_sub_forum.html', context )


@must_be_moderator
def remove_post_confirm( request, postId ):

    try:
        post = Post.objects.get( id= postId )

    except Post.DoesNotExist:
        raise Http404( "Post doesn't exist." )

    context = {
        'post': post
    }

    return render( request, 'remove/remove_post.html', context )


@must_be_moderator
def remove_post( request, postId ):

    try:
        post = Post.objects.get( id= postId )

    except Post.DoesNotExist:
        raise Http404( "Post doesn't exist." )

    theThread = post.thread
    post.delete()

    return HttpResponseRedirect( theThread.get_url() )




@must_be_moderator
def remove_thread_confirm( request, threadSlug ):

    try:
        thread = Thread.objects.get( slug= threadSlug )

    except Thread.DoesNotExist:
        raise Http404( "Thread doesn't exist." )

    context = {
        'thread': thread
    }

    return render( request, 'remove/remove_thread.html', context )


@must_be_moderator
def remove_thread( request, threadSlug ):

    try:
        thread = Thread.objects.get( slug= threadSlug )

    except Thread.DoesNotExist:
        raise Http404( "Thread doesn't exist." )

    for post in thread.post_set.all():
        post.delete()

    forum = thread.sub_forum
    thread.delete()

    return HttpResponseRedirect( forum.get_url() )

@must_be_moderator
def remove_sub_forum_confirm( request, forumSlug ):

    try:
        forum = SubForum.objects.get( slug= forumSlug )

    except SubForum.DoesNotExist:
        raise Http404( "Sub-forum doesn't exist." )

    context = {
        'forum': forum
    }

    return render( request, 'remove/remove_sub_forum.html', context )

@must_be_moderator
def remove_sub_forum( request, forumSlug ):

    try:
        forum = SubForum.objects.get( slug= forumSlug )

    except SubForum.DoesNotExist:
        raise Http404( "Sub-forum doesn't exist." )

    for thread in forum.thread_set.all():
        for post in thread.post_set.all():
            post.delete()

        thread.delete()

    forum.delete()

    return HttpResponseRedirect( reverse( 'index' ) )


@must_be_moderator
def remove_category_confirm( request, categorySlug ):

    try:
        category = Category.objects.get( slug= categorySlug )

    except Category.DoesNotExist:
        raise Http404( "Category doesn't exist." )

    context = {
        'category': category
    }

    return render( request, 'remove/remove_category.html', context )


@must_be_moderator
def remove_category( request, categorySlug ):

    try:
        category = Category.objects.get( slug= categorySlug )

    except Category.DoesNotExist:
        raise Http404( "Category doesn't exist." )

    for forum in category.subforum_set.all():
        for thread in forum.thread_set.all():
            for post in thread.post_set.all():
                post.delete()

            thread.delete()

        forum.delete()

    category.delete()

    return HttpResponseRedirect( reverse( 'index' ) )


@must_be_moderator
def remove_user_confirm( request, username ):

    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    context = {
        'user_to_remove': user
    }

    return render( request, 'remove/remove_user.html', context )


@must_be_moderator
def remove_user( request, username ):

    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    retiredUser = userModel.objects.get( username= settings.RETIRED_USERNAME )

    for thread in user.thread_set.all():

        thread.user = retiredUser
        thread.save()

    for post in user.post_set.all():

        post.user = retiredUser
        post.save()

        # don't really need to save the private messages, so that will be removed

    user.delete()

    return HttpResponseRedirect( reverse( 'index' ) )


@must_be_moderator
def lock_thread( request, threadSlug ):
    """
        Locks/unlocks the thread
    """

    try:
        thread = Thread.objects.get( slug= threadSlug )

    except Thread.DoesNotExist:
        raise Http404( "Thread doesn't exist." )


    thread.is_locked = not thread.is_locked
    thread.save()

    return HttpResponseRedirect( thread.get_url() )


@must_be_staff
def set_moderator( request, username ):

    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    user.is_moderator = not user.is_moderator
    user.save()

    return HttpResponseRedirect( user.get_url() )