from rest_framework.permissions import BasePermission, DjangoModelPermissions, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            (request.user and request.user.is_staff)
        )


class FullDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class ViewCustomerHistoryPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')
