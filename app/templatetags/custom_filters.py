from django import template
from django.contrib.auth import get_user_model

User = get_user_model()
register = template.Library()

@register.filter
def can_delete(request_user, target_user):
    if request_user.role == User.Role.PRINCIPAL:
        return target_user.role in [User.Role.TEACHER, User.Role.STUDENT]
    elif request_user.role == User.Role.TEACHER:
        return target_user.role == User.Role.STUDENT
    return False
