from django import template
from django.template.defaultfilters import safe


register = template.Library()


@register.filter
def account_type( user ):

    if not user.is_active:
        accountType = 'disabled'

    elif user.is_staff:
        accountType = 'staff'

    elif user.is_moderator:
        accountType = 'moderator'

    else:
        accountType = 'normal'

    return safe( '<span class="Accounts-{}" title="{}">{}</span>'.format( accountType, accountType, user.username ) )
