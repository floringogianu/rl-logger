import datetime
from termcolor import colored as clr


def clr_err(*args):
    return clr(" %s " % " ".join(args), 'white', 'on_red', attrs=['bold'])
