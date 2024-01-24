from django.db import models
from rbac_service.models import Role
from django.conf import settings


class UserRole(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user} - {self.role}"
