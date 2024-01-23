from .prototype import Prototyped


class Context(metaclass=Prototyped):
    def __init__(self, config: dict = None):
        if config is None:
            config = {}
        self.config = config
