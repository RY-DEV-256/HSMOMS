from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class HardCodedAdminBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            user, created = User.objects.get_or_create(username=username, defaults={
                'is_staff': True,
                'is_superuser': True
            })
            if created:
                user.set_password(password)
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
