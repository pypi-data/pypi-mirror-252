from django.contrib.contenttypes.models import ContentType
from rbac_service.models import UserRole
from urllib.parse import urlparse
from django.db.models import Q


class BasePermission:
    ACTION_MAP = {
        "list": "read_list",
        "retrieve": "read",
        "create": "add",
        "update": "change",
        "partial_update": "partial_change",
        "destroy": "delete",
    }

    METHOD_MAP = {
        "GET": "read",
        "POST": "add",
        "PUT": "change",
        "PATCH": "partial_change",
        "DELETE": "delete",
    }

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True

    def get_required_action(self, request, view):
        return self.ACTION_MAP.get(
            getattr(view, "action", None), self.METHOD_MAP.get(request.method)
        )

    def check_permission_records(self, request, view, required_action, user_role):
        url_filter = {"url_path": urlparse(request.build_absolute_uri()).path}
        role_query = user_role.permissions.filter(**url_filter)
        if role_query.exists():
            if role_query.filter(**{required_action: True}).exists():
                return True
            else:
                return False
        try:
            model_instance = ContentType.objects.get_for_model(
                view.permission_queryset.model
            )
            return user_role.permissions.filter(
                **{required_action: True, "model": model_instance}
            ).exists()
        except AttributeError:
            return False

class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            user_role = UserRole.objects.get(user=request.user).role
        except Exception:
            return False
        required_action = self.get_required_action(request, view)

        if not required_action:
            return False

        return self.check_permission_records(request, view, required_action, user_role)

