import os
import sys
import time
import datetime
import json
import pickle
from termcolor import colored as clr

from .group import Group
from .utils import clr_err
from .metrics import AvgMetric, MaxMetric, SumMetric, FPSMetric, EpisodicMetric


class Logger(object):
    def __init__(self, label="Logger", path=None):
        self.label = label

        self.path = path
        if path is None:
            self.path = os.path.join(os.getcwd(), label)

        try:
            print("Creating directory %s." % str(self.path))
            os.makedirs(self.path)
        except FileExistsError:
            print("Warning! Directory %s exists, results may be overwritten!"
                  % str(self.path))

        self.groups = {}

        # Need to change this
        self.AvgMetric = AvgMetric
        self.MaxMetric = MaxMetric
        self.SumMetric = SumMetric
        self.FPSMetric = FPSMetric
        self.EpisodicMetric = EpisodicMetric

        self.console = ConsoleLogger()

        self.start_time = time.time()
        self.step_idx = 0

    def add_group(self, **kwargs):
        group = Group(**kwargs)
        assert group.tag not in self.groups, clr_err(
            "Group %s already added to logger." % group.tag)

        self.groups[group.tag] = group
        self.console.add_group_meta(group)

        return self.groups[group.tag]

    def log_info(self, group, info):
        self.console.log_info(group, info)

    def log_time(self, group):
        info = "date: %s." % time.strftime("%d/%m/%Y | %H:%M:%S")
        self.console.log_info(group, info)

    def log(self, group, step_idx):
        x_metrics = {
            "step_idx": step_idx,
            "time_idx": time.time() - self.start_time
        }

        self.console.log(group, x_metrics)
        self._save(group, x_metrics)

    def _save(self, group, x_metrics):
        filename = '%s.pkl' % group.tag.replace(" ", "_").lower()
        path = os.path.join(self.path, filename)

        step_idx = x_metrics["step_idx"]
        time_idx = x_metrics["time_idx"]
        
        try:
            with open(path, 'rb') as f:
                group_hist = pickle.load(f)
        except FileNotFoundError:
            group_hist = {k: [] for k in group.metrics.keys()}

        for metric_name, metric in group.metrics.items():
            group_hist[metric_name].append({
                "step_idx": step_idx,
                "time_idx": time_idx,
                "value": metric.get()
            })

        with open(path, 'wb') as f:
            pickle.dump(group_hist, f)

    def __str__(self):
        return f'{self.__class__.__name__}'

    def __repr__(self):
        obj_id = hex(id(self))
        name = self.__str__()
        return f'{name} @ {obj_id}'


class ConsoleLogger(object):
    def __init__(self):
        try:
            columns = os.get_terminal_size(0).columns
        except OSError:
            columns = 80
        self.console_width = min(columns, 80)
        self.group_display_meta = {}

    def add_group_meta(self, group):
        group_name = group.tag
        display_name = " %s " % group_name
        if group.metrics is None:
            max_metric_len = 0
        else:
            max_metric_len = max(list(map(len, group.metrics.keys())))
        self.group_display_meta[group_name] = {
            "display_name": clr(display_name, *group.console_options),
            "color": group.console_options,
            "name_len": len(group_name),
            "max_metrics_len": max_metric_len
        }

    def log_info(self, group, info):
        meta = self.group_display_meta[group.tag]

        # display header
        left = (meta["display_name"], meta["name_len"] + 2)
        right = (info, len(info))
        print(self.justify_right(left, right))
        sys.stdout.flush()

    def log(self, group, x_metrics):
        y_metrics = [(v.get_name(), v.get(), v.emph) for k, v in
                     group.metrics.items()]

        self.display(group.tag, y_metrics, x_metrics)
        sys.stdout.flush()

    def justify_right(self, left, right, bold=False):
        left, l_len = left
        right, r_len = right
        padding = "." * (self.console_width - (l_len + r_len) - 3)
        if bold:
            padding = clr(padding, attrs=['bold'])
        return "%s %s %s" % (left, padding, right)

    def display(self, group_name, y_metrics, x_metrics):
        meta = self.group_display_meta[group_name]

        # display header
        x_idx = "%8d steps | %s elapsed." % (
            x_metrics["step_idx"],
            str(datetime.timedelta(seconds=x_metrics["time_idx"]))[:-7])
        self._display_header(meta, x_idx)

        # display y_metrics
        for m in y_metrics:
            metric_label = "    | %s" % m[0]
            val = "%05.3f." % m[1]
            emph = m[2]
            if emph:
                left = (clr(metric_label, attrs=['bold']), len(metric_label))
                right = (clr(val, attrs=['bold']), len(val))
            else:
                left = (metric_label, len(metric_label))
                right = (val, len(val))
            print(self.justify_right(left, right))

    def _display_header(self, meta, x_idx):
        left = (meta["display_name"], meta["name_len"] + 2)
        right = (clr(x_idx, attrs=["bold"]), len(x_idx))
        print(self.justify_right(left, right, bold=True))
