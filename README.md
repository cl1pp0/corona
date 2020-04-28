# corona.py
## visualize covid-19 cases (data taken from Johns Hopkins git repo)

```
usage: corona.py [-h] [-t TYPE] [-c COUNTRY] [-s STATE] [-u]

optional arguments:
  -h, --help            show this help message and exit
  -t TYPE, --type TYPE  type of figure to be shown (one of 'stacked',
                        'infected', 'deaths', 'recovered'), default =
                        'stacked'
  -c COUNTRY, --country COUNTRY
                        country, default = 'Germany'
  -s STATE, --state STATE
                        state, default = ''
  -u, --update          force update of cache file (even if it is not
                        outdated)
```
