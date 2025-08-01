import scrapy
from scrapy_playwright.page import PageMethod
from playwright.async_api import Page
from PIL import Image
import base64, requests
import asyncio
from scipy import interpolate
import numpy as np

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

async def drag_slide(page:Page, start, end):
    '''拟人拖动滑块 
    Arguments:
        arg
    Returns:
        out
    '''
    ctrl = [
      (start[0], start[1]),
      ((start[0] + end[0]) / 2, start[1] - 50),
      end
    ]
    points = np.array(ctrl)
    t = range(len(points))
    num_points = 50
    t_new = np.linspace(0, len(points) - 1, num_points)
    x_t = interpolate.splrep(t, points[:,0], k=2)
    y_t = interpolate.splrep(t, points[:,1], k=2)
    x_i = interpolate.splev(t_new, x_t)
    y_i = interpolate.splev(t_new, y_t)
    path_points = [(x,y) for x, y in zip(x_i, y_i)]
    print(path_points)

    await page.mouse.move(start[0], start[1])
    await page.mouse.down()

    num_step = 1
    for x, y in path_points[1:]:
        await page.mouse.move(x, y)
        if num_step < (num_points * 3 / 4):
            wait_time = 0.0005 * (num_points / num_step)
        else:
            wait_time = 0.002 * (num_points / (num_points - num_step))
        await asyncio.sleep(wait_time)
        num_step += 1

    await asyncio.sleep(1.5)
    await page.mouse.up()

class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ["https://www.zhihu.com/signin?next=%2F"]

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url, 
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        # 等待输入框加载
                        PageMethod("add_init_script", """
                            console.log('Running init script to modify navigator.webdriver');
                            Object.defineProperty(navigator, 'webdriver',{get:()=>undefined});
                            Object.defineProperty(navigator, 'languages',{get:()=>['en-US','en']});
                            Object.defineProperty(navigator, 'plugins',{get:()=>[1,2,3,4,5]});
                            window.chrome = {runtime:{}};
                            console.log('navigator.webdriver after modification:', navigator.webdriver);
                            console.log('navigator.webdriver after modification:', navigator.plugins);
                        """),
                        PageMethod("wait_for_selector", "input[name='username']"),
                        # 填写用户名
                        PageMethod("fill", "input[name='username']", "13052694175"),
                        PageMethod("wait_for_timeout", 1000),
                        PageMethod("wait_for_selector", "button:has-text('获取短信验证码')"),
                        PageMethod("click", "button:has-text('获取短信验证码')"),
                        PageMethod("wait_for_timeout", 1000),
                        # 截图
                        PageMethod("screenshot", path="./ans.png"),
                        # PageMethod("pause")
                    ],
                },
                callback=self.login)
    
    async def login(self, response):
        page: Page = response.meta["playwright_page"]

        # 等待验证码加载完成
        await asyncio.sleep(2)
        await page.wait_for_selector("div.yidun_bgimg")

        img = Image.open("./ans.png")
        box = (460, 140, 820, 440)
        slide_img = img.crop(box)
        slide_img.save("./slide.png")

        with open("./slide.png", "rb") as f:
            b = base64.b64encode(f.read()).decode()  ## 图片二进制流base64字符串
        pixel_offset = verify(b)
        x_start = 33 + 460
        y_start = 258 + 140

        x_end = x_start + pixel_offset + 15
        y_end = y_start + 20

        await drag_slide(page, (x_start, y_start), (x_end, y_end))

        print(f"------------------------------------------> offset : {pixel_offset}")
        await page.screenshot(path="./moved.png")
        await page.mouse.up()
        await page.wait_for_timeout(2 * 1000)
        await page.screenshot(path="./final.png")


    def parse(self, response):
        import pdb; pdb.set_trace()
        print(response)
    