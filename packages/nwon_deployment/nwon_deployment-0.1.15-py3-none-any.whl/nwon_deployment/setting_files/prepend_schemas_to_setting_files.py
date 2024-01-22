import os

from nwon_deployment.helper.prepend_lines_to_file import prepend_lines_to_file
from nwon_deployment.setting_files.lines_to_prepend import (
    lines_to_prepend_setting,
    lines_to_prepend_setting_override,
)
from nwon_deployment.settings import get_deployment_package_settings


def prepend_schemas_to_setting_files():
    settings = get_deployment_package_settings()

    setting_file_name = settings.application_settings.setting_file_name
    setting_override_file_name = (
        settings.application_settings.setting_override_file_name
    )

    setting_lines = lines_to_prepend_setting()
    setting_overwrite_lines = lines_to_prepend_setting_override()

    for _, _, files in os.walk(settings.paths.deployment_environment):
        for file in files:
            if setting_file_name in file:
                prepend_lines_to_file(file, setting_lines)

            if setting_override_file_name in file:
                prepend_lines_to_file(file, setting_overwrite_lines)
