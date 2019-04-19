import time
import math
from ..utils import clr_err


class BaseMetric(object):
    def __init__(self, name, resetable=True, emph=False):
        assert name is not None, clr_err(" Metric must be named. ")
        assert name, clr_err(" Name is empty. ")
        self._name = name
        self.val = 0
        self.resetable = resetable
        self.emph = emph

    def get(self):
        return self._get()

    def update(self, args):
        if isinstance(args, tuple):
            return self._update(*args)
        else:
            return self._update(args)

    def reset(self):
        if self.resetable:
            return self._reset()

    def get_name(self):
        return self._name

    def __repr__(self):
        return "%s::%s" % (self.__class__.__name__, self._name)

    def _get(self):
        raise NotImplementedError

    def _update(self, *args):
        raise NotImplementedError

    def _reset(self):
        raise NotImplementedError


class ValueMetric(BaseMetric):
    def __init__(self, name=None, resetable=True, emph=False):
        BaseMetric.__init__(self, name, resetable, emph)
        self.val = []
    
    def _get(self):
        return self.val
    
    def _update(self, val):
        self.val.append(val)
    
    def _reset(self):
        self.val.clear()


class MaxMetric(BaseMetric):
    def __init__(self, name=None, resetable=True, emph=False):
        BaseMetric.__init__(self, name, resetable, emph)
        self.val = -math.inf

    def _get(self):
        return self.val

    def _update(self, val):
        self.val = max(self.val, val)

    def _reset(self):
        self.val = -math.inf


class SumMetric(BaseMetric):
    def __init__(self, name=None, resetable=True, emph=False):
        BaseMetric.__init__(self, name, resetable, emph)

    def _get(self):
        return self.val

    def _update(self, val):
        self.val += val

    def _reset(self):
        self.val = 0


class AvgMetric(BaseMetric):
    def __init__(self, name=None, resetable=True, emph=False):
        BaseMetric.__init__(self, name, resetable, emph)
        self.counter = 0

    def _get(self):
        return self.val / self.counter

    def _update(self, val, n=1):
        self.val += val
        self.counter += n

    def _reset(self):
        self.val = 0
        self.counter = 0


class EpisodicMetric(BaseMetric):
    def __init__(self, name=None, resetable=True, emph=False):
        BaseMetric.__init__(self, name, resetable, emph)
        self.counter = 0
        self.partial_val = 0

    def _get(self):
        return self.val / self.counter

    def _update(self, val, n=1):
        if n == 0:
            self.partial_val += val
        else:
            self.val += self.partial_val + val
            self.counter += n
            self.partial_val = 0

    def _reset(self):
        self.val = 0
        self.counter = 0
        self.partial_val = 0


class FPSMetric(BaseMetric):
    def __init__(self, name=None, resetable=True, emph=False):
        BaseMetric.__init__(self, name, resetable, emph)
        self.timer = time.time()

    def _get(self):
        return self.val / (time.time() - self.timer)

    def _update(self, val):
        self.val += val

    def _reset(self):
        self.val = 0
        self.timer = time.time()


if __name__ == "__main__":
    pass
