from .utils import clr_err


class Group(object):
    counter = 0

    def __init__(self, tag=None, metrics=None, console_options=None):
        self.tag = "group%02d" % Group.counter if tag is None else tag

        if metrics is None:
            self.metrics = None
        elif isinstance(metrics, tuple):
            self.metrics = {m.get_name(): m for m in metrics}
        else:
            self.metrics = {metrics.get_name(): metrics}
        self.console_options = console_options
        Group.counter += 1

    def update(self, **kwargs):
        for k, v in kwargs.items():
            assert k in self.metrics, clr_err("The metric you are trying to \
                update is not in the %s Group." % self.tag)

            self.metrics[k].update(v)

    def reset(self):
        for k, v in self.metrics.items():
            v.reset()

    def __repr__(self):
        return self.tag + "::Group"

    def __del__(self):
        type(self).counter -= 1


if __name__ == "__main__":
    pass
