import  requests
import re
import json
import os
from lxml import etree

# 下载某up的代表作
class BLDSpaceSplider:
    def __init__(self, keyword):
        self.kw = keyword
        self.url = "https://search.bilibili.com/all?keyword={}&from_source=nav_search".format(self.kw)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        }


    def get_up_mid(self):
        print(self.url)
        response = requests.get(self.url,headers=self.headers)
        if response.status_code == 200:
            html_element = etree.HTML(response.content)
            space_url = "https:" + html_element.xpath("//div[@class='up-face']/a/@href")[0]
            print("space_url:%s" % space_url)
            fields = space_url.split("/")
            return fields[len(fields)-1].split("?")[0]

    # 获得代表作的视频番号
    def get_video_aid_list(self,mid):
        video_url = "https://api.bilibili.com/x/space/masterpiece?vmid={}&jsonp=jsonp".format(mid)
        response = requests.get(video_url,headers=self.headers)
        if response.status_code == 200:
            data = json.loads(response.content.decode())["data"]
            number_list = list()
            for d in data:
                number_list.append(d["aid"])
            return number_list

    def run(self):
        aid_list = self.get_video_aid_list(self.get_up_mid())
        print(aid_list)
        for aid in aid_list:
            os.system( "python E:/pythonworkspace/bilibili/video/1_bld_splider.py %s" % aid)


def main():
    splider = BLDSpaceSplider("SPlusTech")
    splider.run()


if __name__ == '__main__':
    main()



