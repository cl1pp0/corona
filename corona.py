#!/usr/bin/python3

import matplotlib.pyplot as plt
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
parser.add_argument("-s", "--state", type=str, help="state, default = ''")
parser.add_argument("-u", "--update", help="force update of cache file (even if it is not outdated)", action="store_true")
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
            print("Cache file " + data.file + " outdated, updating...")

    except OSError:
        # update cache if file does not exist
        data.update = 'nofile'
        print("Cache file " + data.file + " missing, updating...")

    if args.update == True:
        data.update = 'force'
        print("Updating cache file " + data.file + " (forced by user)")

    if data.update:
        response = urllib.request.urlopen(data.url)
        with open(data.file, 'wb') as outfile:
            shutil.copyfileobj(response, outfile)
    else:
        print("Cache file " + data.file + " is up-to-date (" + time.ctime(mtime) + ")")

    found_line = False
    with open(data.file, newline='') as csvfile:
        cr = csv.reader(csvfile)
        for line in cr:
            if line[1] == country and line[0] == state:
                print(', '.join(line))
                # begin at 2020-03-01
                breal[data.name] = [int(num_str) for num_str in line[43:]]
                found_line = True
                break

    if not found_line:
        print("error: country \"" + country + "\" or state \"" + state + "\" not found in file " + cachefile + " .")
        exit(1)

n = len(breal['infected'])
x = list(range(1, n+1))
xt = x[0::7]

for key in breal:
    for i in range(1, n):
        dbreal[key].append(breal[key][i]-breal[key][i-1])

if figtype != 'stacked':
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('COVID-19 ' + figtype + ' since 2020-03-01 ' + state + ' ' + country, fontsize=16)
    plt.setp((ax1, ax2), xticks=xt, xlabel='days')

    labels = ax1.xaxis.get_ticklabels()
#    for label in labels[::2]:
#        label.set_visible(False)

    labels = ax2.xaxis.get_ticklabels()
#    for label in labels[::2]:
#        label.set_visible(False)

    ax1.plot(x, breal[figtype], '.-')
    #plt.xlim(1, n)
    ax1.set_title('linear')
    #ax1.legend('real')
    ax1.grid()

    ax2.semilogy(x, breal[figtype], '.-')
    #plt.xlim(1, n)
    ax2.set_title('logarithmic')
    #ax2.legend('real')
    ax2.grid()

    plt.show()
else:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('COVID-19 ' + figtype + ' since 2020-03-01 ' + state + ' ' + country, fontsize=16)
    plt.setp(ax1, xticks=xt, xlabel='days')
    plt.setp(ax2, xticks=xt, xlabel='days')

    labels = ax1.xaxis.get_ticklabels()
#    for label in labels[::2]:
#        label.set_visible(False)

    labels = ax2.xaxis.get_ticklabels()
#    for label in labels[::2]:
#        label.set_visible(False)

    y1 = breal['infected']
    y2 = np.add(breal['recovered'], breal['deaths'])
    y3 = breal['deaths']
    y4 = np.divide(dbreal['infected'], np.subtract(y1[1:], y2[1:]))

    ax1.plot(x, y1, label='active', color='tab:blue')
    ax1.plot(x, y2, label='recovered', color='tab:green')
    ax1.plot(x, y3, label='deaths', color='red')
    ax1.plot(x[1:], y4, label='change active %', color='black')

    ax1.fill_between(x, y1, y2, color='tab:blue')
    ax1.fill_between(x, y2, y3, color='tab:green')
    ax1.fill_between(x, y3, color='red')

    #plt.xlim(1, n)
    ax1.set_title('cumulated view')
    ax1.legend()
    ax1.grid()

    ax2.plot(x[1:], dbreal['infected'], label='active', color='tab:blue')
    ax2.plot(x[1:], dbreal['recovered'], label='recovered', color='tab:green')
    ax2.plot(x[1:], dbreal['deaths'], label='deaths', color='red')

    ax2.set_title('daily view')
    ax2.legend()
    ax2.grid()

    plt.show()

