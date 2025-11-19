from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    # Змінюємо текст-підказку, щоб він відповідав 5 хвилинам
    help = 'Deletes unverified (is_active=False) users older than 5 minutes.'

    def handle(self, *args, **options):
        # Встановлюємо час "до якого" видаляти
        expiration_time = timezone.now() - timedelta(minutes=5)

        # Знаходимо всіх неактивних користувачів, які були зареєстровані
        # раніше, ніж 5 хвилин тому
        users_to_delete = User.objects.filter(
            is_active=False,
            date_joined__lt=expiration_time 
        )
        # Отримуємо кількість для звіту та видаляємо
        count, _ = users_to_delete.delete()

        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted unverified users.')
        )