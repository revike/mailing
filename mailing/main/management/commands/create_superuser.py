from django.core.management import BaseCommand


class Command(BaseCommand):
    """Команда для создания супер юзера"""

    def handle(self, *args, **options):
        if not User.objects.filter(is_staff=True, is_superuser=True):
            User.objects.create_superuser(
                username='admin', email='admin_email@local.ru',
                password='admin',last_name='admin', first_name='admin'
            )
