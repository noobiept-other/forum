from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url( r'^new_account$', 'accounts.views.new_account', name= 'new_account' ),
    url( r'^login$', 'accounts.views.login', name= 'login' ),
    url( r'^logout$', 'django.contrib.auth.views.logout', name= 'logout' ),
    url( r'^change_password$', 'django.contrib.auth.views.password_change', { 'template_name': 'accounts/change_password.html', 'post_change_redirect': 'accounts:password_changed' }, name= 'change_password' ),
    url( r'^password_changed$', 'accounts.views.password_changed', name= 'password_changed' ),
    url( r'^user/(?P<username>\w+)$', 'accounts.views.user_page', name= 'user_page' ),
    url( r'^send_message/(?P<username>\w+)$', 'accounts.views.send_private_message', name= 'send_message' ),
    url( r'^check_message/$', 'accounts.views.check_message', name='check_message' ),
    url( r'^check_message/(?P<messageId>\w+)$', 'accounts.views.open_message', name= 'open_message' ),
    url( r'^remove_message/(?P<messageId>\w+)$', 'accounts.views.remove_message', name= 'remove_message' ),
    url( r'^set_moderator/(?P<username>\w+)$', 'accounts.views.set_moderator', name= 'set_moderator' ),
)
