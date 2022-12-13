import scrapy
import re
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import urljoin
from dateutil.parser import parse
import datetime as dt
from spider_steam.items import SpiderSteamItem

# сайт парсится английский, не вижу смысла делать хоть какую-то языковую гибкость
# причина очевидна - а зачем? если мы хотим собрать какую-либо статистику, то лучше делать это на английском
# иначе мы уже теряем гибкость в данных, кому наш русский датасет нужен?

# единственное, что имеет гибкость - валюта
# под разными ip она разная, а от это зависит то, как мы будем парсить цену
# Для России - '470,34 руб', США - '$34.66' - повод прописать регулярку
# Почему важно поддерживать разные валюты? Допустим, мы хотим сравнить цены - посчитать своего рода паритет покупательной способности

# queries = ['anime', 'strategy', 'war']


class SteamGamesSpider(scrapy.Spider):
    name = 'SteamGamesSpider'
    base_url = 'https://store.steampowered.com/search/?'

    def __init__(self, pages=5, release_date_boundary='01-01-2001',
                 queries=None, **kwargs):
        if queries is None:
            queries = "strategy, anime, sports"
        self.max_pages = int(pages)
        self.release_date_boundary = parse(release_date_boundary, dayfirst=True)
        self.queries = map(lambda s: s.strip(), queries.split(','))
        super().__init__(**kwargs)

    def start_requests(self):
        for query in self.queries:
            url = self.base_url + urlencode({'term': query, 'page': str(1)})
            yield scrapy.Request(url=url, callback=self.parse_query)

    @staticmethod
    def extract_price(s):
        number = re.search(r'(?:\d*[,.])?\d+', s)
        if number is None:
            return 0
        return float(number.group(0).replace(',', '.'))

    @staticmethod
    def get_text(selector, xpath):
        return selector\
            .xpath(xpath + '/text()')\
            .get().strip()

    @staticmethod
    def get_text_list(selector, xpath):
        return list(map(lambda r: SteamGamesSpider.get_text(r, '.'), selector.xpath(xpath)))

    @staticmethod
    def get_platforms(game_selector):
        platforms_spans = game_selector.xpath('.//span[contains(@class, "platform_img")]')
        return list(map(lambda span: span.attrib['class'].split()[1], platforms_spans))

    @staticmethod
    def get_price_and_discount(game_selector):
            try:
                discount = SteamGamesSpider.get_text(
                    game_selector,
                    './/div[contains(@class, "search_discount")]/span'
                )
            except:
                discount = 0
            if discount == 0:
                initial_price_str = SteamGamesSpider.get_text(
                    game_selector,
                    './/div[contains(@class, "search_price ")]'
                )
                initial_price = SteamGamesSpider.extract_price(initial_price_str) # для бесплатных оно вернет 0
                discounted_price = initial_price
            else:
                discount = int(discount[:-1])
                initial_price_str = SteamGamesSpider.get_text(
                    game_selector,
                    './/div[contains(@class, "search_price discounted")]/span/strike'
                )
                initial_price = SteamGamesSpider.extract_price(initial_price_str)
                discounted_price_str = game_selector\
                    .xpath('.//div[contains(@class, "search_price discounted")]/text()')\
                    .getall()[1].strip()
                discounted_price = SteamGamesSpider.extract_price(discounted_price_str)
            return [initial_price, discounted_price, discount]

    @staticmethod
    def get_release_date(game_selector):
        release_date = SteamGamesSpider.get_text(game_selector, './/div[contains(@class, "search_released")]')
        try:
            release_date = dt.datetime.strftime(parse(release_date), '%d-%m-%Y')
        except:
            release_date = 'Coming soon'
        return release_date

    def parse_query(self, response):
        for game in response.xpath('//a[contains(@class, "search_result_row")]'):
            game_url = game.attrib['href']
            if '/app' in game_url:
                available_platforms = self.get_platforms(game)
                initial_price, discounted_price, discount = self.get_price_and_discount(game)
                release_date = self.get_release_date(game)
                if release_date == "Coming soon" or parse(release_date, dayfirst=True) >= self.release_date_boundary:
                    yield scrapy.Request(url=game_url, callback=self.parse,
                                         cb_kwargs={'available_platforms': available_platforms,
                                                    'release_date': release_date,
                                                    'initial_price': initial_price,
                                                    'discounted_price': discounted_price,
                                                    'discount': discount})

        params = parse_qs(urlparse(response.url).query)
        page = int(params['page'][0])
        query = params['term'][0]
        if page < self.max_pages:
            url = self.base_url + urlencode({'term': query, 'page': str(page + 1)})
            yield scrapy.Request(url=url, callback=self.parse_query)

    @staticmethod
    def get_reviews(response):
        reviews_div = response.xpath('//div[@itemprop = "aggregateRating"]//div[@class = "summary column"]')
        try:
            reviews_number = int(reviews_div.xpath('.//meta[@itemprop = "reviewCount"]').attrib['content'])
            rating_value = int(reviews_div.xpath('.//meta[@itemprop = "ratingValue"]').attrib['content'])
        except:
            reviews_number = 0
            rating_value = 0
        try:
            reviews_summary = SteamGamesSpider.get_text(reviews_div, './/span[@itemprop = "description"]')
        except:
            # "No user reviews"
            reviews_summary = SteamGamesSpider.get_text(reviews_div, '.')
        return reviews_number, rating_value, reviews_summary

    def parse(self, response, **kwargs):
        if 'agecheck' in response.url:
            return
        item = SpiderSteamItem()
        item['title'] = self.get_text(response, '//div[@id = "appHubAppName"]')
        item['category'] = list(map(lambda s: s.strip(), response.xpath('//div[@class = "blockbg"]/a/text()').getall()[1:]))
        item['reviews_number'], item['rating_value'], item['reviews_summary'] = self.get_reviews(response)
        item['release_date'] = kwargs['release_date']
        item['developer'] = self.get_text(response, '//div[@id = "developers_list"]/a')
        item['tags'] = self.get_text_list(response, '//div[@class = "glance_tags popular_tags"]/a[@class = "app_tag"]')
        item['genres']= self.get_text_list(response, '//div[@id = "genresAndManufacturer"]/span/a')
        item['initial_price'] = kwargs['initial_price']
        item['discounted_price'] = kwargs['discounted_price']
        item['discount'] = kwargs['discount']
        item['available_platforms'] = kwargs['available_platforms']
        yield item
