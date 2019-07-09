import requests
import re
import subprocess
import os
import json
from  lxml import etree
# 视频音频分离,需要进行合并
class BLDSplider:
    regex_cid = re.compile("\"cid\":(.{8})")

    def __init__(self, aid):
        self.aid = aid
        self.origin_url = "https://www.bilibili.com/video/av{}?from=search&seid=9346373599622336536".format(aid)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",

        }

        self.video_url = "https://upos-sz-mirrorks32u.acgvideo.com/upgcxcode/{}/{}/{}/{}-1-30032.m4s?"
        self.voice_url = "https://upos-sz-mirrorks32u.acgvideo.com/upgcxcode/{}/{}/{}/{}-1-30216.m4s?"

        # 检查目录
        self.parent_path = "e:/bilibili/" + str(self.aid) + "/"
        if not os.path.exists(self.parent_path):
            os.makedirs(self.parent_path)

        self.video_name = self.parent_path + str(self.aid) + ".mp4"
        self.voice_name = self.parent_path + str(self.aid) + ".mp3"


    def parse_url(self,item):
        cid = item["cid"]
        print("cid:%s" % cid)
        title = item["title"]
        print("title:%s" % title)


        # 切割参数
        first_param = cid[-2:]
        second_param = cid[-4:-2]

        self.headers["Referer"] = self.origin_url
        # 视频
        video_response = requests.get(self.video_url.format(first_param, second_param, cid, cid), headers=self.headers)
        if video_response.status_code == 200:
            # print(video_response.headers)
            with open(self.video_name,"wb") as file:
                 file.write(video_response.content)

        # 音频
        voice_response = requests.get(self.voice_url.format(first_param,second_param,cid,cid),headers=self.headers)
        if voice_response.status_code == 200:
            with open(self.voice_name,"wb") as file:
                file.write(voice_response.content)




    # 将视频音频进行合并
    def combine(self,title):
        print(self.video_name)
        print(self.voice_name)
        cmd = "D:/ffmpeg-4.1.3-win64-static/bin/ffmpeg -i " + self.video_name + " -i " + self.voice_name + " -strict -2 -f mp4 e:/" + title + ".mp4"
        print(cmd)
        subprocess.call(cmd)


    # 获取视频相关参数
    def get_video_info(self):
        response = requests.get(self.origin_url,headers=self.headers)
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
            info_url = "https://api.bilibili.com/x/web-interface/view?aid={}&cid={}".format(self.aid,cid)
            info_response = requests.get(info_url,headers=self.headers)
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

        # self.parse_url(item)
        # print("文件下载完毕,开始合并")
        # # 合并
        # self.combine(item["title"])



def main():
    splider = BLDSplider(53545832)
    splider.run()


if __name__ == '__main__':
    main()


