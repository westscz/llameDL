class ProgressLogger:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self.logger = None

    def push_logger(self, logger):
        self.logger = logger

    def info(self, msg, all=False):
        self.logger.set_description(msg)

    def change_size(self, size):
        self.logger.total = size

    def __iadd__(self, other):
        self.logger.update(n=other)


progresslogger = ProgressLogger()
