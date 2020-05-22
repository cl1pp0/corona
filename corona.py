#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
import numpy as np
import math
import csv
import urllib.request
import shutil
import os.path
import time
import datetime
import argparse
from pathlib import Path

cachedir = "cache/"
base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"

class DataSeries:
    def __init__(self, name, file):
        self.update = False
        self.name = name
        self.file = cachedir + file
        self.url = base_url + file

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--type", type=str, help="type of figure to be shown (one of 'stacked', 'infected', 'deaths', 'recovered'), default = 'stacked'")
parser.add_argument("-c", "--country", type=str, help="country, default = 'Germany'")
parser.add_argument("-l", "--list", help="list all available countries and their states (overrides -c, -s, -t)", action="store_true")
parser.add_argument("-s", "--state", type=str, help="state, default = ''")
parser.add_argument("-u", "--update", help="force update of cache file (even if it is not outdated)", action="store_true")
parser.add_argument("-v", "--verbose", help="verbose output: print data series and cache info to stdout", action="store_true")
args = parser.parse_args()

if not args.type:
    figtype = 'stacked'
else:
    figtype = args.type

if not args.country:
    country = 'Germany'
else:
    country = args.country

if not args.state:
    state = ''
else:
    state = args.state

data_infected  = DataSeries('infected', 'time_series_covid19_confirmed_global.csv')
data_recovered = DataSeries('recovered', 'time_series_covid19_recovered_global.csv')
data_deaths    = DataSeries('deaths', 'time_series_covid19_deaths_global.csv')

data_series = [data_infected, data_recovered, data_deaths]

Path(cachedir).mkdir(exist_ok=True)

breal  = {'infected': [], 'recovered': [], 'deaths': []}
dbreal = {'infected': [], 'recovered': [], 'deaths': []}

for data in data_series:
    try:
        mtime = os.path.getmtime(data.file)
        # update cache if it is older than 6 hours
        if time.time() - mtime > 21600:
            data.update = 'outdated'
            if args.verbose:
                print("Cache file " + data.file + " outdated, updating...")

    except OSError:
        # update cache if file does not exist
        data.update = 'nofile'
        if args.verbose:
            print("Cache file " + data.file + " missing, updating...")

    if args.update == True:
        data.update = 'force'
        if args.verbose:
            print("Updating cache file " + data.file + " (forced by user)")

    if data.update:
        response = urllib.request.urlopen(data.url)
        with open(data.file, 'wb') as outfile:
            shutil.copyfileobj(response, outfile)
    else:
        if args.verbose:
            print("Cache file " + data.file + " is up-to-date (" + time.ctime(mtime) + ")")

    found_line = False
    with open(data.file, newline='') as csvfile:
        cr = csv.reader(csvfile)
        if args.list:
            next(cr)
            for line in cr:
                if line[0]:
                    print(line[1] + "; " + line[0])
                else:
                    print(line[1])
            exit(0)
        else:
            for line in cr:
                if line[1] == country and line[0] == state:
                    if args.verbose:
                        print(', '.join(line))
                    # begin at 2020-03-01
                    breal[data.name] = [int(num_str) for num_str in line[43:]]
                    found_line = True
                    break

    if not found_line:
        print("error: country \"" + country + "\" or state \"" + state + "\" not found in file " + data.file + " .")
        exit(1)

n = len(breal['infected'])
x = list(range(1, n+1))
xt = x[0::7]

for key in breal:
    for i in range(1, n):
        dbreal[key].append(breal[key][i]-breal[key][i-1])

if figtype == 'stacked':
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('COVID-19 ' + figtype + ' since 2020-03-01 ' + state + ' ' + country, fontsize=16)
    plt.setp(ax1, xticks=xt, xlabel='days', ylabel='cases')
    plt.setp(ax2, xticks=xt, xlabel='days', ylabel='cases')

    ax3 = ax1.twinx()
    plt.setp(ax3, ylabel='%')

    eng_fmt = EngFormatter(sep='')
    ax1.yaxis.set_major_formatter(eng_fmt)
    ax2.yaxis.set_major_formatter(eng_fmt)

    y1 = np.subtract(breal['infected'], np.add(breal['recovered'], breal['deaths']))
    y2 = breal['recovered']
    y3 = breal['deaths']

    y4 = []
    for i in range(1, n):
        y4.append(y1[i] - y1[i-1])

    y4 = np.multiply(np.divide(y4, y1[1:]), 100)
    z = np.zeros(n)

    labels = ['deaths', 'recovered', 'active']
    colors = ['red', 'tab:green', 'tab:blue']
    ax1.stackplot(x, y3, y2, y1, colors=colors, labels=labels)
    ax1.yaxis.tick_right()
    ax1.yaxis.set_label_position('right')

    ax3.plot(x[1:], y4, label='change active %', color='grey')
    ax3.plot(x, z, color='black', linestyle=':')
    ax3.yaxis.tick_left()
    ax3.yaxis.set_label_position('left')

    ax1.set_title('cumulated view')
    ax1.grid(alpha=0.5)
    handles, labels = ax1.get_legend_handles_labels()
    ax1.legend(reversed(handles), reversed(labels), loc='upper left')
    ax3.legend(loc='upper right')

    ax2.plot(x[1:], dbreal['infected'], label='active', color='tab:blue')
    ax2.plot(x[1:], dbreal['recovered'], label='recovered', color='tab:green')
    ax2.plot(x[1:], dbreal['deaths'], label='deaths', color='red')

    ax2.set_title('daily view')

    ax2.legend(loc='upper left')
    ax2.grid(alpha=0.5)

    #fig.tight_layout()
    plt.show()

else:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('COVID-19 ' + figtype + ' since 2020-03-01 ' + state + ' ' + country, fontsize=16)
    plt.setp((ax1, ax2), xticks=xt, xlabel='days')

    eng_fmt = EngFormatter(sep='')
    ax1.yaxis.set_major_formatter(eng_fmt)
    # doesn't work with log scale - didn't figure out why
    ax2.yaxis.set_major_formatter(eng_fmt)

    ax1.plot(x, breal[figtype], '.-')
    ax1.set_title('linear')
    ax1.grid(alpha=0.5)

    ax2.set_yscale('log')
    ax2.plot(x, breal[figtype], '.-')
    ax2.set_title('logarithmic')
    ax2.grid(alpha=0.5)

    plt.show()

