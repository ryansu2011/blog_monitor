import scrapy
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
import json


class SpiderUscrd(scrapy.Spider):
    name = "Uscrd"
    start_urls = ['https://www.uscreditcardguide.com/zh/']

    def parse(self, response):
        articles = response.selector.xpath('//article/div/h2/a[@href]')
        if articles.__len__() is 0:
            raise Exception('Cannot get article list.')
        result = {}
        for article in articles:
            url = article.xpath('@href').get()
            title = article.xpath('text()').get()
            # print('get article:' + title)
            result[title] = url
        js = json.dumps(result, ensure_ascii=False)
        filename = '{}.json'.format(self.name)
        with open(filename, 'wb') as f:
            f.write(js.__str__().encode("utf-8"))
        f.close()


class SpiderMbmyc(scrapy.Spider):
    name = "Mbmyc"
    start_urls = ['https://travelafterwork.com']

    def parse(self, response):
        articles = response.selector.xpath('//article/div/a[@title][@href]')
        if articles.__len__() is 0:
            raise Exception('Cannot get article list.')
        result = {}
        for article in articles:
            url = article.xpath('@href').get()
            title = article.xpath('@title').get()
            # print('get article:' + title)
            result[title] = url
        js = json.dumps(result, ensure_ascii=False)
        filename = '{}.json'.format(self.name)
        with open(filename, 'wb') as f:
            f.write(js.__str__().encode("utf-8"))
        f.close()


class SpiderBm101(scrapy.Spider):
    name = "Bm101"
    start_urls = ['https://www.uscreditcards101.com/zh/']

    def parse(self, response):
        articles = response.selector.xpath('//article/header/h2/a[@title][@href]')
        if articles.__len__() is 0:
            raise Exception('Cannot get article list.')
        result = {}
        for article in articles:
            url = article.xpath('@href').get()
            title = article.xpath('@title').get()
            # print('get article:' + title)
            result[title] = url
        js = json.dumps(result, ensure_ascii=False)
        filename = '{}.json'.format(self.name)
        with open(filename, 'wb') as f:
            f.write(js.__str__().encode("utf-8"))
        f.close()


spiderList = [SpiderUscrd, SpiderMbmyc, SpiderBm101]


def craw_all():
    """
    :yield: dict[str title, str url], for all spiders
    """
    @defer.inlineCallbacks
    def crawl():
        for spd in spiderList:
            yield runner.crawl(spd)
        reactor.stop()
    runner = CrawlerRunner()
    crawl()
    reactor.run()  # the script will block here until the last crawl call is finished
    reactor.__init__()
    for spd in spiderList:
        filename = '{}.json'.format(spd.name)
        with open(filename, 'r') as f:
            output = json.load(f)
        f.close()
        yield output
