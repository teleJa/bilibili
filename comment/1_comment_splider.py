import requests
import json
import math
import os

class BLDSplider:
    def __init__(self, aid):
        self.aid = aid
        self.origin_url = "https://www.bilibili.com/video/av{}?from=search&seid=9346373599622336536".format(aid)
        self.url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={}&type=1&oid={}&sort=0&_=1562680632561"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Referer": self.origin_url
        }

        # 检查目录
        self.parent_path = "e:/bilibili/" + str(self.aid) + "/comment/"
        if not os.path.exists(self.parent_path):
            os.makedirs(self.parent_path)

    def parse_url(self,total_pages):
        for i in range(1, total_pages+1):
            response = requests.get(self.url.format(i, str(self.aid)), headers=self.headers)
            if response.status_code == 200:
                data = json.loads(response.content.decode())["data"]
                comment_list = data["replies"]
                with open(self.parent_path + "第{}页".format(str(i)) + ".txt","w",encoding="utf-8") as file:
                    for c in comment_list:
                        file.write(c["content"]["message"])
                        file.write("\n")

    def get_pages(self):
        response = requests.get(self.url.format(1, self.aid), headers=self.headers)
        if response.status_code == 200:
            data = json.loads(response.content.decode())["data"]
            count = data["page"]["count"]
            size = data["page"]["size"]
            total_pages = math.ceil(count / size)
            return total_pages

    def run(self):
        self.parse_url(self.get_pages())


def main():
    splider = BLDSplider(53545832)
    splider.run()


if __name__ == '__main__':
    main()


