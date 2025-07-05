from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    def ready(self):
        import accounts.signals


class SignalementsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'signalements'

    def ready(self):
        import signalements.signals
