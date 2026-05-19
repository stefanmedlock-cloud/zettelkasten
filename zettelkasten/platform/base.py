from abc import ABC, abstractmethod

class BaseFileLock(ABC):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.lock_file = filepath + ".lock"
        self._fd = None

    @abstractmethod
    def acquire(self) -> None:
        pass

    @abstractmethod
    def release(self) -> None:
        pass
