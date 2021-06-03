import logging

from config import APP_SETTINGS, LOGGING_LEVEL

# filename='dmonitor.log',
logging.basicConfig(level=LOGGING_LEVEL[APP_SETTINGS.prop('application.log.level')],
                    format="%(asctime)s %(pathname)s:%(lineno)s %(funcName)s() %(levelname)s - %(message)s")
log = logging.getLogger(__name__)
