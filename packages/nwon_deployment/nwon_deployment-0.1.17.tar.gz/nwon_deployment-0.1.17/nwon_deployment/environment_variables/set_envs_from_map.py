from os import environ

from nwon_deployment.settings import get_deployment_package_settings


def set_envs_from_map():
    settings = get_deployment_package_settings()
    for key, value in settings.docker.env_variable_map().items():
        environ[key] = str(value)
