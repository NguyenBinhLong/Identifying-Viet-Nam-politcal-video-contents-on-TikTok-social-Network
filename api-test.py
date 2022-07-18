from flask import Flask, request, jsonify
from joblib import dump, load
import re
import string

from TikTokApi import TikTokApi
import requests
import subprocess
from pathlib import Path

from class_text_classifier import *
from class_image_classify_model import *
from class_face_reg import *
from fusion_classify_model import *
from class_gg_speech_to_text import *

verify_fp = "verify_l35xaoy9_vvNjtpYh_Nxto_4W4b_BYnZ_i5pUzGxiW5kr"
ms_token = "i0lGDxh4esH2hQctiqZykREVk9wnILcQq0rKteia2t_hRQNnoN-gNraoYK62-qPV9kEDoxPOLSbqY2qPwsrig90rWOUQSNpgPbIc9Fg2swtVoyI_YH8zL1sNNfXSMW0ukF_dhTtcXl11nRcFqA==&X-Bogus=DFSzswSOdjAoFQT5S3LOq37Tlqe6"
sec_user_id = 'MS4wLjABAAAAIX2suxYfrA5EbNZohGg1bpdFVa6hQz1zzLhg54JvZW3Aavm7jI_J__MiabKUx91L'
csrf_session_id = '389ae651aea8039ab693823c9cda7414'
proxy = 'http://lum-customer-hl_25cd8537-zone-data_center:sew2asl5k9kg@zproxy.lum-superproxy.io:22225'

api = TikTokApi(custom_verify_fp=verify_fp, ms_token=ms_token, csrf_session_id=csrf_session_id)
# api = TikTokApi(proxy=proxy, custom_verify_fp=verify_fp, ms_token=ms_token, csrf_session_id=csrf_session_id)

def get_video_info(video_id):
    api_video = api.video(id=video_id)
    info = api_video.info()
    desc = info['desc']
    playAddr = info['video']['playAddr']
    playUrl = info['music']['playUrl']

    data = {
        'desc': desc,
        'url_video': playAddr,
        'url_audio': playUrl
    }

    print('get_video_info: ', data)

    return data


def download_video_id(_video_id):
    print("download_video_id: ", _video_id)
    # try:
    api_video = api.video(id=_video_id)

    # Bytes of the TikTok video
    video_data = api_video.bytes()
    video_name = "download_videos/" + _video_id + '.mp4'
    with open(video_name, "wb") as out_file:
        out_file.write(video_data)
    print("--------------------DONE")
    return 1


def download_video_url(_url_video, _video_id):
    print("download_video_url: ", _url_video)
    video_name = "download_videos/" + _video_id + '.mp4'
    with requests.Session() as req:
        download = req.get(_url_video)
        if download.status_code == 200:
            with open(video_name, 'wb') as f:
                f.write(download.content)
                print("--------------------DONE")
                return True


def download_audio(_url_audio, video_id):
    print("download_audio: ", _url_audio)
    with requests.Session() as req:
        download = req.get(_url_audio)
        if download.status_code == 200:
            with open('download_audios/' + video_id + '.mp3', 'wb') as f:
                f.write(download.content)
                print("--------------------DONE")
                return 1


def extract_key_frames(_video_id):
    print("extract_key_frames: ", _video_id)

    video_name = "download_videos/" + _video_id + ".mp4"
    Path("key_frames/" + _video_id).mkdir(parents=True, exist_ok=True)
    save_path = "key_frames/" + _video_id + "/%02d.jpeg"

    subprocess.call(
        "ffmpeg -skip_frame nokey -i " + video_name + " -vsync vfr -frame_pts true " + save_path,
        shell=True
    )
    print("---------------------DONE")
    return 1


def clean_text(_desc):
    regex1 = "#(\w+)"
    regex2 = "@(\w+)"
    my_str2 = re.sub(regex1, ' ', _desc)
    my_str3 = re.sub(regex2, ' ', my_str2)

    chars = re.escape(string.punctuation)
    _t = "'" + re.sub(r'[' + chars + ']', '', my_str3) + "'"

    strReplaces = "\t\t\t\t;\t\t\t;\t\t;\t;\n;free".split(';')
    tmp = _t

    tmp = tmp.replace('#', ' ')

    for strReplace in strReplaces:
        tmp = tmp.replace(strReplace, '')

    tmp = re.sub(r'<[^>]*>', '', tmp)
    tmp = tmp.lower()
    tmp = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_\[\]]', ' ', tmp)
    tmp = re.sub(r'\s+', ' ', tmp).strip()
    tmp = tmp.replace('  ', ' ')
    tmp = tmp.strip()
    return tmp


text_clf = Text_CLF.getInstance('model/tfidfVectorizer', 'model/text_clf')
image_clf = Image_binary_classify_keras.getInstance()
image_clf.init_model('model/image_clf.h5')
face_reg = Face_reg.getInstance()
fusion_clf = Fusion_CLF.getInstance('model/fusion_clf_lgbm2')


####### INIT
video_id = "7106111741146189083"
print('video_id:', video_id)


#############GET VIDEO INFO
video_info = get_video_info(video_id)

download_video_url(video_info['url_video'], video_id)
download_audio(video_info['url_audio'], video_id)
extract_key_frames(video_id)

_text_audio = speech_to_text(video_id)
_text = video_info['desc'] + " " + _text_audio

text = clean_text(_text)
frames_folder_path = "key_frames/" + video_id

##############PREDICT
text_prediction_score = text_clf.predict_score(text)
print("text_prediction_score: ", text_prediction_score)

image_prediction_score = image_clf.predict_video_frames(frames_folder_path)
print("image_prediction_score:", image_prediction_score)

face_regconition = face_reg.predict_video_frames(frames_folder_path)
print("face_regconition: ", face_regconition)

fusion_score = fusion_clf.predict_score(text_prediction_score, image_prediction_score, face_regconition)
print("fusion_score: ", fusion_score)
