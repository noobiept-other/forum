from django.contrib import admin

from accounts.models import Account, PrivateMessage


class PrivateMessageAdmin( admin.ModelAdmin ):

    list_display = ( 'receiver', 'sender', 'title', 'content' )

admin.site.register( PrivateMessage, PrivateMessageAdmin )


class AccountAdmin( admin.ModelAdmin ):

    list_display = ( 'username', 'email', 'is_moderator', 'is_staff', 'date_joined' )

admin.site.register( Account, AccountAdmin )
