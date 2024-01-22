from django.template import Library
from mazerango.sidemenu import SIDEMENU_SETTING

register = Library()

@register.inclusion_tag("mazerango/side_menu.html", takes_context=True)
def mazerango_side_menu(context):
    return {
        "menus" : SIDEMENU_SETTING
    }

@register.filter
def test(value):
    return value
