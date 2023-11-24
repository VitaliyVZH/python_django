from django.contrib.auth.models import User
from django.core.management import BaseCommand

from myauth.models import Profile


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            Profile.objects.get_or_create(
                user=user,
            )
