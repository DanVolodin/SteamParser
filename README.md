# SteamParser

An application for parsing Steam - online game store - using scrapy spiders.

## Usage

To run parser:

1. Add queries you want to search to **SteamParser/spider_steam/spiders/SteamGamesSpider.py** to *queries* variable
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
