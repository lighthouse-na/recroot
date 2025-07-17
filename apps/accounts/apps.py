from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"

    def ready(self):
        """
        Perform any app-specific initialisation when the app is ready.

        This method imports the signals module to ensure that any signal handlers
        associated with the 'accounts' app are correctly registered when the app is loaded.
        """
