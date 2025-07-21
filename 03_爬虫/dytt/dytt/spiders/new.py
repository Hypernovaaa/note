import scrapy
from scrapy.linkextractors import LinkExtractor
from pprint import pprint 


class NewSpider(scrapy.Spider):
    name = "new"
    allowed_domains = ["dydytt.net"]
    start_urls = ["https://dydytt.net/html/gndy/dyzz/index.html"]

    def parse(self, response):
        le = LinkExtractor(restrict_css="table a[class]")
        links = le.extract_links(response)
        pprint([i.url for i in links])
        # for link in links:
        #     yield scrapy.Request(link.url, callback=self.parse_megnet)

        # 翻页
        n_page = LinkExtractor(restrict_xpaths="//a[text()='下一页']")
        n_page_url = n_page.extract_links(response)
        if n_page_url:
            yield scrapy.Request(n_page_url[0].url, callback=self.parse)


    def parse_megnet(self, response):
        pass 
