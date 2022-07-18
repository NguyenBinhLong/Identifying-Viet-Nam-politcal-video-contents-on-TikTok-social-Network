
from TikTokApi import TikTokApi
import requests
import subprocess
from pathlib import Path
import re
import string

def get_video_info(video_id, api):
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


def download_video_id(_video_id, api):
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

    video_name = "download_videos" + _video_id + ".mp4"
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
