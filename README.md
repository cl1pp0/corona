# corona.py
## Visualize covid-19 cases (data taken from Johns Hopkins git repo)

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

![Figure_1](https://user-images.githubusercontent.com/28967414/80623831-15bb5400-8a4b-11ea-898a-dbaacd58e400.png)

```
$ ./corona.py -t 'infected'
```

![Figure_2](https://user-images.githubusercontent.com/28967414/80623829-1522bd80-8a4b-11ea-86a0-9cc3cbb8ecb8.png)

