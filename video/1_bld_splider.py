import requests
import re
import os
import json
import sys
from lxml import etree


class BLDSplider:
    regex_cid = re.compile("\"cid\":(.{8})")

    def __init__(self, aid):
        self.aid = aid

        self.origin_url = "https://www.bilibili.com/video/av{}?from=search&seid=9346373599622336536".format(aid)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        }

        self.url = "https://api.bilibili.com/x/player/playurl?avid={}&cid={}&qn=0&type=&otype=json"

        # 检查目录
        self.parent_path = "e:/bilibili/" + str(self.aid) + "/"
        if not os.path.exists(self.parent_path):
            os.makedirs(self.parent_path)

        self.video_name = self.parent_path + str(self.aid) + ".mp4"

    def parse_url(self, item):
        cid = item["cid"]
        print("cid:%s" % cid)
        title = item["title"]
        print("title:%s" % title)

        self.headers["Referer"] = self.origin_url
        # 视频
        response = requests.get(self.url.format(self.aid, cid), headers=self.headers)
        if response.status_code == 200:
            result = json.loads(response.content.decode())
            durl = result["data"]["durl"][0]
            video_url = durl["url"]
            print(video_url)
            # 视频大小
            size = durl["size"]
            print("size:%s" % size )
            video_response = requests.get(video_url, headers=self.headers,stream=True)
            if video_response.status_code == 200:
                with open(self.video_name, "wb") as file:
                    buffer = 1024
                    count = 0
                    while True:
                        if count + buffer <= size:
                            file.write(video_response.raw.read(buffer))
                            count += buffer
                        else:
                            file.write(video_response.raw.read(size % buffer))
                            count += size % buffer
                        file_size = os.path.getsize(self.video_name)
                        # print("\r下载进度 %.2f %%" % (count * 100 / size), end="")

                        width=50
                        percent = (count / size)
                        use_num = int(percent * width)
                        space_num = int(width - use_num)
                        percent = percent * 100
                        print('\r进度:[%s%s]%d%%' % (use_num * '#', space_num * ' ', percent), file=sys.stdout, flush=True,end="")
                        if size == count:
                            break


    # 获取视频相关参数
    def get_video_info(self):
        response = requests.get(self.origin_url, headers=self.headers)
        item = dict()
        if response.status_code == 200:
            # author
            html_element = etree.HTML(response.content.decode())
            author = dict()
            author_name = html_element.xpath("/html/body/div[@id='app']/div[@class='v-wrap']/div[@class='r-con']/div[@id='v_upinfo']//a[@report-id='name']/text()")[0]
            # 通常是微博,微信公众号等联系方式
            author_others = html_element.xpath("/html/body/div[@id='app']/div[@class='v-wrap']/div[@class='r-con']/div[@id='v_upinfo']//div[@class='desc']/@title")[0]
            author["name"] = author_name
            author["others"] = author_others
            item["author"] = author

            # cid
            cid = BLDSplider.regex_cid.findall(response.content.decode())[0]
            item["cid"] = cid
            info_url = "https://api.bilibili.com/x/web-interface/view?aid={}&cid={}".format(self.aid, cid)
            info_response = requests.get(info_url, headers=self.headers)
            if info_response.status_code == 200:
                data = json.loads(info_response.content.decode())["data"]
                # 视频简介
                desc = data["desc"]
                item["desc"] = desc

                # title
                title = data["title"]
                item["title"] = title

                stat = data["stat"]
                # 播放量
                view = stat["view"]
                item["view"] = view

                # 弹幕
                danmaku = stat["danmaku"]
                item["danmaku"] = danmaku

                # 评论
                reply = stat["reply"]
                item["reply"] = reply

                # 硬币
                coin = stat["coin"]
                item["coin"] = coin

                # 点赞
                like = stat["like"]
                item["like"] = like

                # 收藏
                favorite = stat["favorite"]
                item["favorite"] = favorite

                # 分享
                share = stat["share"]
                item["share"] = share
            # 视频参数
            with open(self.parent_path + "video_info.txt", "w") as file:
                file.write(json.dumps(item, ensure_ascii=False, indent=2))
            return item

    def run(self):
        item = self.get_video_info()
        self.parse_url(item)


def main():
    splider = BLDSplider(55036734)
    splider.run()


if __name__ == '__main__':
    main()
