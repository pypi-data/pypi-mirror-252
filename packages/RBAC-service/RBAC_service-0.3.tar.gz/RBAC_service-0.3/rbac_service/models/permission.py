from django.db import models
from django.contrib.contenttypes.models import ContentType


class Permission(models.Model):
    name = models.CharField(max_length=100)
    model = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="rbac_permissions",
    )
    url_path = models.CharField(max_length=250, blank=True, null=True)
    read_list = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    add = models.BooleanField(default=False)
    change = models.BooleanField(default=False)
    partial_change = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

    def __str__(self):
        if self.model:
            return f"{self.name} - {self.model.name}"
        else:
            return f"{self.name} - {self.url_path}"
