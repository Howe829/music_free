import TencentYoutuyun

AppID = '10143555'

SecretID = 'AKIDXwGSSEd8G9pKej7R3QaVBcolV0GNtvLX'

SecretKey = '80d1A9rJYbOvDF3dzFKBnBKEtJUQ7aoo'

userid= '1090710046'

end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT

youtu = TencentYoutuyun.YouTu(AppID,SecretID,SecretKey,userid,end_point)

result = youtu.fooddetect('/home/alexhowe/Pictures/hotdog.jpzg',data_type=0,seq= '')

print(result)