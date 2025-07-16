import scrapy 
from pprint import pprint 

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"

    async def start(self):
        cookies = {
            '_xsrf': 'fAV1ddETS08U6k2nVMd3p2vIf5QN1qDz',
            '_zap': 'ec14958c-f067-49c9-9ecd-50a93d32b301',
            'd_c0': 'TqbTzdTuuBqPTvrDVMxoYjkgVFxngXScfxM=|1751867237',
            'captcha_session_v2': '2|1:0|10:1751867238|18:captcha_session_v2|88:L2R1amYxR1Y3Mm84SXNhRldDY2dVbUt3eFpWVlNiYnVlMit6VTFydjNRallZcGxURGxiVkZZcSs2VEF6eVl4Zg==|133f19a28aa354f0bbe8be4ead9c89b1c02fb64065f5d2fbdc9fdc5d75b9bcfb',
            '__snaker__id': 'qEJ495KDpVBYSNZN',
            'gdxidpyhxdE': 'ZXg%5CbvU6uGEQRxSc0c%5CqOeRreTxyYpB%2Bw3Ek%5CKyXxtUNXtl81SmKD1WSTetX0rVcDYaaxa9M6RbUHSVHeJqXZtYNU806pguMNpPfjZh1%2FW%5Cdwdd6BWeGI0Zpe8I%5CoQY9aaJCNcXezI7vHJWpMBSSW490yja2%2B4Xc1oQkfUbsfca9SUK4%3A1751868140818',
            'captcha_ticket_v2': '2|1:0|10:1751867252|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfZ3RiSmVVRFhQWnM1RkRBMURfZEpBenNHbzVUVlQ5Q1ZNSzlwamJibXYyWW1MU3ZpdW9pamRGKkMyVkM5dkNuNjF6NUFKSGRDWlhpaV85YUQ1QWE2US5Ua1U5VXpLM1lXTngxc2VjNU9ac2RlWWRNNnhTZ2c0U3E1SmpQZTR2TkZMQ0RRa3BnOWRWbmhyXzRhUjIxRGhHQ3RzU2xXaEJkdV9fOFhFNlNQYzJrUkZTbFNXZXRzWTFYRXI4YjIqYWFieFd1TXptTkJNNjN2emZFZyppYyp1LkJvZU9yU25HVlZpZUhmbEVyOVllbXk1NEdYdWpNLkRXbW9XQnZHcU9hTEFYem02anM2TEJDcFpFU2c5NjZGVjR2SlJualFVX0dYX1VRejZJNkFwWmxlcXVVbGdPMjROWXFzczBvNk5QWkc0WFJySUE2a1hyVHRuaWk2eU5TTXZRc1VlNmpkcUltTG5QZFF3ZHlzZHpfWHBXWlF0NE1rQjVOZFRlQkFreTlOY3kqVWNWbTBmcmQyOFNHQVZUSHkqWEFta0JZRHIydkdQSVF6WE9ZM1lBTGhOcDNnYVE2cUJaazZvWmxKTktoY01tMXkuRk5ITHpQVl9CZUdNTDI0KkVIYUc5VVI2OTlobG51SU5zbFdDQU5JLmp5QWtaVW9GZWdHYzEwZHVDZGh0S2tOZVg3N192X2lfMSJ9|2b784e78068deac97ab3dac46d753a13680969f2f6ba85facd65a9c5b92d0c82',
            'z_c0': '2|1:0|10:1751867279|4:z_c0|92:Mi4xOU8wUUR3QUFBQUJPcHRQTjFPNjRHaVlBQUFCZ0FsVk5qNjFZYVFEUDYyNkt2a1pEeXl2Y1pJejNjTnNCelpnQmhR|c4c61a602f45dd3ba01ff5457d7bc77981530e1e433e52f73f8ee5fa3bf22aeb',
            'q_c1': '5192dfb0aa2c4452b92291dcfed08f61|1751937931000|1751937931000',
            'Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49': '1751248298,1751270888,1752456465',
            'HMACCOUNT': 'FDF943C033E3BF66',
            'tst': 'r',
            'SESSIONID': 'm8qphQqcbgmTQy1eKQfbdDs3cQpcQlreD3KOEevHn4G',
            'JOID': 'U1oTCkLFfBCLuQARJsxXBd2Bn7Q4q0Bu-9lSZEqvGHnQ6HEjR4xfaeuyBxop3IbOBkDaUksDLbI9bEBS2MX6VXU=',
            'osd': 'UV4cCkLHeB-LuQIVKcxXB9mOn7Q6r09u-9tWa0qvGn3f6HEhQ4Nfaem2CBop3oLBBkDYVkQDLbA5Y0BS2sH1VXU=',
            'Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49': '1752632206',
            'BEC': '6ff32b60f55255af78892ba1e551063a',
            '__zse_ck': '004_urxtCkAY84waiFLX9A21tFNvvjnfW5xb2b23pqWwTy2LCn3XfhaeZI6CsvdIuR3qyYQwXPyqRzp6I9ro//7vHg2HVqSWHd6l8PdGN5fYHrQG2oond/o9tETly8uQyhuD-ovsR2UB1Z5AG2u2dgimZtft3dlqYJ3OCD1p5rRmkERo8nEbkUzLoPOYGPFSpsk52RKi/07IjF+XWRFofZgOOy/d/wM9gtbVylbiYkhl9nP0ByylNZwW9cKR8R0zv5/mt',
        }

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'referer': 'https://www.zhihu.com/search?q=vllm&search_source=History&utm_content=search_history&type=content',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            # 'cookie': '_xsrf=fAV1ddETS08U6k2nVMd3p2vIf5QN1qDz; _zap=ec14958c-f067-49c9-9ecd-50a93d32b301; d_c0=TqbTzdTuuBqPTvrDVMxoYjkgVFxngXScfxM=|1751867237; captcha_session_v2=2|1:0|10:1751867238|18:captcha_session_v2|88:L2R1amYxR1Y3Mm84SXNhRldDY2dVbUt3eFpWVlNiYnVlMit6VTFydjNRallZcGxURGxiVkZZcSs2VEF6eVl4Zg==|133f19a28aa354f0bbe8be4ead9c89b1c02fb64065f5d2fbdc9fdc5d75b9bcfb; __snaker__id=qEJ495KDpVBYSNZN; gdxidpyhxdE=ZXg%5CbvU6uGEQRxSc0c%5CqOeRreTxyYpB%2Bw3Ek%5CKyXxtUNXtl81SmKD1WSTetX0rVcDYaaxa9M6RbUHSVHeJqXZtYNU806pguMNpPfjZh1%2FW%5Cdwdd6BWeGI0Zpe8I%5CoQY9aaJCNcXezI7vHJWpMBSSW490yja2%2B4Xc1oQkfUbsfca9SUK4%3A1751868140818; captcha_ticket_v2=2|1:0|10:1751867252|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfZ3RiSmVVRFhQWnM1RkRBMURfZEpBenNHbzVUVlQ5Q1ZNSzlwamJibXYyWW1MU3ZpdW9pamRGKkMyVkM5dkNuNjF6NUFKSGRDWlhpaV85YUQ1QWE2US5Ua1U5VXpLM1lXTngxc2VjNU9ac2RlWWRNNnhTZ2c0U3E1SmpQZTR2TkZMQ0RRa3BnOWRWbmhyXzRhUjIxRGhHQ3RzU2xXaEJkdV9fOFhFNlNQYzJrUkZTbFNXZXRzWTFYRXI4YjIqYWFieFd1TXptTkJNNjN2emZFZyppYyp1LkJvZU9yU25HVlZpZUhmbEVyOVllbXk1NEdYdWpNLkRXbW9XQnZHcU9hTEFYem02anM2TEJDcFpFU2c5NjZGVjR2SlJualFVX0dYX1VRejZJNkFwWmxlcXVVbGdPMjROWXFzczBvNk5QWkc0WFJySUE2a1hyVHRuaWk2eU5TTXZRc1VlNmpkcUltTG5QZFF3ZHlzZHpfWHBXWlF0NE1rQjVOZFRlQkFreTlOY3kqVWNWbTBmcmQyOFNHQVZUSHkqWEFta0JZRHIydkdQSVF6WE9ZM1lBTGhOcDNnYVE2cUJaazZvWmxKTktoY01tMXkuRk5ITHpQVl9CZUdNTDI0KkVIYUc5VVI2OTlobG51SU5zbFdDQU5JLmp5QWtaVW9GZWdHYzEwZHVDZGh0S2tOZVg3N192X2lfMSJ9|2b784e78068deac97ab3dac46d753a13680969f2f6ba85facd65a9c5b92d0c82; z_c0=2|1:0|10:1751867279|4:z_c0|92:Mi4xOU8wUUR3QUFBQUJPcHRQTjFPNjRHaVlBQUFCZ0FsVk5qNjFZYVFEUDYyNkt2a1pEeXl2Y1pJejNjTnNCelpnQmhR|c4c61a602f45dd3ba01ff5457d7bc77981530e1e433e52f73f8ee5fa3bf22aeb; q_c1=5192dfb0aa2c4452b92291dcfed08f61|1751937931000|1751937931000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1751248298,1751270888,1752456465; HMACCOUNT=FDF943C033E3BF66; tst=r; SESSIONID=m8qphQqcbgmTQy1eKQfbdDs3cQpcQlreD3KOEevHn4G; JOID=U1oTCkLFfBCLuQARJsxXBd2Bn7Q4q0Bu-9lSZEqvGHnQ6HEjR4xfaeuyBxop3IbOBkDaUksDLbI9bEBS2MX6VXU=; osd=UV4cCkLHeB-LuQIVKcxXB9mOn7Q6r09u-9tWa0qvGn3f6HEhQ4Nfaem2CBop3oLBBkDYVkQDLbA5Y0BS2sH1VXU=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1752632206; BEC=6ff32b60f55255af78892ba1e551063a; __zse_ck=004_urxtCkAY84waiFLX9A21tFNvvjnfW5xb2b23pqWwTy2LCn3XfhaeZI6CsvdIuR3qyYQwXPyqRzp6I9ro//7vHg2HVqSWHd6l8PdGN5fYHrQG2oond/o9tETly8uQyhuD-ovsR2UB1Z5AG2u2dgimZtft3dlqYJ3OCD1p5rRmkERo8nEbkUzLoPOYGPFSpsk52RKi/07IjF+XWRFofZgOOy/d/wM9gtbVylbiYkhl9nP0ByylNZwW9cKR8R0zv5/mt',
        }

        url = "https://www.zhihu.com/api/v4/search_v3?gk_version=gz-gaokao&t=general&q=vllm&correction=1&offset=0&limit=20&filter_fields=&lc_idx=0&show_all_topics=0&search_source=History"
        # url = "https://www.zhihu.com/search?q=vllm&search_source=History&utm_content=search_history&type=content"
        yield scrapy.Request(url=url, headers=headers, cookies=cookies, callback=self.parse)

    def parse(self, response):
        print(f" ==========>> {response}")
        import pdb; pdb.set_trace()
        titles = response.xpath('//*[@id="SearchMain"]/div/div/div/div[*]/div/div/div/h2/span/div/div/div/a/span')

