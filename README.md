# SteamParser

An application for parsing Steam - online game store - using scrapy spiders.

## Usage

To run parser:

1. Add queries you want to search to **SteamParser/spider_steam/spiders/SteamGamesSpider.py** to *queries* variable. You can also chage *SteamGamesSpider.max_pages* variable to alter the number of parsed search pages.
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
