from arcx.conf import settings
from arcx.utils.log import configure_logging


def setup(**usr_settings):
    settings.configure(**usr_settings)
    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
