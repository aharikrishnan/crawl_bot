# -*- coding: utf-8 -*-
import json
import scrapy
from crawl_bot.items import SearsItem


class SearsItemSpider(scrapy.Spider):
    name = "sears_item"
    # start_urls = ["http://sears.com"]
    allowed_domains = ["sears.com"]
    handle_httpstatus_list = [404]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawl_bot.middlewares.IgnoreCrawledMiddleware': 543,
        },
        'ITEM_PIPELINES': {
            'crawl_bot.pipelines.MongoPipeline': 300,
        },
	'MONGO_DATABASE' : "sears",
        'MONGO_COLLECTION': 'items_crawl'
    }
    def __init__(self, in_file=None, *args, **kwargs):
        super(SearsItemSpider, self).__init__(*args, **kwargs)
        self.item_ids = None
        if in_file is not None:
            with open(in_file) as fo:
                self.item_ids = fo.read().split("\n")

    def cookie_id(self):
        return 1

    def start_requests(self):
        headers = {
            'Accept-Encoding':
            'gzip, deflate, sdch',
            'Accept-Language':
            'en-US,en;q=0.8',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
            'Accept':
            'application/json, text/plain, */*',
            'Referer':
            'http://www.sears.com/appliances-microwaves-over-the-range-microwaves/b-1020309?pageNum=2',
            'Connection':
            'keep-alive',
            'Cookie':
            'ra_id=xxx1476873860807%7CG%7C0; btpdb.PCNPFl9.c3NvIGlkIChjb29raWVkKQ=MTM2OTYxNjY2NjEyMzUwMDg2XzMwNzcwXzMxMzE4; OAX=ylMSs1gHTocAC9IL; __gads=ID=50f2e9636e69a48f:T=1476873864:S=ALNI_MZx3PwL-xUvs-AzImd-3kBtxCc5gg; sn.vi=vi||8707bf8a-e399-4245-9e7e-3df3bcfbf675; expo_us_llt=05feabd9-d151-477e-ac59-9af4b26f9dec; irp=5213c527-1696-4c1f-9d86-8f95b7edf1ea|5nqOuONm5fqjsvF2eRxPVFBcP7uPcXuhB6EfXkUesBE%3D|G|136961666612350086_30770_31318|0|1876596202; ot=i2-prod-ch3-vX-; Yottaacookie=1; KI_FLAG=false; s_sso=s_r%7CY%7C; ResonanceSegment=1; IntnlShip=US%7CUSD%7C1%7C12425778%7C%7C%7CN; IntlCntGrp=; cust_info=%7B%22customerinfo%22%3A%7B%22userName%22%3A%22%22%2C%22isAkamaiZipSniff%22%3Afalse%2C%22isGuest%22%3Atrue%2C%22isSYWR%22%3Afalse%2C%22sywrNo%22%3A%22%22%2C%22encryptedSywrNo%22%3A%22%22%2C%22sywrPoints%22%3A0%2C%22sywrAmount%22%3A0%2C%22expiringPoints%22%3A0%2C%22expiringPointsDate%22%3Anull%2C%22expiringPointsWarn%22%3Afalse%2C%22spendingYear%22%3A0%2C%22vipLevel%22%3A%22%22%2C%22nextLevel%22%3A0%2C%22maxStatus%22%3A%22SVU%22%2C%22maxSavings%22%3A0%2C%22sessionID%22%3A%225213c527-1696-4c1f-9d86-8f95b7edf1ea%22%2C%22globalID%22%3A%22136961666612350086_30770_31318%22%2C%22memberID%22%3A%22136961666612350086_30770_31318%22%2C%22associate%22%3Afalse%2C%22pgtToken%22%3A%22%22%2C%22displayName%22%3A%22%22%2C%22partialLogin%22%3Afalse%2C%22cartCount%22%3A8%7D%7D; _gat_tealium_0=1; mbox=PC%2309958532f30244b6865ff15d16aa5601.22_6%231540194915%7Csession%2332a6f51da51946079314420c5edb693d%231476951976; RES_TRACKINGID=375805419181096; RES_SESSIONID=614384310934796; BTT_X0siD=4769457815293224518; __CG=u%3A5732322810063839000%2Cs%3A90748869%2Ct%3A1476950116274%2Cc%3A7%2Ck%3Awww.sears.com/82/92/2234%2Cf%3A0%2Ci%3A1; s_pers=%20s_vnum%3D1634553861208%2526vn%253D2%7C1634553861208%3B%20s_fid%3D7D39DA6F4EC2CBA5-31CE4E1CB7813D8E%7C1634716517556%3B%20s_invisit%3Dtrue%7C1476951917562%3B%20s_depth%3D7%7C1476951917565%3B%20gpv_pn%3DProduct%2520Summary%7C1476951917570%3B%20gev_lst%3DprodView%252Cevent10%252Cevent45%253D1%252Cevent77%7C1476951917572%3B%20gpv_sc%3DLawn%2520%2526%2520Garden%7C1476951917577%3B%20gpv_pt%3DProduct%2520Summary%2520%253E%2520CFG01%7C1476951917579%3B; s_sess=%20s_sq%3D%3B%20s_e30%3DAnonymous%3B%20s_e26%3DMP%2520%2526%2520SHC%2520PIDs%2520seen%3B%20s_cc%3Dtrue%3B; s_vi=[CS]v1|2C03A742852A1887-4000010700034566[CE]; aam_tnt=seg%3D104605~1932117~2938850~3610337; aam_chango=crt%3Dsears%2Ccrt%3Dsearsabandoncart%2Ccrt%3Dclothingenthusiast; aamsears=aam%3D3; aam_criteo=crt%3Dsears; sears_offers=offers%3D1; aam_profile_seg=seg%3D104605; aam_uuid=81201937849952017684083103320705558661; phfsid=default; _br_uid_2=uid%3D5724284217291%3Av%3D11.8%3Ats%3D1476873875585%3Ahc%3D12; _ga=GA1.2.1024801762.1476873867; utag_main=v_id:0157dc8ab71800519b0ae2e7d1700506800370600086e$_sn:2$_ss:0$_st:1476951917927$dc_visit:2$_pn:7%3Bexp-session$ses_id:1476945786986%3Bexp-session$dc_event:8%3Bexp-session$dc_region:eu-central-1%3Bexp-session; BTT_WCD_Collect=on; fsr.s=%7B%22v2%22%3A-2%2C%22v1%22%3A1%2C%22rid%22%3A%22d1159f3-80458147-b321-eba0-b9cbd%22%2C%22r%22%3A%22www.sears.com%22%2C%22st%22%3A%22%22%2C%22c%22%3A%22http%3A%2F%2Fwww.sears.com%2Flevi-s-men-s-501-original-straight-leg-jeans%2Fp-SPM12105154016%22%2C%22pv%22%3A5%2C%22lc%22%3A%7B%22d1%22%3A%7B%22v%22%3A5%2C%22s%22%3Atrue%7D%7D%2C%22cd%22%3A1%2C%22cp%22%3A%7B%22usrSessionID%22%3A%225213c527-1696-4c1f-9d86-8f95b7edf1ea%7C5nqOuONm5fqjsvF2eRxPVFBcP7uPcXuhB6EfXkUesBE%3D%7CG%7C136961666612350086_30770_31318%7C0%7C1876596202%22%2C%22shcMPSHC%22%3A%22MP%20%26%20SHC%20PIDs%20seen%22%7D%2C%22sd%22%3A1%7D; bounceClientVisit1400=N4IgbiBcoMYEYEMBOB9AzgFwKYAcoDMEAbNLAGhDRRyQHscAmB9DWpBAcyyhBAqpr0GAZhZtO3SLwC+-AJYATKAA4K+MBigBGACwB2AGzK9OkavCLt+gwE4dAVj3Kbe+zYOuKCWlAAMXtD8KMBwISD0KJSklCiI8KQALDAwcAFJhAEFUhgAxbJyAdyKAOlJkNGKYWgBbfKIsMDkAWjQm6qwAOxam+18tJrY5DjkO4haMdiGkpvqOJoArLAQOtHycJt8dLQA1DI9lXxctBgAFdJykJCwYdIARCYBXbgokHj4QGA0rQztHZwoODBXpAjBRqkEQApLFIDG4bI4tPCGLC9DYtMIGDobO8iF9ILofr0tFplNIgA; __CT_Data=gpv=14&apv_99_www04=12; WRUID20151512=0; ak_bmsc=1F56CCC01C3192D244E3882CED0CF68B170346177B300000726708585E50147B~pl8DZyGrAfsL0zOHmYLKaPGkowREr8b5O6q7WDgORv6GBLMnf9JP+YyFmZtOwifHJhL7DjsfDqziDOeuA6eQLKllr03q/Kby6txMFvs3/RMnmoYPFqPx72dU6yPGkVdSLGc9WxYfUVWkCC4wRF0evlgmuZ2vMl4cIzvDRn7yvnRJALKmnx5oDmiijroEQU944ZuN0ry7MhYdkHDpGXGkTMRA=='
        }

        cookies = {
            'ra_id':
            'xxx1476873860807%7CG%7C0',
            'btpdb.PCNPFl9.c3NvIGlkIChjb29raWVkKQ':
            'MTM2OTYxNjY2NjEyMzUwMDg2XzMwNzcwXzMxMzE4',
            'OAX':
            'ylMSs1gHTocAC9IL',
            '__gads':
            'ID=50f2e9636e69a48f:T=1476873864:S=ALNI_MZx3PwL-xUvs-AzImd-3kBtxCc5gg',
            'sn.vi':
            'vi||8707bf8a-e399-4245-9e7e-3df3bcfbf675',
            'expo_us_llt':
            '05feabd9-d151-477e-ac59-9af4b26f9dec',
            'irp':
            '5213c527-1696-4c1f-9d86-8f95b7edf1ea|5nqOuONm5fqjsvF2eRxPVFBcP7uPcXuhB6EfXkUesBE%3D|G|136961666612350086_30770_31318|0|1876596202',
            'ot':
            'i2-prod-ch3-vX-',
            'Yottaacookie':
            '1',
            'KI_FLAG':
            'false',
            's_sso':
            's_r%7CY%7C',
            'ResonanceSegment':
            '1',
            'IntnlShip':
            'US%7CUSD%7C1%7C12425778%7C%7C%7CN',
            'IntlCntGrp':
            '',
            'cust_info':
            '%7B%22customerinfo%22%3A%7B%22userName%22%3A%22%22%2C%22isAkamaiZipSniff%22%3Afalse%2C%22isGuest%22%3Atrue%2C%22isSYWR%22%3Afalse%2C%22sywrNo%22%3A%22%22%2C%22encryptedSywrNo%22%3A%22%22%2C%22sywrPoints%22%3A0%2C%22sywrAmount%22%3A0%2C%22expiringPoints%22%3A0%2C%22expiringPointsDate%22%3Anull%2C%22expiringPointsWarn%22%3Afalse%2C%22spendingYear%22%3A0%2C%22vipLevel%22%3A%22%22%2C%22nextLevel%22%3A0%2C%22maxStatus%22%3A%22SVU%22%2C%22maxSavings%22%3A0%2C%22sessionID%22%3A%225213c527-1696-4c1f-9d86-8f95b7edf1ea%22%2C%22globalID%22%3A%22136961666612350086_30770_31318%22%2C%22memberID%22%3A%22136961666612350086_30770_31318%22%2C%22associate%22%3Afalse%2C%22pgtToken%22%3A%22%22%2C%22displayName%22%3A%22%22%2C%22partialLogin%22%3Afalse%2C%22cartCount%22%3A8%7D%7D',
            '_gat_tealium_0':
            '1',
            'mbox':
            'PC%2309958532f30244b6865ff15d16aa5601.22_6%231540194915%7Csession%2332a6f51da51946079314420c5edb693d%231476951976',
            'RES_TRACKINGID':
            '375805419181096',
            'RES_SESSIONID':
            '614384310934796',
            'BTT_X0siD':
            '4769457815293224518',
            '__CG':
            'u%3A5732322810063839000%2Cs%3A90748869%2Ct%3A1476950116274%2Cc%3A7%2Ck%3Awww.sears.com/82/92/2234%2Cf%3A0%2Ci%3A1',
            's_pers':
            '%20s_vnum%3D1634553861208%2526vn%253D2%7C1634553861208%3B%20s_fid%3D7D39DA6F4EC2CBA5-31CE4E1CB7813D8E%7C1634716517556%3B%20s_invisit%3Dtrue%7C1476951917562%3B%20s_depth%3D7%7C1476951917565%3B%20gpv_pn%3DProduct%2520Summary%7C1476951917570%3B%20gev_lst%3DprodView%252Cevent10%252Cevent45%253D1%252Cevent77%7C1476951917572%3B%20gpv_sc%3DLawn%2520%2526%2520Garden%7C1476951917577%3B%20gpv_pt%3DProduct%2520Summary%2520%253E%2520CFG01%7C1476951917579%3B',
            's_sess':
            '%20s_sq%3D%3B%20s_e30%3DAnonymous%3B%20s_e26%3DMP%2520%2526%2520SHC%2520PIDs%2520seen%3B%20s_cc%3Dtrue%3B',
            's_vi':
            '[CS]v1|2C03A742852A1887-4000010700034566[CE]',
            'aam_tnt':
            'seg%3D104605~1932117~2938850~3610337',
            'aam_chango':
            'crt%3Dsears%2Ccrt%3Dsearsabandoncart%2Ccrt%3Dclothingenthusiast',
            'aamsears':
            'aam%3D3',
            'aam_criteo':
            'crt%3Dsears',
            'sears_offers':
            'offers%3D1',
            'aam_profile_seg':
            'seg%3D104605',
            'aam_uuid':
            '81201937849952017684083103320705558661',
            'phfsid':
            'default',
            '_br_uid_2':
            'uid%3D5724284217291%3Av%3D11.8%3Ats%3D1476873875585%3Ahc%3D12',
            '_ga':
            'GA1.2.1024801762.1476873867',
            'utag_main':
            'v_id:0157dc8ab71800519b0ae2e7d1700506800370600086e$_sn:2$_ss:0$_st:1476951917927$dc_visit:2$_pn:7%3Bexp-session$ses_id:1476945786986%3Bexp-session$dc_event:8%3Bexp-session$dc_region:eu-central-1%3Bexp-session',
            'BTT_WCD_Collect':
            'on',
            'fsr.s':
            '%7B%22v2%22%3A-2%2C%22v1%22%3A1%2C%22rid%22%3A%22d1159f3-80458147-b321-eba0-b9cbd%22%2C%22r%22%3A%22www.sears.com%22%2C%22st%22%3A%22%22%2C%22c%22%3A%22http%3A%2F%2Fwww.sears.com%2Flevi-s-men-s-501-original-straight-leg-jeans%2Fp-SPM12105154016%22%2C%22pv%22%3A5%2C%22lc%22%3A%7B%22d1%22%3A%7B%22v%22%3A5%2C%22s%22%3Atrue%7D%7D%2C%22cd%22%3A1%2C%22cp%22%3A%7B%22usrSessionID%22%3A%225213c527-1696-4c1f-9d86-8f95b7edf1ea%7C5nqOuONm5fqjsvF2eRxPVFBcP7uPcXuhB6EfXkUesBE%3D%7CG%7C136961666612350086_30770_31318%7C0%7C1876596202%22%2C%22shcMPSHC%22%3A%22MP%20%26%20SHC%20PIDs%20seen%22%7D%2C%22sd%22%3A1%7D',
            'bounceClientVisit1400':
            'N4IgbiBcoMYEYEMBOB9AzgFwKYAcoDMEAbNLAGhDRRyQHscAmB9DWpBAcyyhBAqpr0GAZhZtO3SLwC+-AJYATKAA4K+MBigBGACwB2AGzK9OkavCLt+gwE4dAVj3Kbe+zYOuKCWlAAMXtD8KMBwISD0KJSklCiI8KQALDAwcAFJhAEFUhgAxbJyAdyKAOlJkNGKYWgBbfKIsMDkAWjQm6qwAOxam+18tJrY5DjkO4haMdiGkpvqOJoArLAQOtHycJt8dLQA1DI9lXxctBgAFdJykJCwYdIARCYBXbgokHj4QGA0rQztHZwoODBXpAjBRqkEQApLFIDG4bI4tPCGLC9DYtMIGDobO8iF9ILofr0tFplNIgA',
            '__CT_Data':
            'gpv=14&apv_99_www04=12',
            'WRUID20151512':
            '0',
            'ak_bmsc':
            '1F56CCC01C3192D244E3882CED0CF68B170346177B300000726708585E50147B~pl8DZyGrAfsL0zOHmYLKaPGkowREr8b5O6q7WDgORv6GBLMnf9JP+YyFmZtOwifHJhL7DjsfDqziDOeuA6eQLKllr03q/Kby6txMFvs3/RMnmoYPFqPx72dU6yPGkVdSLGc9WxYfUVWkCC4wRF0evlgmuZ2vMl4cIzvDRn7yvnRJALKmnx5oDmiijroEQU944ZuN0ry7MhYdkHDpGXGkTMRA=='
        }

        if self.item_ids is not None:
            for sin in self.item_ids:
                url = "http://www.sears.com/content/pdp/config/products/v1/products/{0}?site=sears".format(sin)
                uid = "{0}-{1}-{2}".format('s', 'p', sin)
                print(url)
                print(uid)
                request = scrapy.Request(url, headers=headers, cookies=cookies, callback=self.parse)
                # request.meta['cookiejar'] = self.cookie_id
                request.meta['uid'] = uid
                yield request



    def parse(self, response):
        if 'skip' not in response.meta:
            print(response.body)
            try:
                json_payload = json.loads(response.body)
                item = SearsItem()
                item['uid'] = response.meta['uid']
                item['data'] = json_payload
                yield item
            except:
                pass
