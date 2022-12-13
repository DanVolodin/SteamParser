# SteamParser

An application for parsing Steam - online game store - using scrapy spiders.

## Usage

To run parser:

1. Install scrapy:

```sh
$ pip install scrapy
```

2. If you get a warning - add the named directory to your $PATH variable
3. Open project repository in console
4. Run

```sh
$ scrapy crawl SteamGamesSpider -O result.json --nolog
```
The result will be saved to result.json file

5*. You can define your own parameters which are described in the next abstract

## Parameters

You can define 3 parameters:

  * Number of pages to search for each query - **pages** - *5* default
  * Release date filter - **release_date_boundary** - in dayfirst format - *01-01-2001* default
  * Queries to search - **queries** - in *"query_1, query_2, ..., query_n"* format - *"strategy, anime, sports"* default

To add any of them you need to add ```-a NAME=VALUE``` option to the running command

Example:

```
scrapy crawl SteamGamesSpider -O games.json -a pages=2 -a release_date_boundary=01-01-2015 -a queries="anime, sims, football"

```
This will find all games released after 1 January 2015 that can be found in the first 2 pages of search queries "anime", "sims" and "football". The result of this query can be seen it the *games.json* file.

## JSON result data types

```perl
[
  {
    "title" : string,
    "category" : array[string],
    "reviews_number" : int,
    "rating_value" : int,
    "reviews_summary" : string,
    "release_date" : string, # in '%d-%m-%Y format
    "developer" : string,
    "tags" : array[string],
    "genres" : array[string],
    "initial_price" : float,
    "discounted_price" : float,
    "discount" : int, # e.g.: -31 means -31%
    "available_platforms" : array[string]
  }
]
```
