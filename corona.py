import matplotlib.pyplot as plt
import math
import csv
import urllib.request
import shutil
import os.path
import time
import datetime
import argparse
from pathlib import Path
from scipy.optimize import curve_fit
import numpy as np

url_infected  = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
url_deaths    = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
url_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--type", type=str, help="type of figure to be shown (one of 'infected', 'deaths', 'recovered'), default = 'infected'")
parser.add_argument("-c", "--country", type=str, help="country, default = 'Germany'")
parser.add_argument("-s", "--state", type=str, help="state, default = ''")
parser.add_argument("-u", "--update", help="force update of cache file (even if it is not outdated)", action="store_true")
args = parser.parse_args()

if args.type == 'deaths':
    url = url_deaths
    figtype = args.type
elif args.type == 'recovered':
    url = url_recovered
    figtype = args.type
else:
    url = url_infected
    figtype = 'infected'

if not args.country:
    country = 'Germany'
else:
    country = args.country

if not args.state:
    state = ''
else:
    state = args.state

cachedir = "cache"
Path(cachedir).mkdir(exist_ok=True)

if url == url_deaths:
    cachefile = cachedir + "/" + "deaths.csv"
elif url == url_infected:
    cachefile = cachedir + "/" + "infected.csv"
elif url == url_recovered:
    cachefile = cachedir + "/" + "recovered.csv"
else:
    print("no valid url")
    exit(1)

update_cache = False

try:
    # update cache if not done today
    mtime = os.path.getmtime(cachefile)
    if datetime.datetime.today().date() > datetime.datetime.fromtimestamp(mtime).date():
        update_cache = True
        print("Updating cache file since it is not up-to-date (last update: %s)" % time.ctime(mtime))
except OSError:
    update_cache = True
    print("Updating cache file since it doesn't exist")

if args.update == True:
    update_cache = True
    print("Updating cache file (forced by user)")

if update_cache:
    response = urllib.request.urlopen(url)
    with open(cachefile, 'wb') as outfile:
        shutil.copyfileobj(response, outfile)
else:
    print("Cache file is up-to-date")

breal = []
found_line = False

#data = response.read().decode(response.headers.get_content_charset())
with open(cachefile, newline='') as csvfile:
    cr = csv.reader(csvfile)
    for line in cr:
        if line[1] == country and line[0] == state:
            print(', '.join(line))
            # begin at 2020-03-01
            breal = [int(num_str) for num_str in line[43:]]
            found_line = True
            break

if not found_line:
    print("error: country \"" + country + "\" or state \"" + state + "\" not found in data file.")    
    exit(1)

n = len(breal)
t2 = 3
b = 2
lambd = math.log(2)/t2
x = list(range(1, n+1))
xt = list(range(0, n+1, 2))
bcalc = []
bcalc.append(breal[0])

def expcurve(t, b0, b, t2):
    return b0*np.exp(b, 1/t2*t)

popt, pcov = curve_fit(expcurve, x, breal)
popt

#bcalc2 = expcurve(x, *popt)

for t in range(1,n):
    # explicit form
    #bcalc.append(bcalc[0]*math.pow(b, 1/t2*t))
    # recursive form
    bcalc.append(bcalc[-1]*math.exp(lambd))

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('COVID-19 ' + figtype + ' since 2020-03-01 ' + state + ' ' + country, fontsize=16)
plt.setp((ax1, ax2), xticks=x, xlabel='Tage')

labels = ax1.xaxis.get_ticklabels()
for label in labels[::2]:
    label.set_visible(False)

labels = ax2.xaxis.get_ticklabels()
for label in labels[::2]:
    label.set_visible(False)

ax1.plot(x, breal, '.-', x, bcalc, '.-')
#plt.xlim(1, n)
ax1.set_title('linear')
ax1.legend(['real', 'berechnet'])
ax1.grid()

ax2.semilogy(x, breal, '.-', x, bcalc, '.-')
#plt.xlim(1, n)
ax2.set_title('logarithmisch')
ax2.legend(['real', 'berechnet'])
ax2.grid()

plt.show()
