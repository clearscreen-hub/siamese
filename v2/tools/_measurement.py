import datetime
import time


class Counter:
    def __init__(self, limit=None):
        """
        if limit is none: the counter is infinite
        :param limit:
        """
        self._cnt = 0
        self._limit = limit

    def __is_infinite(self) -> bool:
        return True if self._limit is None else False

    def reset(self) -> None:
        self._cnt = 0

    def next(self) -> None:
        if self.__is_infinite() or self._cnt != self._limit - 1:
            self._cnt += 1
        else:
            self._cnt = 0

    def __call__(self) -> int:
        return self._cnt


class FPS:
    def __init__(self):
        self._start = None
        self._end = None
        self._n_frame = Counter(limit=None)

    def start(self):
        self._start = datetime.datetime.now()

    def stop(self):
        self._end = datetime.datetime.now()

    def update(self):
        self._n_frame.next()

    def elapsed(self):
        return (self._end - self._start).total_seconds()

    def fps(self) -> float:
        try:
            if self._end is None:
                return self._n_frame()/(datetime.datetime.now()-self._start).total_seconds()
            return self._n_frame() / self.elapsed()
        except ZeroDivisionError:
            return 0.
