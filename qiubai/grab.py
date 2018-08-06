import re
import requests

res = requests.get("https://www.qiushibaike.com/")

class joke():
    def __init__(self,auth):
        pass

pa1 = re.compile(r'<div class="content">\n<span>\n\n\n(\D*)\n\n</span>\n\n</div>')

pa2 = re.compile(r'<img src="([\w|\S]*)" alt="(\S*)"')



contents = pa1.findall(res.text)
authors = pa2.findall(res.text)

jokes=[]

for c in contents :
    print(c)


for a in authors:
    print(a)