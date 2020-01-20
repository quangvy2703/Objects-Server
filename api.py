from flask import Flask, request, render_template,jsonify
import os
import random
import string

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
  input_video = 'static/uploads/' + file_name
  output_video = 'static/uploads/converts/' + file_name

  train_dir = "datasets"
  test_dir = "datasets"
  f = open("static/uploads/progress/status.txt", "w")
  f.write("0")
  f.close()

  gender = "True" if 'gender' in request.values.keys() else "False"
  age = "True" if 'age' in request.values.keys() else "False"
  emotion = "True" if ('emotion' in request.values.keys()) else "False"
  objects_detection = "True" if ('objects' in request.values.keys()) else "False"
  face_recognition = "True" if ('recognition' in request.values.keys()) else "False"
  scenes_change = "True" if ('scenesChange' in request.values.keys()) else "False"
  face_detection = "True" if ('faceDetection' in request.values.keys()) else "False"
  n_classes = "4"
  if "Tru" in gender or "Tru" in age or "Tru" in emotion or "Tru" in face_recognition:
    face_detection = "True"

  file.save(input_video)

  # path_root = '/var/www/html/convertvideo/demo/'
  # input_video = path_root + input_video
  # output_video = path_root + output_video

  # cmd = "python /media/vy/DATA/projects/face/project3/Objects/main.py  " \
  #         "--input_video {}  " \
  #         "--output_video {} " \
  #         "--train_dir {} --test_dir {}  " \
  #         "--use_ga_prediction {} " \
  #         "--use_emotion_prediction {} " \
  #         "--use_face_detection {} " \
  #         "--use_face_recognition {} " \
  #         "--use_scenes_change {} " \
  #         "--use_objects_detection {} " \
  #         "--n_classes {}".format(input_video, output_video, train_dir, test_dir, ga, emotion,
  #                                 face_detection, face_recognition, scenes_change, objects_detection, n_classes)

  cmd = "python /media/vy/DATA/projects/face/project3/Objects/main.py --input_video " + input_video
  cmd += "  --output_video "  + output_video
  if "Tru" in objects_detection:
    cmd += "  --use_objects_detection "  + objects_detection
  if "Tru" in face_detection:
    cmd += "  --use_face_detection " + face_detection
  if "Tru" in age:
    cmd += "  --use_age_prediction " + age
  if "Tru" in gender:
    cmd += "  --use_gender_prediction " + age
  if "Tru" in emotion:
    cmd += "  --use_emotion_prediction " + emotion
  if "Tru" in face_recognition:
    cmd += "  --use_face_recognition " + face_recognition
  if "Tru" in scenes_change:
    cmd += "  --use_scenes_change_count " + scenes_change
  cmd += "  --n_classes " + n_classes

  os.system(cmd)

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
    app.run(host="192.168.2.14", port=55555, debug=True)

