from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'apps.profiles'
    verbose_name = "VHMS Profile"


class UtilsConfig(AppConfig):
    name = 'apps.utils'
    verbose_name = "VHMS Utils"


class CoreConfig(AppConfig):
    name = 'apps.core'
    verbose_name = "VHMS Core"