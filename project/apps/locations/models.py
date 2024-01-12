from django.db import models
from apps.users.models import User
# Create your models here.


class UserLocations(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='user_locations',
        on_delete=models.CASCADE,
    )
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
