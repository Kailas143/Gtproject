from django.apps import AppConfig


class ProductionMasterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'production_master'
