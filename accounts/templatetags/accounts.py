from django import template
from django.template.defaultfilters import safe


register = template.Library()


@register.filter
def account_name( user ):

    if not user.is_active:
        accountType = 'disabled'

    elif user.is_staff:
        accountType = 'staff'

    elif user.is_moderator:
        accountType = 'moderator'

    else:
        accountType = 'normal'

    return safe( '<a href="{}" class="Accounts-{}" title="{}">{}</a>'.format( user.get_url(), accountType, accountType, user.username ) )
