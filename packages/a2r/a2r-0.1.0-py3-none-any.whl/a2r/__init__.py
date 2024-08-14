from a2r.conf import settings
from a2r.utils.log import configure_logging


def setup(**usr_settings):
    settings.configure(**usr_settings)
    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
