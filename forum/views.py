from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone

from forum.models import Category, SubForum, Thread, Post, PrivateMessage
from forum.forms import PostForm, MyUserCreationForm, PrivateMessageForm, ThreadForm, CategoryForm, SubForumForm
import forum.utilities as utilities

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


def sub_forum( request, forumSlug ):

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

    context = {
        'threads': ordered,
        'forumSlug': forumSlug,
        'paths': [ forum ]
    }

    return render( request, 'sub_forum.html', context )


def open_thread( request, threadSlug ):

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

            return HttpResponseRedirect( newPost.get_url() )

    else:
        form = PostForm()

    context = {
        'thread': theThread,
        'threadSlug': threadSlug,
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


@login_required( login_url= 'login' )
def new_category( request ):

    if not request.user.is_moderator:
        return HttpResponseForbidden( "Not a moderator." )


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


@login_required( login_url= 'login' )
def new_sub_forum( request, categorySlug ):

    if not request.user.is_moderator:
        return HttpResponseForbidden( "Not a moderator." )

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


@login_required( login_url= 'login' )
def edit_category( request, categorySlug ):

    try:
        category = Category.objects.get( slug= categorySlug )

    except Category.DoesNotExist:
        raise Http404( "Category doesn't exist." )

    if not request.user.is_moderator:
        return HttpResponseForbidden( "Not a moderator." )

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


@login_required( login_url= 'login' )
def edit_sub_forum( request, forumSlug ):

    try:
        forum = SubForum.objects.get( slug= forumSlug )

    except SubForum.DoesNotExist:
        raise Http404( "Sub-forum doesn't exist." )

    if not request.user.is_moderator:
        return HttpResponseForbidden( "Not a moderator." )

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


@login_required( login_url= 'login' )
def remove_post_confirm( request, postId ):

    try:
        post = Post.objects.get( id= postId )

    except Post.DoesNotExist:
        raise Http404( "Post doesn't exist." )

    if not request.user.is_moderator:
        return HttpResponseForbidden( 'Not a moderator.' )

    context = {
        'post': post
    }

    return render( request, 'remove/remove_post.html', context )


@login_required( login_url= 'login' )
def remove_post( request, postId ):

    try:
        post = Post.objects.get( id= postId )

    except Post.DoesNotExist:
        raise Http404( "Post doesn't exist." )

    if not request.user.is_moderator:
        return HttpResponseForbidden( 'Not a moderator.' )

    theThread = post.thread
    post.delete()

    return HttpResponseRedirect( theThread.get_url() )




@login_required( login_url= 'login' )
def remove_thread_confirm( request, threadSlug ):

    try:
        thread = Thread.objects.get( slug= threadSlug )

    except Thread.DoesNotExist:
        raise Http404( "Thread doesn't exist." )

    if not request.user.is_moderator:
        return HttpResponseForbidden( 'Not a moderator.' )

    context = {
        'thread': thread
    }

    return render( request, 'remove/remove_thread.html', context )


@login_required( login_url= 'login' )
def remove_thread( request, threadSlug ):

    try:
        thread = Thread.objects.get( slug= threadSlug )

    except Thread.DoesNotExist:
        raise Http404( "Thread doesn't exist." )

    if not request.user.is_moderator:
        return HttpResponseForbidden( 'Not a moderator.' )

    posts = Post.objects.filter( thread= thread )

    for post in posts:
        post.delete()

    forum = thread.sub_forum
    thread.delete()

    return HttpResponseRedirect( forum.get_url() )