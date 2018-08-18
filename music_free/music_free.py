#--coding:utf-8--
#author:HoweChen Email:1090710046@qq.com
import re
import requests
import os
from bs4 import BeautifulSoup as bs
import time
import oss2
from oss2.models import BucketWebsite
import json
import get_song_id
import generate_html
import os

auth = oss2.Auth('LTAIQCTBQ4StGm9u','xcUCHfU3JZBPpXq5kQttkJO9yO3OjQ')
bucket = oss2.Bucket(auth,'oss-cn-beijing.aliyuncs.com','howechenya')
bucket.put_bucket_website(BucketWebsite('index.html', 'error.html'))
#专辑id,网页打开专辑详情分析URL获取(Album ID)

album_id = '002uS1Hd180SQ3'
#歌曲信息id
songmid=''
#歌曲资源id
songid =''
#获取专辑详情html
url_album = 'https://y.qq.com/n/yqq/album/'+album_id+'.html'

pa = re.compile(r'"songmid":"(.*?)"')

pa2 = re.compile(r'"songname":"(.*?)"')

pa3 = re.compile(r'ws.stream.qqmusic.qq.com/(.*?).m4a')

pa4 = re.compile(r'"albumname":"(.*?)"')

pa5 = re.compile(r'"singers":"(.*?)"')

pa6 = re.compile(r'"media_mid":"(.*?)"')


url_detail='https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid='+songmid+'=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback&g_tk=' \
           '5381&jsonpCallback=getOneSongInfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'

url_source= 'http://dl.stream.qqmusic.qq.com/'+songid+'.m4a?vkey=E24DD0C63489E5E5B07CFD8E410C165FDF9AE663BB860DBB1EF9D5E57E5C2673A88477EE2E554' \
            '7A1318531F899CB75A368317CDCDA0EB009&guid=7978049712&uin=0&fromtag=66'
album_img = ''

song_json = []
class song(object):
    def __init__(self,songmid,songname,albumname,singers):
        self.songmid = songmid
        self.songname = songname
        self.albumname = albumname
        self.singers = singers

def grab_album():
    res = requests.get(url_album)
    soup = bs(res.text,'lxml')
    ls = str(soup.find_all(id = 'albumImg')[0])
    album_img = 'https:'+ls[ls.index('" src="')+7:-3]
    resp = requests.get(album_img)

    songmids = pa.findall(res.text)
    songnames = pa2.findall(res.text)
    albumname = pa4.findall(res.text)
    singers = pa5.findall(res.text)
    songs = []
    print(len(songmids))
    for i in range(int(len(songmids)/2)):
        Song = song("","","","")
        Song.songmid=songmids[i]
        Song.songname = songnames[i]
        Song.albumname = albumname[i]
        Song.singers = singers[i]
        Song.album_img = album_img
        songs.append(Song)
    result = bucket.put_object(songs[0].albumname+'/album_img.jpg',resp.content)
    print(len(songs))
    return songs

def grab_songid(infos):
    sds =[]

    for i in infos:
        songmid = i.songmid
        url_detail = 'https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid=' + songmid + '&tpl=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback&g_tk=' \
                                                                                                   '5381&jsonpCallback=getOneSongInfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'

        res_sd = requests.get(url_detail)
        sd = pa3.findall(res_sd.text)
        i.media_mid = pa6.findall(res_sd.text)[0]
        sds.append(sd[0])
    return sds

def mutation(songs):
    pa7 = re.compile(r'"vkey":"(.*?)"')
    headers = ['C400']
    for s in songs:
        url_fcg = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&jsonpCallback=MusicJsonCallback6156217366676482&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&' \
                  'cid=205361747&callback=MusicJsonCallback6156217366676482&uin=0&songmid='+s.songmid+'&filename='+headers[0]+s.media_mid+'.m4a&guid=7978049712'
        res = requests.get(url_fcg)
        info = str(res.content)
        s.vkey = pa7.findall(info)[0]
        # print(s.vkey)
    return songs
