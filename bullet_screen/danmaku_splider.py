import requests
import re
import os
from lxml import  etree
# 弹幕
class BLDSplider:
    regex_cid = re.compile("\"cid\":(.{8})")
    def __init__(self, aid):
        self.aid = aid
        self.origin_url = "https://www.bilibili.com/video/av{}?from=search&seid=9346373599622336536".format(aid)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        }
        self.danmaku_url = "https://comment.bilibili.com/{}.xml"
        # 检查目录
        self.parent_path = "e:/bilibili/" + str(self.aid) + "/"
        if not os.path.exists(self.parent_path):
            os.makedirs(self.parent_path)
        self.danmaku_name = self.parent_path + str(self.aid) + ".txt"

    def parse_url(self, cid):
        response = requests.get(self.danmaku_url.format(cid),headers=self.headers)
        if response.status_code == 200:
            danmaku_xml = etree.HTML(response.content)
            d_list = danmaku_xml.xpath("//d")
            with open(self.danmaku_name,"w",encoding="utf-8") as file:
                for d in d_list:
                    file.write(d.xpath("./text()")[0])
                    file.write("\n")



    def get_cid(self):
        response = requests.get(self.origin_url, headers=self.headers)
        if response.status_code == 200:
            cid = BLDSplider.regex_cid.findall(response.content.decode())[0]
            return cid

    def run(self):
        cid = self.get_cid()
        self.parse_url(cid)

def main():
    splider = BLDSplider(55036734)
    splider.run()


if __name__ == '__main__':
    main()


