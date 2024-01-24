#!/usr/bin/python3
# -*- coding: utf-8 -*-

# imports

from .__init__ import __doc__ as DESCRIPTION, __version__ as VERSION, int2human
from argparse import ArgumentParser as Parser, RawDescriptionHelpFormatter as Formatter
from math import log
from psutil import virtual_memory as mem, swap_memory as swap
from psutil import cpu_percent as cpu, sensors_temperatures as temp
from psutil import disk_io_counters as disk, net_io_counters as net
from sys import argv, exit
from time import localtime, sleep, time
from warnings import simplefilter

# '·' middle dot

# constants

FORMATS = 'yhmMcCrRdD'
LOG1024 = log(1024)

# classes

class Arguments: pass # container for arguments
arg = Arguments()

# functions

def ints(start=0, step=1):
    i = start
    while True:
        yield i
        i += step

def YYYY_mm_dd(): return "%04d-%02d-%02d" % localtime()[:3]

def HH_MM_SS(): return "%02d:%02d:%02d" % localtime()[3:6]

def header():
    titles = []
    width = 25 if arg.tera_byte else 19
    for char in arg.format:
        if char == 'y':   titles.append('YYYY-mm-dd')
        elif char == 'h': titles.append('HH:MM:SS')
        elif char == 'm': titles.append('M% S%')
        elif char == 'M': titles.append('0 · · · ·50 · · · 100')
        elif char == 'c': titles.append('C% T°')
        elif char == 'C': titles.append('0 · · · ·50 · · · 100')
        elif char == 'r': titles.append('R-B/s W-B/s')
        elif char == 'R': titles.append('1 · · K · · M · · G · · T'[:width])
        elif char == 'd': titles.append('D-B/s U-B/s')
        elif char == 'D': titles.append('1 · · K · · M · · G · · T'[:width])
    return ' '.join(titles)    

def line(m, s, c, t, r, w, d, u, i):
    fields = []
    for char in arg.format:
        if char == 'y':   fields.append(YYYY_mm_dd())
        elif char == 'h': fields.append(HH_MM_SS())
        elif char == 'm': fields.append(two_digits(m) + ' ' + two_digits(s))
        elif char == 'M': fields.append(linear_graph([m, s], 'MS', i))
        elif char == 'c': fields.append(two_digits(c) + ' ' + two_digits(t))
        elif char == 'C': fields.append(linear_graph([c, t], 'CT', i))
        elif char == 'r': fields.append(human(r) + ' ' + human(w))
        elif char == 'R': fields.append(logarithmic_graph([r, w], 'RW', i))
        elif char == 'd': fields.append(human(d) + ' ' + human(u))
        elif char == 'D': fields.append(logarithmic_graph([d, u], 'DU', i))
    return ' '.join(fields)    

def two_digits(x):
    '2-digits display (linear_graph data)'
    x = round(x)
    return ' 0' if x <= 0 else '**' if x >= 100 else '%2d' % x

def linear_graph(xx, cc, i):
    'linear graph'
    hh = list('├─────────┼─────────┤' if i % 5 == 0 else '│ · · · · │ · · · · │')
    for x, c in zip(xx, cc):
        j = max(0, min(20, round(0.2 * x)))
        hh[j] = 'X' if 'A' <= hh[j] <= 'Z' else c
    return ''.join(hh)
            
def human(x):
    '5-chars display (logarithmic data)'
    return int2human(max(0, round(x)), length=5)

def logarithmic_graph(xx, cc, i):
    'logarithmic graph'
    if arg.tera_byte:
        hh = list('├─────┼─────┼─────┼─────┤' if i % 5 == 0 else '│ · · │ · · │ · · │ · · │')
    else:
        hh = list('├─────┼─────┼─────┤' if i % 5 == 0 else '│ · · │ · · │ · · │')
    for x, c in zip(xx, cc):
        j = max(0, min(len(hh) - 1, round(6.0 * log(max(1.0, x)) / LOG1024)))
        hh[j] = 'X' if 'A' <= hh[j] <= 'Z' else c
    return ''.join(hh)

def get_arguments(argv):
    parser = Parser(prog="minmon", formatter_class=Formatter, description=DESCRIPTION)
    parser.add_argument("-V","--version", action="version", version=f"MINMON {VERSION}")
    parser.add_argument("-s","--seconds", type=str, default='1', help="interval in seconds as an integer greater than 0 (default: '1')")
    parser.add_argument("-f","--format", type=str, default=FORMATS, help=f"output format (default: {FORMATS!r})")
    parser.add_argument("-t","--tera-byte", action='store_true', help=f"extended 25-characters '1-K-M-G-T' logarithmic scale (default: 19-characters '1-K-M-G')")
    parser.parse_args(argv[1:], arg)

def check_arguments():
    try:
        seconds = int(arg.seconds)
        assert seconds > 0
        arg.seconds = seconds
    except (ValueError, AssertionError):
        exit(f'minmon: wrong -s --seconds {arg.seconds!r} should be an integer greater than zero')
    for char in arg.format:
        if char not in FORMATS:
            exit(f'minmon: wrong -f --format {arg.format!r}, character {char!r} should be in {FORMATS!r}')
            
def minmon(argv):
    get_arguments(argv)
    check_arguments()
    print(header())
    r0, w0, d0, u0, k0, k2 = 0, 0, 0, 0, 0.0, arg.seconds
    for i in ints(-1):
        dk = k2 - k0
        k0 = time()
        m = mem().percent
        s = swap().percent
        c = cpu()
        t = max([x.current for xx in temp().values() for x in xx], default=0)
        r1 = disk().read_bytes;  r = max(0, r1 - r0) / dk; r0 = r1
        w1 = disk().write_bytes; w = max(0, w1 - w0) / dk; w0 = w1
        d1 = net().bytes_recv;   d = max(0, d1 - d0) / dk; d0 = d1
        u1 = net().bytes_sent;   u = max(0, u1 - u0) / dk; u0 = u1
        if i >= 0:
            print(line(m, s, c, t, r, w, d, u, i))
        k1 = time()
        sleep(max(0, arg.seconds - (k1 - k0)))
        k2 = time()
            
def main():
    simplefilter('ignore')
    try:
        minmon(argv)
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()

