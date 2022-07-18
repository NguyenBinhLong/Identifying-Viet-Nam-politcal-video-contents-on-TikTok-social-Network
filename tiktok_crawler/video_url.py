# import sys
#
# from TikTokApi import TikTokApi
# import requests
# from pymongo import MongoClient
# import os
#
# conn = MongoClient(
#     'mongodb+srv://nguyenbinhlong:MbFgZls0VfDtzehQ@cluster0.iylkd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
# )
# db = conn['crawler']
# collection_tiktok = db['tiktok']
#
# verify_fp = "verify_l35xaoy9_vvNjtpYh_Nxto_4W4b_BYnZ_i5pUzGxiW5kr"
# ms_token = "i0lGDxh4esH2hQctiqZykREVk9wnILcQq0rKteia2t_hRQNnoN-gNraoYK62-qPV9kEDoxPOLSbqY2qPwsrig90rWOUQSNpgPbIc9Fg2swtVoyI_YH8zL1sNNfXSMW0ukF_dhTtcXl11nRcFqA==&X-Bogus=DFSzswSOdjAoFQT5S3LOq37Tlqe6"
# sec_user_id = 'MS4wLjABAAAAIX2suxYfrA5EbNZohGg1bpdFVa6hQz1zzLhg54JvZW3Aavm7jI_J__MiabKUx91L'
# csrf_session_id = '389ae651aea8039ab693823c9cda7414'
# proxy = 'http://lum-customer-hl_25cd8537-zone-data_center:sew2asl5k9kg@zproxy.lum-superproxy.io:22225'
#
# # api = TikTokApi(proxy=proxy, custom_verify_fp=verify_fp, ms_token=ms_token, csrf_session_id=csrf_session_id)
# api = TikTokApi(custom_verify_fp=verify_fp, ms_token=ms_token, csrf_session_id=csrf_session_id)
#
#
# def download_video(url_video):
#     api_video = api.video(id=_video['id'])
#
#     # Bytes of the TikTok video
#     video_data = api_video.bytes()
#     video_name = "video" + str(_num_folder) + "/" + _video['id'] + '.mp4'
#     with open(video_name, "wb") as out_file:
#         out_file.write(video_data)
#     print("--------------------DONE")
#     return 1
#     # except:
#     #     print(f"Download Failed For File {_video['id']}")
#     #     return 0
#
#
# def download(url):
#     try:
#         with requests.Session() as req:
#             download = req.get(url_video)
#             if download.status_code == 200:
#                 with open(video_name, 'wb') as f:
#                     return True
#             else:
#                 return False
#         return False
#
#
# list_video = collection_tiktok.find({
#     "$or": [
#         {"video_downloaded": 0},
#         {"video_downloaded": {"$exists": False}}
#     ]
# }, {"_id": 1, "playAddr": 1, "id": 1}
# ).limit(10)
#
# num_folder = 1
# num_video = 0
#
# while len(list(list_video)) > 0:
#
#     list_video = collection_tiktok.find({
#         "$or": [
#             {"video_downloaded": 0},
#             {"video_downloaded": {"$exists": False}}
#         ]
#     }, {"_id": 1, "playAddr": 1, "id": 1}
#     ).limit(10)
#
#     print("============START WHILE NEW")
#     for video in list_video:
#         print("download video id:", video['id'], "num_video: ", num_video, " - num_folder: ", num_folder)
#
#         # check so luong video va tao moi folder
#         num_video += 1
#         if num_video > 200:
#             num_folder += 1
#             num_video = 0
#             # create sub folder image
#             os.mkdir("video" + str(num_folder))
#
#         result = download_video(video, num_folder)
#         if result:
#             collection_tiktok.update_one(
#                 {'_id': video['_id']},
#                 {"$set": {"video_downloaded": 1}},
#                 upsert=False
#             )
#             continue
#
#         result_url = download_video_url(video, num_folder)
#         if result_url:
#             collection_tiktok.update_one(
#                 {'_id': video['_id']},
#                 {"$set": {"video_downloaded": 1}},
#                 upsert=False
#             )
#             continue
#
#         # crawl fall
#         print("--------------------FALL")
#         collection_tiktok.update_one(
#             {'_id': video['_id']},
#             {"$set": {"video_downloaded": 2}},
#             upsert=False
#         )
#
#     list_video = collection_tiktok.find({
#         "$or": [
#             {"video_downloaded": 0},
#             {"video_downloaded": {"$exists": False}}
#         ]
#     }, {"_id": 1, "playAddr": 1, "id": 1}
#     ).limit(10)
#
# conn.close()
# print("--------------------COMPLETE")
# sys.exit()
