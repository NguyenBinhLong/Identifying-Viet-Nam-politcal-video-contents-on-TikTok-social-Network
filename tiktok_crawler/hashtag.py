from TikTokApi import TikTokApi

from pymongo import MongoClient

conn = MongoClient(
    'mongodb+srv://nguyenbinhlong:MbFgZls0VfDtzehQ@cluster0.iylkd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
)
db = conn['crawler']
collection_tiktok = db['tiktok']

# hashtag = 'nguyenphutrong'
# hashtag = 'tintucchinhphu'
# hashtag = 'chinhphu'
# hashtag = 'dangcongsanvietnam'
# hashtag = 'chinhtri'
# hashtag = '#chungocanh'
# hashtag = 'phamthanhlong'
# hashtag = 'quochoi'
# hashtag = '#vuongdinhhue'
# hashtag = '#phamminhchinh'
# hashtag = '#nguyenxuanphuc'
# hashtag = '#tolam'
# hashtag = '#thoisu'
# hashtag = '#vuducdam'
# hashtag = '#nguyenthanhnghi'
# hashtag = '#nguyentandung'
# hashtag = '#tranhongha'
# hashtag = 'bộ công an'
# is_politics = 1

# hashtag = '#bongdanam'
# hashtag = 'u23chaua'
# hashtag = 'hoahau'
# hashtag = 'thoitrang'
# hashtag = 'sieuxe'
# hashtag = 'oto'
# hashtag = 'bongdanam'
# hashtag = 'trangdiem'
# hashtag = '#meo'
# hashtag = '#husky'
# hashtag = 'bong da'
# hashtag = 'bong chuyen'
# hashtag = 'sức khỏe'
# hashtag = 'ăn uống'
# hashtag = 'Cầu lông'
# hashtag = 'Thể thao mỗi ngày'
# hashtag = 'yogagirl'
# hashtag = '#xatress'
hashtag = '#xàmvuitiktok'
is_politics = 0

verify_fp = "verify_l35xaoy9_vvNjtpYh_Nxto_4W4b_BYnZ_i5pUzGxiW5kr"
ms_token = "i0lGDxh4esH2hQctiqZykREVk9wnILcQq0rKteia2t_hRQNnoN-gNraoYK62-qPV9kEDoxPOLSbqY2qPwsrig90rWOUQSNpgPbIc9Fg2swtVoyI_YH8zL1sNNfXSMW0ukF_dhTtcXl11nRcFqA==&X-Bogus=DFSzswSOdjAoFQT5S3LOq37Tlqe6"
sec_user_id = 'MS4wLjABAAAAIX2suxYfrA5EbNZohGg1bpdFVa6hQz1zzLhg54JvZW3Aavm7jI_J__MiabKUx91L'
csrf_session_id = '389ae651aea8039ab693823c9cda7414'
proxy = 'http://lum-customer-hl_25cd8537-zone-data_center:sew2asl5k9kg@zproxy.lum-superproxy.io:22225'

with TikTokApi(proxy=proxy, custom_verify_fp=verify_fp, ms_token=ms_token, csrf_session_id=csrf_session_id) as api:
# with TikTokApi(proxy=proxy) as api:
    for offset in range(0, 1000, 30):
        for video in api.hashtag(name=hashtag).videos(count=30, offset=offset):
            data = video.as_dict

            print('video_id:', data['id'], 'title', data['desc'])

            if "playAddr" in data['video'] and "playUrl" in data['music']:
                item = {}
                item['id'] = data['id']
                item['hashtag'] = hashtag
                item['desc'] = data['desc']
                item['video'] = data['video']
                item['playAddr'] = data['video']['playAddr']
                item['music'] = data['music']
                item['playUrl'] = data['music']['playUrl']
                item['is_politics'] = is_politics

                # yield items
                collection_tiktok.update_one(
                    {"id": item['id']},
                    {"$set": item},
                    upsert=True
                )

conn.close()