def download_lyrics(songs):
    count = 1
    searcher = get_song_id.search()
    for song in songs :
        song_id = str(searcher.search_song(song.songname+'-'+song.singers))
        url_lyric = 'http://music.163.com/api/song/lyric?os=pc&id='+song_id+'&lv=-1&kv=-1&tv=-1'
        res = requests.get(url_lyric)
        print(res.text)
        while  '"uncollected":true' in str(res.text) and count<9:
            song_ids = str(searcher.search_song(song.songname+'-'+song.singers,index=count))
            url_lyric = 'http://music.163.com/api/song/lyric?os=pc&id=' + song_ids + '&lv=-1&kv=-1&tv=-1'
            res = requests.get(url_lyric)
            count+=1
            print(song_ids)
        rest = json.loads(res.text)
        print(song.songname,' ', song_id)
        lyric = rest['lrc']['lyric']
        tlyric = rest['tlyric']['lyric']
        lyric_name = song.songname + '-' + song.singers + '.lrc'
        if lyric==None :
            print(lyric_name+' Not Found!')
            continue
        result = bucket.put_object(song.albumname+'/'+lyric_name,lyric)
        if tlyric==None:
            print('t_'+lyric_name+' Not Found!')
            continue
        result = bucket.put_object(song.albumname+'/t_'+lyric_name,tlyric)


def download_songs():
    #歌曲保存路径，根据自己电脑修改(Save Path)
    path = '/home/alexhowe/Music/CloudMusic/'
    if not os.path.exists(path):
        os.mkdir(path)
    songs = grab_album()
    songids = grab_songid(songs)
    print('Now begin to download album '+songs[0].albumname+' please wait........')
    t1 = time.time()
    song_paths = ''
    count = 0
    download_lyrics(songs)
    for i in range(len(songids)):
        url_source = 'http://dl.stream.qqmusic.qq.com/' + songids[i] + '.m4a?vkey=E24DD0C63489E5E5B07CFD8E410C165FDF9AE663BB860DBB1EF9D5E57E5C2673A88477EE2E554' \
                                                                   '7A1318531F899CB75A368317CDCDA0EB009&guid=7978049712&uin=0&fromtag=66'
        res = requests.get(url_source)
        song_name = str(songs[i].songname+'-'+songs[i].singers+'.m4a')
        if '/' in song_name:
            song_name = song_name.replace('/','|')
        if len(res.content) == 0 :
            count += 1
            print('CallBack is empty,jump to next...........')
            continue
        result = bucket.put_object(songs[0].albumname+'/'+song_name,res.content)
        print(result.status)
        sp = songs[i].albumname+'/'+songs[i].songname+'-'+songs[i].singers
        song_paths += sp +','
        song_dict ={'name':songs[i].songname,'artist':songs[i].singers,'url':url_source,'cover':'https://howechenya.oss-cn-beijing.aliyuncs.com/'+songs[i].albumname+'/album_img.jpg','lrc':'https://howechenya.oss-cn-beijing.aliyuncs.com/'+sp+'.lrc'}
        song_json.append(song_dict)
    print(json.dumps(song_json))
    result = bucket.put_object(songs[0].albumname+'.json',json.dumps(song_json))
    print(result)
    reu = generate_html.gne_html(songs[0].singers,songs[0].albumname)
    print(reu)
    if reu == True:
        os.system('google-chrome //home/alexhowe/ap_demo/web1.html')
        # with open(path+song_name,'wb') as f :
        #     print("Downloading  "+song_name+'.................')
        #     f.write(res.content)
    # with open(path+'/songs','w') as f:
    #     f.write(str(song_paths))


    if count >= 3:
        print('Found too many empty files ,now using MUTATION MODE pls wait .....')
        m_songs = mutation(songs)
        for i in range(len(m_songs)):
            url_msource = 'http://dl.stream.qqmusic.qq.com/C400' + m_songs[i].media_mid + '.m4a?vkey='+m_songs[i].vkey+'&guid=7978049712&uin=0&fromtag=66'
            res = requests.get(url_msource)
            song_name = str(songs[i].songname + '-' + songs[i].singers + '.m4a')
            if '/' in song_name:
                song_name = song_name.replace('/', '|')
            # print(url_msource)
            # result = bucket.put_object(songs[0].albumname + '/' + song_name, res.content)
            # print(result.status)
            with open(path+song_name,'wb') as f :
                print("Downloading  "+song_name+'.................')
                f.write(res.content)
    # result = bucket.put_object('songs', song_paths)
    # print(result.status)
        # audiofile =AudioSegment.from_file(path+song_name,'m4a')
        # tags = {'artist':songs[i].singers,'album':songs[i].albumname,'album_artist':songs[i].singers,'title':songs[i].songname}
        # audiofile.export(song_name,tags=tags)
    t2 = time.time()
    print("Successfully downloaded! "+songs[0].albumname+' There are/is '+str(len(songs))+' songs. Used '+str(t2-t1)+' s Enjoy!')




if __name__ == '__main__':
    download_songs()
    # grab_songid(grab_album())
