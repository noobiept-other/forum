from django import template
from forum import settings


register = template.Library()


@register.filter
def add_emotes( text ):

    for emote in settings.EMOTES:

        text = text.replace( emote, '<img src="{}" alt="{}" title="{}" />'.format( settings.EMOTES[ emote ], emote, emote ) )

    return text
