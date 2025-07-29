import scrapy
from scrapy_playwright.page import PageMethod


class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ["https://www.zhihu.com/signin?next=%2F"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url, 
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        # 等待输入框加载
                        PageMethod("wait_for_selector", "input[name='username']"),
                        PageMethod("wait_for_timeout", 1000),
                        # 填写用户名
                        PageMethod("fill", "input[name='username']", "13052694175"),
                        PageMethod("wait_for_selector", "button:has-text('获取短信验证码')"),
                        PageMethod("click", "button:has-text('获取短信验证码')"),
                        PageMethod("wait_for_timeout", 2000),
                        # 截图
                        PageMethod("screenshot", path="/data/workspace/liuhui/liuhui_work/06_Learning/note/03_爬虫/zhihu_login/ans.png"),
                    ],
                },
                callback=self.parse)

    def parse(self, response):
        import pdb; pdb.set_trace()
        print(response)


    