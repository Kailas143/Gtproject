from django.apps import AppConfig


class ProductionStoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'production_store'
