from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Model User"""

    class Meta:
        verbose_name_plural = 'Users'
        verbose_name = 'Users'

    def __str__(self):
        return f'{self.username}'
