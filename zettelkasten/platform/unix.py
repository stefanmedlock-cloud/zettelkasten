import os
import fcntl
from .base import BaseFileLock
from ..exceptions import LockTimeoutError

class UnixFileLock(BaseFileLock):
    def acquire(self) -> None:
        self._fd = os.open(self.lock_file, os.O_CREAT | os.O_WRONLY)
        try:
            fcntl.flock(self._fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, BlockingIOError):
            os.close(self._fd)
            self._fd = None
            raise LockTimeoutError(f"Konnte Dateisperre für {self.filepath} nicht erlangen.")

    def release(self) -> None:
        if self._fd is not None:
            try:
                fcntl.flock(self._fd, fcntl.LOCK_UN)
            finally:
                os.close(self._fd)
                self._fd = None
                try:
                    os.unlink(self.lock_file)
                except OSError:
                    pass
