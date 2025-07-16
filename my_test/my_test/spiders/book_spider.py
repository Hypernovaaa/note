import os, shutil, json, random, sys, logging, glob
from pprint import pprint
import scrapy

class BookSpider(scrapy.Spider):
    name = "books"

    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        import pdb; pdb.set_trace()
        # 提取数据
        # 每一本书的信息在<article class="product_pod">中，我们使用
        # css()方法找到所有这样的article 元素，并依次迭代
        for book in response.css('article.product_pod'):
            # 书名信息在article > h3 > a 元素的title属性里
            # 例如: <a title="A Light in the Attic">A Light in the ...</a>
            name = book.xpath('./h3/a/@title').extract_first()
            # 书价信息在 <p class="price_color">的TEXT中。
            # 例如: <p class="price_color">￡51.77</p>
            price = book.css('p.price_color::text').extract_first()
        yield {
            'name': name,
            'price': price,
            }
        # 提取链接
        # 下一页的url 在ul.pager > li.next > a 里面
        # 例如: <li class="next"><a href="catalogue/page-2.html">next</a></li>
        next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        if next_url:
        # 如果找到下一页的URL，得到绝对路径，构造新的Request 对象
            next_url = response.urljoin(next_url)
        yield scrapy.Request(next_url, callback=self.parse)