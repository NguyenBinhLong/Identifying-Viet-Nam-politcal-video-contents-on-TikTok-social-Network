from TikTokApi import TikTokApi
import pymongo
from pymongo import MongoClient

conn = MongoClient(
    'mongodb+srv://nguyenbinhlong:MbFgZls0VfDtzehQ@cluster0.iylkd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
)
db = conn['crawler']
collection_tiktok = db['tiktok']

verifyFp = "erify_l35xaoy9_vvNjtpYh_Nxto_4W4b_BYnZ_i5pUzGxiW5kr"
msToken = "i0lGDxh4esH2hQctiqZykREVk9wnILcQq0rKteia2t_hRQNnoN-gNraoYK62-qPV9kEDoxPOLSbqY2qPwsrig90rWOUQSNpgPbIc9Fg2swtVoyI_YH8zL1sNNfXSMW0ukF_dhTtcXl11nRcFqA==&X-Bogus=DFSzswSOdjAoFQT5S3LOq37Tlqe6"
csrf_session_id = 'MS4wLjABAAAAIX2suxYfrA5EbNZohGg1bpdFVa6hQz1zzLhg54JvZW3Aavm7jI_J__MiabKUx91L'

username = '@lichsuvietnam35'

with TikTokApi(custom_verify_fp=verifyFp, ms_token=msToken) as api:
    for offset in range(0, 60, 30):
        for video in api.user(username=username).videos(count=30, offset=offset):
            data = video.as_dict

            print(data['desc'])

            # item = {}
            # item['id'] = data['id']
            # item['username'] = username
            # item['desc'] = data['desc']
            # item['video'] = data['video']
            # item['music'] = data['music']
            #
            # # yield items
            # collection_tiktok.update_one(
            #     {"id": item['id']},
            #     {"$set": item},
            #     upsert=True
            # )
