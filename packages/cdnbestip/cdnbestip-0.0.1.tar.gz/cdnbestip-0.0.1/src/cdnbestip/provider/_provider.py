from abc import ABC
from abc import abstractmethod


class Provider(ABC):
    def __init__(self, domain, skip=True, cdn_url='') -> None:
        self.domain = domain
        self.skip = skip
        self.cdn_url = cdn_url

    @abstractmethod
    def run(self):
        pass
