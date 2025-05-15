from abc import ABC, abstractmethod


class FileRepository(ABC):

    @abstractmethod
    def upload(self, file):
        raise NotImplementedError

    @abstractmethod
    def download(self, file):
        raise NotImplementedError

    @abstractmethod
    def delete(self, file):
        raise NotImplementedError
