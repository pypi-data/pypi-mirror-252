from django.contrib import admin
from rbac_service.models import Permission, Role, UserRole


class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_model_name",
        "url_path",
        "read_list",
        "read",
        "add",
        "change",
        "partial_change",
        "delete",
    )
    search_fields = ["name", "url_path", "model__model"]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super(PermissionAdmin, self).formfield_for_dbfield(
            db_field, request, **kwargs
        )
        if db_field.name == "url_path":
            field.help_text = (
                'Please enter the path starting and ending with a slash ("/"). For example, "/example-path/". Do not include the full URL, just the path.',
            )
        return field

    def get_model_name(self, obj):
        if obj.model:
            return obj.model.model
        return None

    get_model_name.short_description = "Model Name"


admin.site.register(Permission, PermissionAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "display_permissions"]
    filter_horizontal = ("permissions",)

    def display_permissions(self, obj):
        return ", ".join([permission.name for permission in obj.permissions.all()])

    display_permissions.short_description = "Permissions"


admin.site.register(Role, RoleAdmin)


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ["user", "role"]


admin.site.register(UserRole, UserRoleAdmin)
