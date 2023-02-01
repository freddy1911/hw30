from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsCreateBySelectionOwner(BasePermission):
    message = 'Вы не имеете прав изменять подборку'

    def has_object_permission(self, request, view, selection):
        if request.user == selection.owner:
            return True
        return False


class IsCreatedByAuthorOrStaff(BasePermission):
    message = 'Только пользователь, создавший объявление, amdin и модераторы может изменять или удалять его.'

    def has_object_permission(self, request, view, ad):
        if request.user == ad.author or request.user.role != UserRoles.MEMBER or request.user.role != UserRoles.ADMIN:
            return True
        return False
