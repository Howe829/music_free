import requests
import re

pa = re.compile(r'data-original="(.*?)"')

def gne_singer_pics(singer_name):
    url_search = 'http://www.haibao.com/search/index.html?name='+singer_name+'&type=3&orderType=3&isHighLight=0'
    res = requests.get(url_search)
    img_urls = pa.findall(res.text)
    urls_baked = []
    for i in img_urls:
        ub = str(i)
        ub = ub.replace('/imagecut/0_400','')

        if 'c3' in i :
            ub = ub.replace('c3','c1')
            ub = ub.replace('pic/0','img/0')
        if 'c2' in i and 'piccommon' in i:
            ub = ub.replace('c2','c3')
        # if 'c4' in i :
        #     ub = ub.replace('pic/0','img/0')
        if 'piccommon' in i  and requests.get(i).status_code==200 :
            urls_baked.append(ub)

    return urls_baked


if __name__ == '__main__':
    gne_singer_pics('Lorde')
    # http://c2.haibao.cn/pic/0_0_100_0/li0s6T7fW8Ajc/piccommon/1213/12139/li0s6T7fW8Ajc.jpg