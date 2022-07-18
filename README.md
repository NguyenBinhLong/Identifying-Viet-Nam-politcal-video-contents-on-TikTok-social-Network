# Identifying-Viet-Nam-politcal-video-contents-on-TikTok-social-Network

#CODE NOTE

#thu thập & Xử lý dữ liệu
- folder tiktok_crawler => crawler data from tiktok
- speect2text.ipynb => audio file speech to text

#training model
- text_classification_final.ipynb => train model text classify
- face_detect.ipynb => detect face and save vetor face feature
- class_image_classify_model.py => train model image classify
- fusion_classify_model.py => train model fusion Ligh GBM

#Predict video
- predict.py
####### INIT id video
video_id = "7106111741146189083"

print('video_id:', video_id)

# to do:
- download video from tiktok in to folder download_videos/
- download audio from tiktok in to folder download_audio/
- extract key frame from video to folder key_frames/
- use gg api speech to text to generate text
- load model tranned: text, face, image, lighgbm
- pre process text data
=> predict video is politcal?


