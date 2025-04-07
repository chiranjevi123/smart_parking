from django import template

register = template.Library()

@register.filter(name='user_role')
def user_role(user):
    if user.is_superuser or user.is_staff:
        return "admin"
    return "user"
