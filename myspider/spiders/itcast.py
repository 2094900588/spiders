import scrapy,json
from myspider.items import MyspiderItem

class ItcastSpider(scrapy.Spider):
    name = "itcast"
    allowed_domains = ["zfcg.gxzf.gov.cn"]
    start_urls = ["http://zfcg.gxzf.gov.cn/"]
    base_url = "http://zfcg.gxzf.gov.cn"
    spider_name = "采购意向公开" #要爬取的板块内容

    def parse(self, response):
        script=response.xpath("//script/text()").extract_first().split(";")[0]
        d = json.loads(script[script.find("=")+1:])

        models = d["preview"][6]["models"] #将对应的数据分析出来
        paramsDistrictCode = models["paramsDistrictCode"]
        # print(paramsDistrictCode)

        params = {
            "districtCode": paramsDistrictCode,
            "pageSize": 8,
            "needTotal": True,
            "needValidCount": True,
            "needNewCnt": True,
        }
        for i in models["noticeTabList"]:
            if i["tabName"] == self.spider_name:
                params["code"]=i["tabCategoryCode"]
                params["subCodes"]=i["tabSubsetCodes"].split(",")
                break
        else:
            return None
        yield scrapy.Request(
            self.base_url + models["articleListInterface"],
            method="POST",
            body=json.dumps(params),
            headers={'Content-Type':'application/json'},
            callback=self.parse_json)


    def parse_json(self,response):
        # items = []
        for i in response.json()["result"]["data"]["children"]:
            item = MyspiderItem()
            item["title"] = i["title"]
            item["articleId"] = i["articleId"]
            item["pubDate"] = i["pubDate"]
            item["districtName"] = i["districtName"]
            yield item
            # items.append(item)

        # return items