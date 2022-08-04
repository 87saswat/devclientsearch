from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    # registering signals from signals.py
    def ready(self):
        import users.signals
