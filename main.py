import os
from flask import Flask, request, jsonify
import torch
import matplotlib.pyplot as plt
from feat import Detector
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "/tmp"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 最大16MBのファイルサイズ制限

@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello!"

@app.route("/goodbye")
def goodbye_world():
    name = os.environ.get("NAME", "World")
    return "Goodbye {}!".format(name)

@app.route("/image", methods=["POST"])
def image():
    if "file" not in request.files:
        return "ファイルがありません", 400

    file = request.files["file"]
    if file.filename == "":
        return "選択されたファイルがありません", 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        
        # 検出器の定義
        detector = Detector()
        
        # 画像を指定して表情認識を実行
        result = detector.detect_image(filepath)
        emotions_str = result.emotions.to_json()

        # 一時ファイルを削除
        os.remove(filepath)

        print(emotions_str)
        return emotions_str, 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
