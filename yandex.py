import scrapy


class YandexSpider(scrapy.Spider):
    name = "yandex"
    allowed_domains = ["yandex.com"]
    start_urls = ["https://yandex.com"]

    def parse(self, response):
        pass
