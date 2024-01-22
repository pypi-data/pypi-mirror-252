import logging
import dumbee


class Logger(dumbee.Middleware):
    @property
    def logger(self):
        return logging.getLogger("dumdb")

    def __call__(self, query, next):
        self.logger.info(f"{query.type} \t {query.path}")
        return next(query)
