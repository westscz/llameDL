class ProgressLogger:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self.logger = None

    def push_logger(self, logger):
        self.logger = logger

    def info(self, msg, all=False):
        self.logger.set_description(msg)


progresslogger = ProgressLogger()
