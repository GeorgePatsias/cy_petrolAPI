from config import API_KEY
from classes.Logger import Logger
logger = Logger().getLogger()


class Auth():
    def isValid(self, api_key=None):
        try:
            if not api_key or api_key != API_KEY:
                logger.error('Unauthorized API Key')
                return False

            return True

        except Exception as e:
            logger.exception(e)
            return False
