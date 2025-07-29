import scrapy
from scrapy_playwright.page import PageMethod
from playwright.async_api import Page
from PIL import Image
import base64, requests
import asyncio

def verify(b):
    url = "http://api.jfbym.com/api/YmServer/customApi"
    data = {
        ## 关于参数,一般来说有3个;不同类型id可能有不同的参数个数和参数名,找客服获取
        "token": "lGqPHEFLWd4iSv2pgbsj_dJZUuNd0ef3pBEvsXQxR3c",
        "type": "22222",
        "image": b,
    }
    _headers = {
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=_headers, json=data).json()
    return int(response["data"]["data"])

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
                        PageMethod("screenshot", path="./ans.png"),
                        # PageMethod("pause")
                    ],
                },
                callback=self.login)
    
    async def login(self, response):
        page: Page = response.meta["playwright_page"]
        img = Image.open("./ans.png")
        box = (460, 140, 820, 440)
        slide_img = img.crop(box)
        slide_img.save("./slide.png")

        with open("./slide.png", "rb") as f:
            b = base64.b64encode(f.read()).decode()  ## 图片二进制流base64字符串
        pixel_offset = verify(b)
        x_start = 33 + 460
        y_start = 258 + 140
        await page.mouse.move(x_start, y_start)
        await page.mouse.down()

        total = int(pixel_offset + 10)
        current = 0
        while current < total:
            step = min(5, total - current)
            current += step
            await page.mouse.move(x_start + current, y_start, steps=1)
            await asyncio.sleep(0.02)

        print(f"------------------------------------------> offset : {pixel_offset}")
        await page.screenshot(path="./moved.png")
        await page.mouse.up()


    def parse(self, response):
        import pdb; pdb.set_trace()
        print(response)


    