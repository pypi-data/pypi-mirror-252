from django.template import Library
from django.conf import settings

register = Library()

@register.inclusion_tag("mazerango/side_menu.html", takes_context=True)
def mazerango_side_menu(context):
    return {
        "menus" : settings.SIDEMENU_SETTING
    }

@register.filter
def test(value):
    return value
