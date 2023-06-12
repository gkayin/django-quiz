from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
#    return user.groups.filter(name=group_name).exists()
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False