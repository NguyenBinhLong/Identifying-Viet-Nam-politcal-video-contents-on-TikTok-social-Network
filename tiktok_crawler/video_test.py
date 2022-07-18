import sys
from TikTokApi import TikTokApi

verify_fp = "verify_l35xaoy9_vvNjtpYh_Nxto_4W4b_BYnZ_i5pUzGxiW5kr"
ms_token = "i0lGDxh4esH2hQctiqZykREVk9wnILcQq0rKteia2t_hRQNnoN-gNraoYK62-qPV9kEDoxPOLSbqY2qPwsrig90rWOUQSNpgPbIc9Fg2swtVoyI_YH8zL1sNNfXSMW0ukF_dhTtcXl11nRcFqA==&X-Bogus=DFSzswSOdjAoFQT5S3LOq37Tlqe6"
sec_user_id = 'MS4wLjABAAAAIX2suxYfrA5EbNZohGg1bpdFVa6hQz1zzLhg54JvZW3Aavm7jI_J__MiabKUx91L'
csrf_session_id = '389ae651aea8039ab693823c9cda7414'
proxy = 'http://lum-customer-hl_25cd8537-zone-data_center:sew2asl5k9kg@zproxy.lum-superproxy.io:22225'

api = TikTokApi(custom_verify_fp=verify_fp, ms_token=ms_token, csrf_session_id=csrf_session_id)

video_id = "7113876486179851546"
api_video = api.video(id=video_id)
info = api_video.info()
desc = info['desc']
playAddr = info['video']['playAddr']
playUrl = info['music']['playUrl']
print(desc)
print(playAddr)
print(playUrl)


