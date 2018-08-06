#Author：HoweChen Email:1090710046@qq.com
# -- coding: utf-8 --
import re
import requests
import os
import time
from PIL import Image
from io import BytesIO

#建一个英雄类存英雄的名字和地址
class hero:
    def __init__(self,name,url):
        self.name = name
        self.url = url

#皮肤类存皮肤的名字和皮肤代码的
class skin:
    def __init__(self,name,code):
        self.name=name
        self.code=code

#爬取英雄的名字
def grab_hero_info():
    url1='http://lol.qq.com/biz/hero/champion.js'
    response = requests.get(url1)
    pat = re.compile(r'"([0-9]{1,4})":"([\w]*)",*')
    l = pat.findall(response.text)#找出champion.js中所有符合正则表达式的内容，存在一个元祖tuple l中
    return l

#生成一个英雄类实例
def generate_hero():
    heros = []
    hero_infos =grab_hero_info()
    for i in hero_infos:
        hero1= hero('','')
        hero1.name = i[1]
        print ('Generating '+hero1.name+'...')
        hero1.url = 'http://lol.qq.com/biz/hero/' + hero1.name + '.js'
        heros.append(hero1)
    return heros

#爬取每个皮肤的名字和皮肤代码
def grab_skin_info():
    heros = generate_hero()
    skins = []
    for h in heros:
        res = requests.get(h.url)
        pat = re.compile(r'"id":"([0-9]*)","num":[0-9]*,"name":"([\w]*|(\\[\w]*)*\s*(\\[\w]*)*)"')
        my_l = pat.findall(res.text)
        for s in my_l:
            skin1 = skin('','')
            skin1.code=s[0]
            skin1.name=eval(repr(s[1]).replace('\\\\', '\\'))#将双斜杠替换成单斜杠，有兴趣的朋友可以将代码放在终端中看一些终端爬下来的是什么样的
            print ('Skin: '+skin1.name+"'s url is generated!")
            skins.append(skin1)
    return skins

#通过皮肤代码来爬取每一张皮肤海报并保存到本地
def grab_skin_images():
    skins = grab_skin_info()
    count = 0
    default=0
    t1 = time.time()
    img_urls = []
    for sk in skins:
        img_url = "http://ossweb-img.qq.com/images/lol/web201310/skin/big"+sk.code+".jpg"
        img_urls.append(img_url)
        response = requests.get(img_url)
        image = Image.open(BytesIO(response.content))
        path='/home/alexhowe/lol/'
        if not os.path.exists(path):
            os.mkdir(path)
            print ('Skin images in path: '+path)
        print ('Grabbing skin image '+sk.name+'.jpg')
        sname = str(sk.name.encode('utf-8'))
        if sname =='default':
            sname = sname+str(default)
            default = default +1
            image.save(path + sname + ".jpg")
        else:
            image.save(path+sk.name+".jpg")
        count = count +1
    t2=time.time()
    t=t2-t1
    print ('Congratulations!Grab successfully! There are '+str(count)+' images. Use '+str(t)+'s')
    return img_urls

if __name__=='__main__':
    try:
        grab_skin_images()
    except Exception as e:
        print ('Error:',e)



