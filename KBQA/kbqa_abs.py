from abc import abstractmethod


class KBQAAbs:
    @abstractmethod
    def parse_config(self):
        pass

    @abstractmethod
    def init_obj(self):
        pass
