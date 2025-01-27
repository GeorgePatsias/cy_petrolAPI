import logging


class Logger():
    def __init__(self):
        self.logger = logging.getLogger("main")
        self.logger.setLevel(logging.DEBUG)

        self._handler = logging.FileHandler('/var/log/uwsgi/server.log')
        self._handler.setLevel(logging.DEBUG)

        self._formatter = logging.Formatter('[%(name)s] - %(levelname)s - %(asctime)s  - %(message)s')
        self._handler.setFormatter(self._formatter)
        self.logger.addHandler(self._handler)

    def getLogger(self):
        return self.logger
