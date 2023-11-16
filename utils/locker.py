# https://stackoverflow.com/a/60214222
import os
from pathlib import Path

MUTEX_FILENAME = ".mutex.lock"
if not os.path.exists(MUTEX_FILENAME):
    Path(MUTEX_FILENAME).touch()

if os.name == "nt":
    import msvcrt

    def portable_lock(fp):
        fp.seek(0)
        msvcrt.locking(fp.fileno(), msvcrt.LK_LOCK, 1)

    def portable_unlock(fp):
        fp.seek(0)
        msvcrt.locking(fp.fileno(), msvcrt.LK_UNLCK, 1)

else:
    import fcntl

    def portable_lock(fp):
        fcntl.flock(fp.fileno(), fcntl.LOCK_EX)

    def portable_unlock(fp):
        fcntl.flock(fp.fileno(), fcntl.LOCK_UN)


class Locker:
    def __enter__(self):
        self.fp = open(MUTEX_FILENAME)
        portable_lock(self.fp)

    def __exit__(self, _type, value, tb):
        portable_unlock(self.fp)
        self.fp.close()
