import oss2
import requests
auth = oss2.Auth('LTAIQCTBQ4StGm9u','xcUCHfU3JZBPpXq5kQttkJO9yO3OjQ')
bucket = oss2.Bucket(auth,'oss-cn-beijing.aliyuncs.com','howechenya')
url = bucket.sign_url('GET','songs',60)
print(url)
res = requests.get(url)
songs = str(res.content)
index = len(songs)-2
songs_list = songs[2:index].split(',')

for s in songs_list:
    print(bucket.sign_url('GET',s+'.m4a',1800))
# sf = open('/home/alexhowe/Music/CloudMusic/songs')
#
# lsf = sf.read()
# lsfs = lsf .split(',')
#
# for ls in lsfs :
#     print(ls)
#
# sf.close()