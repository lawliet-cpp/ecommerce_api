from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class Backend(BaseBackend):
    def authenticate(self, request, email=None,password=None):
        user_model = get_user_model()
        try:
            user=user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        return get_user_model().objects.get(id=user_id)
