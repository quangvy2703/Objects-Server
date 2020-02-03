from flask import Flask, request, render_template,jsonify
import os
import random
import string

import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'..','Objects', 'src', 'deploy'))
import config
from synthetic import Synthetic
import argparse


prefix = "/home/quangvy2703/Objects-server/"

app = Flask(__name__)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/upload', methods=['POST'])
def my_form_post():
  file = request.files['file']
  file_name = id_generator() + '.mp4'
  input_video = prefix + 'static/uploads/' + file_name
  output_video = prefix + 'static/uploads/converts/' + file_name

  train_dir = "datasets"
  test_dir = "datasets"
  f = open(prefix + "static/uploads/progress/status.txt", "w")
  f.write("0")
  f.close()

  gender = True if 'gender' in request.values.keys() else False
  age = True if 'age' in request.values.keys() else False
  emotion = True if ('emotion' in request.values.keys()) else False
  objects_detection = True if ('objects' in request.values.keys()) else False
  face_recognition = True if ('recognition' in request.values.keys()) else False
  scenes_change = True if ('scenesChange' in request.values.keys()) else False
  face_detection = True if ('faceDetection' in request.values.keys()) else False
  n_classes = 4
  if gender or age or emotion or face_recognition:
    face_detection = True
  else:
    face_detection = False

  file.save(input_video)
  file.close()
  # path_root = '/var/www/html/convertvideo/demo/'
  # input_video = path_root + input_video
  # output_video = path_root + output_video

  parser = argparse.ArgumentParser(description="Synthetic")
  # Face detection arguments
  parser.add_argument('--flip', default=False, type=bool)
  parser.add_argument('--face_detection_model', default='models/retinaface-R50/R50', type=str,
                      help="Path to face detection model, examples, /50 is prefix")
  # parser.add_argument('--face_detection_model_path', default='../models/mnet.25/mnet.25', type=str)
  # Age, emotion, gender
  parser.add_argument('--ga_model', default='models/gamodel-r50/model, 0',
                      help='Path to gender age prediction model')
  parser.add_argument('--emotion_model', type=str, default="models/emotion_model.hdf5",
                      help="Path to emotion prediction model")
  # Face features
  # parser.add_argument('--batch_size', type=int, default=32)
  parser.add_argument('--emb_size', type=int, default=512, help="Embedding size of face features")
  parser.add_argument('--face_feature_model', type=str, default='models/model-r100-ii/model, 0',
                      help="Path to face features extraction model")
  # Object Detection
  parser.add_argument('--object_detection_model', default='models/resnet50_coco_best_v2.1.0.h5',
                      help='Path to objects detection model')
  # Face recognition
  parser.add_argument('--batch_size', type=int, default=32, help="Batch size")
  parser.add_argument('--epochs', type=int, default=300, help="Epochs")
  # parser.add_argument('--emb_size', type=int, default=512, help="Embedding size")
  parser.add_argument('--train_dir', type=str, default="datasets/train/features")
  parser.add_argument('--test_dir', type=str, default="datasets/val/features")
  parser.add_argument('--train', action='store_true')


  parser.add_argument('--gpuid', type=int, default=0, help="GPU ID")
  
  parser.add_argument('--input_video', type=str, default=input_video)
  parser.add_argument('--output_video', type=str, default=output_video)
  parser.add_argument('--use_gender_prediction', type=bool, default=gender)
  parser.add_argument('--use_age_prediction', type=bool, default=age)
  parser.add_argument('--use_emotion_prediction', type=bool, default=emotion)
  parser.add_argument('--use_face_recognition', type=bool, default=face_recognition)
  parser.add_argument('--use_objects_detection', type=bool, default=objects_detection)
  parser.add_argument('--use_scenes_change_count', type=bool, default=scenes_change)
  parser.add_argument('--use_face_detection', type=bool, default=face_detection)
  parser.add_argument('--n_classes', type=int, default=n_classes)
  args = parser.parse_args()
  print(args)

#  if args.train:
#    syn.train_face_recognition()
  syn = Synthetic(args) 
  syn.run()


  data = {
    "data": {
      "originalVideo": {
        'title': file_name,
        'path': input_video
      },
      "processVideo": {
        'title': file_name,
        'path': output_video
      }
    }
  }

  return data

@app.route('/progress', methods=['GET'])
def get_progress():
  f = open("static/uploads/progress/status.txt", "r")
  progress = f.read()
  return {'progress': progress}

if __name__ == '__main__':
    app.run(host="10.142.0.13", port=8000)

