import scrapy
from scrapy.linkextractors import LinkExtractor



class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["matplotlib.org"]
    start_urls = ["https://matplotlib.org/stable/plot_types/index.html"]

    def parse(self, response):
        le = LinkExtractor(restrict_css="div.sphx-glr-thumbcontainer a[class][href]")
        links = le.extract_links(response)
        for link in links:
            print(link.url)
            yield scrapy.Request(link.url, callback=self.parse_sub_page)

    def parse_sub_page(self, response):
        pass 



