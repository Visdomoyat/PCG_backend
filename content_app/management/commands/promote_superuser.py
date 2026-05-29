from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

User = get_user_model()


class Command(BaseCommand):
    help = "Grant superuser + staff to an existing username (e.g. after sign-up on Render)."

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Existing account username")

    def handle(self, *args, **options):
        username = options["username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as exc:
            raise CommandError(f'No user with username "{username}".') from exc

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(update_fields=["is_staff", "is_superuser", "is_active"])
        self.stdout.write(self.style.SUCCESS(f'"{username}" is now a superuser.'))
