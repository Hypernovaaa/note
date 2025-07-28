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
                        # 填写用户名
                        PageMethod("fill", "input[name='username']", "your_username"),
                        # 可选：填写密码框
                        PageMethod("fill", "input[name='password']", "your_password"),
                        # 点击登录按钮
                        PageMethod("click", "button[type='submit']"),
                        # 等待页面稳定
                        PageMethod("wait_for_load_state", "networkidle"),
                    ],
                },
                callback=self.parse)

    def parse(self, response):
        import pdb; pdb.set_trace()
        print(response)


    