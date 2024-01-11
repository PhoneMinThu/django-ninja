from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class CustomPermissionManager(models.Manager):

    def get_by_natural_key(self, codename, app_label, model):
        return self.get(
            codename=codename,
            content_type=ContentType.objects.db_manager(self.db).get_by_natural_key(
                app_label, model
            ),
        )


class CustomPermission(models.Model):
    CREATE = 'create'
    UPDATE = 'update'
    PATCH = 'patch'
    DELETE = 'delete'
    RETRIEVE = 'retrieve'
    LIST = 'list'
    READ_ONLY = 'read_only'
    NO_DELETE = 'no_delete'
    ALL = 'all'
    ACTIONS = [
        (CREATE, CREATE),
        (UPDATE, UPDATE),
        (PATCH, PATCH),
        (DELETE, DELETE),
        (RETRIEVE, RETRIEVE),
        (LIST, LIST),
        (READ_ONLY, READ_ONLY),
        (NO_DELETE, NO_DELETE),
        (ALL, ALL),
    ]
    content_type = models.ForeignKey(
        ContentType,
        related_name="content_type_permissions",
        on_delete=models.CASCADE,
    )
    actions = ArrayField(models.CharField(max_length=15, choices=ACTIONS), size=9)

    objects = CustomPermissionManager()


class UserType(models.Model):
    USER = 'user'
    ADMIN = 'admin'
    SUPER_ADMIN = 'super_admin'
    TYPE_CHOICES = [
        (USER, USER),
        (ADMIN, ADMIN),
        (SUPER_ADMIN, SUPER_ADMIN),
    ]
    user_type = models.CharField(choices=TYPE_CHOICES, max_length=11)

    type_permissions = models.ManyToManyField(
        CustomPermission,
        related_name="user_types",
        blank=True,
    )


class UserModel(AbstractBaseUser):
    phone_number = models.CharField(max_length=11, unique=True)
    user_types = models.ManyToManyField(
        UserType,
        related_name="users",
    )
    user_permissions = models.ManyToManyField(
        CustomPermission,
        blank=True,
        related_name="users",
    )

    USERNAME_FIELD = "phone_number"
