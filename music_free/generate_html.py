import requests
import generate_singer_pics

def gne_html(singer_name,album_name):
        res = requests.get('https://howechenya.oss-cn-beijing.aliyuncs.com/'+album_name+'.json')
        singer_pics = generate_singer_pics.gne_singer_pics(singer_name)
        head = '<div class="section">\n'
        tail = '</div>\n'
        final = ''
        for s in singer_pics:
            middle = '<img src='+s+' >\n'
            final += head+middle+tail
        if len(singer_pics)==0:
            final+='<img src='+'https://howechenya.oss-cn-beijing.aliyuncs.com/'+album_name+'/album_img.jpg'

        with open('/home/alexhowe/ap_demo/web_origin.html','r') as f:
            str = f.read()

        html = str.replace('audio_json',res.text)
        html = html.replace('div_pic',final)
        print(html)
        with open('/home/alexhowe/ap_demo/web1.html','w') as f:
            f.write(html)
        return res.status_code==200

# print(str)
# print(str.index('audio_json'))