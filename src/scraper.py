import scrapy
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
import json

settings_ref = None


class GeneralSpider(scrapy.Spider):
    name = "GeneralSpider"

    def start_requests(self):
        global settings_ref
        for i in range(settings_ref.n):
            url = settings_ref.url_list[i]
            yield scrapy.Request(url=url, callback=self.parse, meta={'index': i})

    def parse(self, response):
        global settings_ref
        # parameters for this response
        index = response.meta['index']
        title_xpath = settings_ref.title_xpath_list[index]
        href_xpath = settings_ref.href_xpath_list[index]
        filename = settings_ref.temp_file_name[index]
        # select
        title_list = response.selector.xpath(title_xpath)
        href_list = response.selector.xpath(href_xpath)
        if title_list.__len__() is 0:
            raise Exception('Cannot get article list.')
        if title_list.__len__() is not href_list.__len__():
            raise Exception('Number of title_list is different from number of href_list')
        # output result
        result = {}
        for i in range(title_list.__len__()):
            result[title_list[i].get()] = href_list[i].get()
        js = json.dumps(result, ensure_ascii=False)
        with open(filename, 'wb') as f:
            f.write(js.__str__().encode("utf-8"))
        f.close()


def craw_all():
    """
    :return: list of dict[str title, str url], for all sites
    """
    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(GeneralSpider)
        reactor.stop()
    global settings_ref
    runner = CrawlerRunner()
    crawl()
    reactor.run()  # the config will block here until the last crawl call is finished
    reactor.__init__()
    ret = []
    for filename in settings_ref.temp_file_name:
        with open(filename, 'r') as f:
            output = json.load(f)
        f.close()
        ret.append(output)
    return ret

