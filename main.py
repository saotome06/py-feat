import os
from flask import Flask, send_file
import torch
import matplotlib.pyplot as plt
from feat import Detector
from feat.utils.io import get_test_data_path
import cv2
from mtcnn.mtcnn import MTCNN
from deepface import DeepFace

app = Flask(__name__)

# 検出器の定義

@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello!"

@app.route("/goodbye")
def goodbye_world():
    name = os.environ.get("NAME", "World")
    return "Goodbye {}!".format(name)

@app.route("/image")
def image():
    # 検出器の定義
    detector = Detector()

    # 公式が用意した画像のパスを取得
    test_data_dir = get_test_data_path()
    single_face_img_path = os.path.join(test_data_dir, "single_face.jpg")

    # 画像を指定して表情認識を実行
    result = detector.detect_image(single_face_img_path)
    emotions_str = result.emotions.to_json()

    print(emotions_str)
    return emotions_str

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
