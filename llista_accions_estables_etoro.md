- [Using yfinance](#using-yfinance)
  - [If not working](#if-not-working)
- [Simple investing strategy](#simple-investing-strategy)
  - [Indices](#indices)
- [WINNERS](#winners)
  - [What should be the base value of a stock?](#what-should-be-the-base-value-of-a-stock)
  - [6 month trend suggests increase](#6-month-trend-suggests-increase)
  - [around global minimum:](#around-global-minimum)
  - [slow down, sudden ups](#slow-down-sudden-ups)
  - [slow down trend last 6 months](#slow-down-trend-last-6-months)
  - [slow up, last 3 years](#slow-up-last-3-years)
  - [around global maximum](#around-global-maximum)
  - [1 week trend up](#1-week-trend-up)
- [LOOSERS](#loosers)
  - [around global minimum:](#around-global-minimum-1)
  - [down trend last month](#down-trend-last-month)
  - [3 year, pretty stable, local minimum](#3-year-pretty-stable-local-minimum)
  - [3year trend down, 6 month super down trend](#3year-trend-down-6-month-super-down-trend)
  - [6 month global maximum](#6-month-global-maximum)
  - [6 month stable](#6-month-stable)
- [Market hours](#market-hours)
- [Considereant en invertir](#considereant-en-invertir)
  - [2 abril 2023](#2-abril-2023)
    - [Cryptos:](#cryptos)
    - [Jo invertiria en:](#jo-invertiria-en)


# Using yfinance

## If not working

This is a suggested solution > https://github.com/ranaroussi/yfinance/issues/1484 uprade the yfinance version.

# Simple investing strategy

1. Compute the daily density distributions for the last 6 Months and 1 Year. See if currently the stock price is around the Minimum, Max, or Median of that density.

2. Compute the trend for that period using a linear regression.
3. Check this trend by taking a look at the main indices, and confirm the trend of the stock follows that of the indices. If it doesn't, then the period trend is uncertain.
4. Compute the instanteneous trend of the stock by running a linear regression of the last 5 days of the stock price.
5. Invest in those stocks that have:
   1. Are around the minimum or the mean of the density distribution.
   2. A non negative trend for the period.
   3. A non negative instantaneous trend.

## Indices

Indices include:

1. NASDAQ
2. DJ30
3. SPX500
4. GER40

# WINNERS

## What should be the base value of a stock?

We can consider the "real" or "base" value of a stock, to be the daily mean over the last 2 years. Because we are not interested in longer returns, we will invest monthly or weekly, and a 2 year period
should provide a stable enough base value.

## 6 month trend suggests increase
- tesla
- google
- cocoa *last week trend is up*
- nvidia *1 week stable*

## around global minimum:
- riot
- gamestop  *slow down, sudden ups*


## slow down, sudden ups

## slow down trend last 6 months
- Nestlé *slow down for last 3 years, for last 6 months just quite uncertain*
- xiaomi - *why the fuck did I buy this?*

## slow up, last 3 years
- LG *weekly trend strong up*

## around global maximum
- Manchester united   *stable last 6 months*
- copper *1M stable, 1 week up trend*
  
## 1 week trend up


# LOOSERS

## around global minimum:
- Juventus  *stable last 6 months*

## down trend last month
- soy beans

## 3 year, pretty stable, local minimum
- corn

## 3year trend down, 6 month super down trend
- palladium
- credit suisse *last week strong down*

## 6 month global maximum
- bitcoin *weekly stable*


## 6 month stable
- cardano *weekly stable*
- herbalife *1M, 1 week, down*
- cotton *1M, 1 week, down*


# Market hours

| actiu  | obra  | tanca  | pausa |   |
|---|---|---|---|---|
|  *accions* |  | |  |   |
|   **NASDAQ** |  2:30pm |  9pm  |   |   |
|   **Hong Kong** |  2:30am |  9am  |  |   |
|   **US stocks** |  3:30pm |  22pm  |  |   |
|   **Frankfurt, Madrid, Italia** |  9am |  5:30pm  |  |   |
|  *index* |  | |  |   |
|  *recursos* |  | |  |   |
|  **copper** |  11pm |  9:30pm  |  |   |
|  **suggar** |  9:30am  |  6pm  |  |   |
|  **soy beans** |  1am  |  7:20pm  |  1.45-2.30pm  |   |
|  **palladium** |  11pm |  9:30pm  |   |   |
|  **cotton** |  2am  |  7:20pm  |  |   |
|  **cocoa** |  10:45am  |  6:30pm  |   |   |
|  **corn** |  1am  |  7:20pm  |  1.45-2.30pm  |   |
|  **zinc** |  2am  |  7:55pm  | |   |

1. Si un mercat obra a les hores *am* vol dir que obra dilluns, si obra a les hores *pm* vol dir que obra diumenge. Totes les hores de tancar són per divendres.
2. Tot actiu fa una pausa de la hora de tancada del dia actual, fins a la hora d'obertura del dia següent. La pausa que és llista és si és adicional a aquesta.

# Considereant en invertir

## 2 abril 2023

1. Samsung, puja en els últims *15 dies* un **11%** i en els últims *6 mesos* puja un **30%**
2. Més en TESLA, però puja continuament desde els últimes *15 dies* un **23%**, però en *l'últim any* perd un **42%** del valor
3. Phillips, però baixa en els *útlims 2 anys* un **50%** del valor. En l'*última setmana* puja un **11%**
4. Juventus: *últims 4 mesos* puja un **15%**. Últims *4 dies* puja un **10%**
5. Man United: puja de cop, en els últims *6 mesos*, un **65%**, *ultim mes* puja un **9%**, els últims dies **baixa** esperar uns dies per comprar
6. Xiaomi: *últims 6 mesos* puja un **38%**, últims *15 dies* puja un **10%**
7. Més en Nvidia: puja contínuament desde els últims *6 mesos* un **130%**
8. Més en Riot: puja continuament en els últims *3 mesos* un **200%**
9. Més en Credit Suisse, puja en els últims *10 dies* un **10%**, en els últims *6 mesos* ha perdunt un **80%** del valor.
10. Més en Honda que puja continuament (amb pics i valls) en els últims *6 mesos* un **22%**

### Cryptos:
1. Bitcoin
2. Ethereum
3. Cardano

### Jo invertiria en:

1. Phillips 150€
2. Manchester united, en 3 dies.
3. Juventus 100€
4. Samsung 150€
5. 50€ en Tesla