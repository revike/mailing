from django.core.management import BaseCommand

from authenticated.models import User


class Command(BaseCommand):
    """Команда для создания супер юзера"""

    def handle(self, *args, **options):
        if not User.objects.filter(is_staff=True, is_superuser=True):
            User.objects.create_superuser(
                username='admin', email='admin@local.ru', password='admin'
            )
