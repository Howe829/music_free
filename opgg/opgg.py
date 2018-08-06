import requests
from bs4 import BeautifulSoup as bs
import re

url_s = 'http://www.op.gg/spectate/pro/'
url_c = 'www.op.gg/summoner/userName='
url_p = 'http://best.gg/player/'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Cookie': 'Hm_lvt_29884b6641f1b5709cc89a8ce5a99366=1532928521; _ga=GA1.3.354331290.1532928521; _gid=GA1.3.572502062.1532928521; _hist=xiaolongxia; Hm_lpvt_29884b6641f1b5709cc89a8ce5a99366=1532932585; wcs_bt=55c48ac9e22bec:1532932585; sc_is_visitor_unique=rx8630180.1532932585.78B7C18DF6AF4F9C1A4908B8135EB15E.2.1.1.1.1.1.1.1.1; customLocale=zh_CN',
           'Host': 'www.op.gg',
           'Referer': 'http://www.op.gg/spectate/pro/',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', }
ranks = {"Challenger":"最强王者","Master":'超凡大师',"Diamond 1":"璀璨钻石一","Diamond 2":"璀璨钻石二","Diamond 3":'璀璨钻石三',"Diamond 4":'璀璨钻石四',"Diamond 5":'璀璨钻石五', "Platinum 1":"华贵铂金一","Platinum 2":"华贵铂金二","Platinum 3":"华贵铂金三"}



class Summoner(object):
    def __init__(self, team, name, champion, rank, sname):
        self.name = name
        self.champion = champion
        self.team = team
        self.rank = rank
        self.sname = sname



def spectate_pro():
    res = requests.get(url_s, headers=headers)
    soup = bs(res.text, 'lxml')
    Champions_ = soup.find_all(class_='ChampionName')
    Summoners_ = soup.find_all(class_='SummonerName')
    Name_ = soup.find_all(class_ ='Extra')
    TeamName_ = soup.find_all(class_='TeamName')
    pa = re.compile(r'//opgg-static.akamaized.net/images/lol/champion/\D+.png')
    l_cimgs = pa.findall(res.text)

    for c in Champions_:
        summoner = Summoner('', '', '', '','')
        summoner.champion = c.string
        Summoners.append(summoner)
    for i in range(len(Summoners)):
        Summoners[i].sname = Summoners_[i].string
        Summoners[i].name = Name_[i].string
        Summoners[i].team = TeamName_[i].string
        Summoners[i].cimg = l_cimgs[i]

def user():
    for s in Summoners:
      res = requests.get(str('http://'+url_c+s.sname))
      soup = bs(res.text,'lxml')
      r = soup.find_all(class_='tierRank')[0].string
      s.rank = ranks[r]

      #print(s.rank)

if __name__=='__main__':

    Summoners = []
    spectate_pro()
    user()
    for su in Summoners:
        print(su.team+" 战队的 "+su.name," 正在韩服高端局使用:",su.champion+" ID:"+su.sname+" 段位:"+su.rank+" img:"+su.cimg)


