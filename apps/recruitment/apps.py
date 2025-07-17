from django.apps import AppConfig


class RecruitmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.recruitment"
    label = "recruitment"

    def ready(self):
<<<<<<< HEAD
        pass
=======
        import apps.recruitment.signals
>>>>>>> upstream/main
