import os
from .base import BaseFileLock
from ..exceptions import LockTimeoutError

try:
    import msvcrt
except ImportError:
    msvcrt = None

class WindowsFileLock(BaseFileLock):
    def acquire(self) -> None:
        if not msvcrt:
            return
        self._fd = os.open(self.lock_file, os.O_CREAT | os.O_WRONLY)
        try:
            msvcrt.locking(self._fd, msvcrt.LK_NBLCK, 1)
        except OSError:
            os.close(self._fd)
            self._fd = None
            raise LockTimeoutError(f"Konnte Windows-Dateisperre für {self.filepath} nicht erlangen.")

    def release(self) -> None:
        if self._fd is not None:
            try:
                if msvcrt:
                    os.lseek(self._fd, 0, os.SEEK_SET)
                    msvcrt.locking(self._fd, msvcrt.LK_UNLCK, 1)
            finally:
                os.close(self._fd)
                self._fd = None
                try:
                    os.unlink(self.lock_file)
                except OSError:
                    pass
