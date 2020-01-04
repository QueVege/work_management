from rest_framework import permissions
from django.contrib.auth.models import Group


class IsManager(permissions.BasePermission):
    """
    Check user is in 'Managers' group
    """
    message = 'This action is allowed only for managers'

    def has_permission(self, request, view):
        group_name = 'Managers'

        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            return Group.objects.get(name=group_name).user_set.filter(id=request.user.id).exists()
        except Group.DoesNotExist:
            return False
