# myapp/templatetags/nav_extras.py
from django import template

register = template.Library()

@register.filter
def startswith(text, value):
    """
    Returns True if 'text' starts with 'value'.
    Usage: {% if request.path|startswith:'inbox' %}
    """
    if isinstance(text, str) and isinstance(value, str):
        return text.lstrip('/').startswith(value.strip('/'))
    return False
