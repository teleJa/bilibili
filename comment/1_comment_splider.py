import requests
import json

class BLDSplider:
    def __init__(self, aid):
        self.origin_url = "https://www.bilibili.com/video/av{}?from=search&seid=9346373599622336536".format(aid)
        self.url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=1&oid={}&sort=0&_=1562680632561".format(aid)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Referer": self.origin_url
        }

    def parse_url(self):
        response = requests.get(self.url,headers=self.headers)
        json.loads(response.content.decode())


    def get_cid(self):
        pass

    def run(self):
        self.parse_url()

def main():
    splider = BLDSplider(55036734)
    splider.run()

if __name__ == '__main__':
    main()


