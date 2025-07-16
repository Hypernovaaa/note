import scrapy 
from scrapy.http import FormRequest


class ZhihuLongin(scrapy.Spider):
    name = "login"

    async def start(self):
        url = "https://www.zhihu.com/signin?next=%2F"
        yield scrapy.Request(url=url, callback=self.login)

    def login(self, response):
        import pdb; pdb.set_trace()

