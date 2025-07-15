import scrapy 

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"

    async def start(self):
        cookies = {
            '_zap': 'bf2cd6b9-717e-4376-8674-4d1191613b2a',
            'd_c0': '7ITT1dL6kxqPTrDQZT6efl1SPFiv_3t-C_Q=|1749387353',
            '__snaker__id': 'UOoYjOJlIXziLn3h',
            'q_c1': '2a27925b53a3464f88905321f54c4ead|1749387382000|1749387382000',
            '_xsrf': '131daf63-fc13-467b-a94a-2031b1d48ccb',
            'BEC': '6bca8f185b99e85d761c7a0d8d692864',
            'Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49': '1751112374,1752582001',
            'HMACCOUNT': '0B38B7CA2C334C8F',
            'tst': 'r',
            'z_c0': '2|1:0|10:1752582003|4:z_c0|80:MS4xOU8wUUR3QUFBQUFtQUFBQVlBSlZUWE9WWTJtTndROXlmeVhkUGM1eWNsU3NQcEk1WXZJMEpRPT0=|3e04086fdefacc4ca9e9a81252ba66e9eb33102cc9fc63cc5b052e99ca61fd4b',
            'SESSIONID': 'LogbQnNmyLrwIGrqaLWbGfCkwGsvscbdnlqQCmCf3A5',
            'JOID': 'UlwQAknk_uKbfyToefHqM5Sr331mrJCB-ixOpxCftpHoNWGeCZK8k_J5Ie1-T7CyrxPnf87cIsKFCCb2XKdeOx0=',
            'osd': 'VV8UB07j_eaeeCPrffTtNJev2nphr5SE_StNoxWYsZLsMGaZCpa5lPV6Jeh5SLO2qhTgfMrZJcWGDCPxW6RaPho=',
            '__zse_ck': '004_ifi7xuIOuOM24k0ZTzo=G9EPevQO3wW8LQPBFUqAEZGM76esx7ghbI/UdgxMDfT/tVY8ZrLdapPfVYyNGDjs9=KewBPJ675cU96mpsTLX=GJIoP550kmFnM=81V7jewR-ibEcM1jw+lwCjGmGoxsLizJ2gVdSnv/2RJEAQZ+1ReaCZwEWd+QYCwaJYhHw+NYk6ilgfP9ZGS8guyNm7ysCIdoDyGb+x4AkridpX5nVutt0TsMbc4eEFknxjSIqOo56',
            'Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49': '1752582487',
        }

        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'priority': 'u=1, i',
            'referer': 'https://www.zhihu.com/search?q=a%E8%82%A1&search_source=Suggestion&type=content&utm_content=search_suggestion&time_interval=a_week',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'x-api-version': '3.0.91',
            'x-app-za': 'OS=Web',
            'x-requested-with': 'fetch',
            'x-zse-93': '101_3_3.0',
            'x-zse-96': '2.0_SheS=jxLLD1cp0utFl5rBJif4FnGRI=FWC9z44Tca63JikLwjmJgUd=zs+cveaxi',
            'x-zst-81': '3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZf0Y0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIoLVqr4gxrRPOI0cY7HL8qun9g93mFukyigcmebS_FwOYPRP0E4rZUrN9DDom3hnynAUMnAVPF_PhaueTF8S_1qHKBBVm3B309veqVB2MZhCqxDgY20om6XHm2DXLYTo9c4cfUJN9b8cTV4x1_JHLSMgL_qX9JGc8Iu3MqBOYLUOM84XYYvu1gDXpOuwmsXxMtuV8pcLO0DcM2GwK-9xGYvcmYCFMPu3mkQCBIbHVLBNB8uc_gvL8gvw_oRF_5UFCOg_zohLBNBCMkqtOYgxftU28Nvc80rxYPUgKZhNssC2YFGF_SweVzCY1FqLmHupLIbCBzUNOqCYKp0e9QUc16ULxrwNO3hpY_vLMngxYBveYccN1CJNLe8es',
            # 'cookie': '_zap=bf2cd6b9-717e-4376-8674-4d1191613b2a; d_c0=7ITT1dL6kxqPTrDQZT6efl1SPFiv_3t-C_Q=|1749387353; __snaker__id=UOoYjOJlIXziLn3h; q_c1=2a27925b53a3464f88905321f54c4ead|1749387382000|1749387382000; _xsrf=131daf63-fc13-467b-a94a-2031b1d48ccb; BEC=6bca8f185b99e85d761c7a0d8d692864; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1751112374,1752582001; HMACCOUNT=0B38B7CA2C334C8F; tst=r; z_c0=2|1:0|10:1752582003|4:z_c0|80:MS4xOU8wUUR3QUFBQUFtQUFBQVlBSlZUWE9WWTJtTndROXlmeVhkUGM1eWNsU3NQcEk1WXZJMEpRPT0=|3e04086fdefacc4ca9e9a81252ba66e9eb33102cc9fc63cc5b052e99ca61fd4b; SESSIONID=LogbQnNmyLrwIGrqaLWbGfCkwGsvscbdnlqQCmCf3A5; JOID=UlwQAknk_uKbfyToefHqM5Sr331mrJCB-ixOpxCftpHoNWGeCZK8k_J5Ie1-T7CyrxPnf87cIsKFCCb2XKdeOx0=; osd=VV8UB07j_eaeeCPrffTtNJev2nphr5SE_StNoxWYsZLsMGaZCpa5lPV6Jeh5SLO2qhTgfMrZJcWGDCPxW6RaPho=; __zse_ck=004_ifi7xuIOuOM24k0ZTzo=G9EPevQO3wW8LQPBFUqAEZGM76esx7ghbI/UdgxMDfT/tVY8ZrLdapPfVYyNGDjs9=KewBPJ675cU96mpsTLX=GJIoP550kmFnM=81V7jewR-ibEcM1jw+lwCjGmGoxsLizJ2gVdSnv/2RJEAQZ+1ReaCZwEWd+QYCwaJYhHw+NYk6ilgfP9ZGS8guyNm7ysCIdoDyGb+x4AkridpX5nVutt0TsMbc4eEFknxjSIqOo56; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1752582487',
        }

        params = {
            'gk_version': 'gz-gaokao',
            't': 'general',
            'q': 'a股',
            'correction': '1',
            'offset': '0',
            'limit': '20',
            'filter_fields': '',
            'lc_idx': '0',
            'show_all_topics': '0',
            'search_source': 'Filter',
            'time_interval': 'a_week',
        }
