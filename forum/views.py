from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify

from forum.models import Category, SubForum, Thread, Post, PrivateMessage
from forum.forms import PostForm, MyUserCreationForm, PrivateMessageForm, NewThreadForm, CategoryForm, NewSubForumForm


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
            return last.date_created

        else:
            return aThread.date_created

    ordered = sorted( threads, key= sortThreads, reverse= True )

    context = {
        'threads': ordered,
        'forumSlug': forumSlug,
        'paths': [ forum ]
    }

    return render( request, 'sub_forum.html', context )


def thread( request, threadSlug ):

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
        form = NewThreadForm( request.POST )

        if form.is_valid():

            title = form.cleaned_data[ 'title' ]
            content = form.cleaned_data[ 'content' ]

            #HERE the slug has to be unique...
            slug = slugify( title )

            theThread = Thread( sub_forum= forum, user= request.user, title= title, slug= slug, text= content )
            theThread.save()

            return HttpResponseRedirect( reverse( 'thread', args= [ slug ] ) )

    else:
        form = NewThreadForm()


    context = {
        'forumSlug': forumSlug,
        'form': form
    }

    return render( request, 'new_thread.html', context )


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
        'username': username,
        'last_posts': last_posts,
        'total_posts': total_posts,
        'last_threads': last_threads,
        'total_threads': total_threads
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
            categorySlug = slugify( categoryName )
            category = Category( name= categoryName, slug= categorySlug )
            category.save()

            return HttpResponseRedirect( reverse( 'index' ) )

    else:
        form = CategoryForm()

    context = {
        'form': form
    }

    return render( request, 'new_category.html', context )


@login_required( login_url= 'login' )
def new_sub_forum( request, categorySlug ):

    if not request.user.is_moderator:
        return HttpResponseForbidden( "Not a moderator." )

    try:
        category = Category.objects.get( slug= categorySlug )

    except Category.DoesNotExist:
        raise Http404( "Wrong category." )


    if request.method == 'POST':

        form = NewSubForumForm( request.POST )

        if form.is_valid():

            forumName = form.cleaned_data[ 'forumName' ]
            forumSlug = slugify( forumName )

            forum = SubForum( name= forumName, slug= forumSlug, category= category )
            forum.save()

            return HttpResponseRedirect( reverse( 'index' ) )

    else:
        form = NewSubForumForm()

    context = {
        'categorySlug': categorySlug,
        'form': form
    }

    return render( request, 'new_sub_forum.html', context )