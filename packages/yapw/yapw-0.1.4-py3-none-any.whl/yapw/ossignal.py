# Copied and adapted from https://github.com/scrapy/scrapy/blob/master/scrapy/utils/ossignal.py
import signal

signal_names = {}
for signame in dir(signal):
    if signame.startswith("SIG") and not signame.startswith("SIG_"):
        signum = getattr(signal, signame)
        if isinstance(signum, int):
            signal_names[signum] = signame
