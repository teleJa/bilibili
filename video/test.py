import requests
import json
import os
# url = "https://api.bilibili.com/x/player/playurl?avid=55036734&cid=96243521&qn=0&type=&otype=json"
#
# #url = "http://upos-hz-mirrorks3u.acgvideo.com/upgcxcode/21/35/96243521/96243521-1-32.flv?e=ig8euxZM2rNcNbhVhwdVhoMzhwdVhwdEto8g5X10ugNcXBlqNxHxNEVE5XREto8KqJZHUa6m5J0SqE85tZvEuENvNC8xNEVE9EKE9IMvXBvE2ENvNCImNEVEK9GVqJIwqa80WXIekXRE9IMvXBvEuENvNCImNEVEua6m2jIxux0CkF6s2JZv5x0DQJZY2F8SkXKE9IB5QK==&deadline=1562595805&gen=playurl&nbs=1&oi=0&os=ks3u&platform=pc&trid=cc126e5455c34de39a84aa37ecdb53da&uipk=5&upsig=3fff20385d99ec7fda42f36b1aaf903b&uparams=e,deadline,gen,nbs,oi,os,platform,trid,uipk&mid=0"
# headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
#             "Referer": "https://www.bilibili.com/video/av55036734?from=search&seid=9346373599622336536"
#         }
# response = requests.get(url, headers=headers)
# result = json.loads(response.content.decode())
# video_url = result["data"]["durl"][0]["url"]
# print(video_url)
#
# print(headers)
# res = requests.get(video_url, headers=headers)
# print(res.status_code)
# with open("e:/test.flv","wb") as file:
#     file.write(res.content)

import sys
import time
def process_bar(precent, width=50):
    use_num = int(precent*width)
    print(use_num)
    space_num = int(width-use_num)
    precent = precent*100
    #   第一个和最后一个一样梯形显示, 中间两个正确,但是在python2中报错
    #
    # print('[%s%s]%d%%'%(use_num*'#', space_num*' ',precent))
    # print('[%s%s]%d%%'%(use_num*'#', space_num*' ',precent), end='\r')
    # print('[%s%s]%d%%'%(use_num*'#', space_num*' ',precent),file=sys.stdout,flush=True, end='\r')
    print('[%s%s]%d%%'%(use_num*'#', space_num*' ',precent),file=sys.stdout,flush=True)


if __name__ == '__main__':
    for i in range(21):
        precent = i/20
        process_bar(precent)
        time.sleep(0.2)
    print('\n')
