#--coding:utf-8--
#author:HoweChen Email:1090710046@qq.com
import re
import requests
import os
#专辑id,网页打开专辑详情分析URL获取
album_id = '001QmRCD2PGa4o'
#歌曲信息id
songmid=''
#歌曲资源id
songid =''
#获取专辑详情html
url_album = 'https://y.qq.com/n/yqq/album/'+album_id+'.html'

pa = re.compile(r'"songmid":"(.*?)"')

pa2 = re.compile(r'"songname":"(.*?)"')

pa3 = re.compile(r'ws.stream.qqmusic.qq.com/(.*?).m4a')

url_detail='https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid='+songmid+'=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback&g_tk=' \
           '5381&jsonpCallback=getOneSongInfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'

url_source= 'http://dl.stream.qqmusic.qq.com/'+songid+'.m4a?vkey=E24DD0C63489E5E5B07CFD8E410C165FDF9AE663BB860DBB1EF9D5E57E5C2673A88477EE2E554' \
            '7A1318531F899CB75A368317CDCDA0EB009&guid=7978049712&uin=0&fromtag=66'

class song(object):
    def __init__(self,songmid,songname):
        self.songmid = songmid
        self.songname = songname

def grab_album():
    res = requests.get(url_album)
    songmids = pa.findall(res.text)
    songnames = pa2.findall(res.text)
    songs = []
    for i in range(len(songmids)):
        Song = song("","")
        Song.songmid=songmids[i]
        Song.songname = songnames[i]
        songs.append(Song)
    return songs

def grab_songid():
    infos = grab_album()
    sds =[]
    for i in infos:
        songmid = i.songmid
        url_detail = 'https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid=' + songmid + '&tpl=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback&g_tk=' \
                                                                                                   '5381&jsonpCallback=getOneSongInfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'

        res_sd = requests.get(url_detail)
        sd = pa3.findall(res_sd.text)
        sds.append(sd[0])

    return sds

def download_songs():
    #歌曲保存路径，根据自己电脑修改
    path = '/home/alexhowe/Music/CloudMusic/'
    if not os.path.exists(path):
        os.mkdir(path)
    songs = grab_album()
    songids = grab_songid()

    for i in range(len(songids)):
        url_source = 'http://dl.stream.qqmusic.qq.com/' + songids[i] + '.m4a?vkey=E24DD0C63489E5E5B07CFD8E410C165FDF9AE663BB860DBB1EF9D5E57E5C2673A88477EE2E554' \
                                                                   '7A1318531F899CB75A368317CDCDA0EB009&guid=7978049712&uin=0&fromtag=66'
        res = requests.get(url_source)
        if '/' in songs[i].songname:
            songs[i].songname = str(songs[i].songname).replace('/','|')
        with open(path+str(songs[i].songname)+'.mp3','wb') as f :
            print("Downloading  "+str(songs[i].songname)+'.................')
            f.write(res.content)
        print("Successfully downloaded!")

if __name__ == '__main__':
    download_songs()