import os

os.system("python /media/vy/DATA/projects/face/project3/Objects/main.py  --input_video static/uploads/FKLZBE.mp4  --output_video static/uploads/results/FKLZBE.mp4  --train_dir datasets/fer2013/train/train  --test_dir datasets/fer2013/test/test   --use_ga_prediction True  --use_emotion_prediction True  --use_face_detection True  --emb_size 512   --use_face_recognition True  --n_classes 4")
