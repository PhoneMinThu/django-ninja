from django.core.management.base import BaseCommand
from apps.users.utils import USER_TYPE_LIST
from django.contrib.auth.models import Group
import logging
# from apps.users.models import UserType


class Command(BaseCommand):
    help = 'Add Initial Data'

    def handle(self, *args, **kwargs):
        group_instances = []
        for user_type in USER_TYPE_LIST:
            group_instances.append(Group(
                name=user_type,
            ))
        Group.objects.bulk_create(group_instances)
        logging.info(msg="create User Type")
