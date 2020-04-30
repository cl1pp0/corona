# corona.py
## Visualize covid-19 cases (data taken from Johns Hopkins git repo)

Data source:
[CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series)

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

## Example plots:

```
$ ./corona.py -c 'US'
```
![Figure_1](https://user-images.githubusercontent.com/28967414/80757493-8a1df200-8b34-11ea-8ea8-bed1d83bb69a.png)

```
$ ./corona.py -c 'US' -t 'infected'
```
![Figure_2](https://user-images.githubusercontent.com/28967414/80757488-89855b80-8b34-11ea-9315-982580908a4c.png)

