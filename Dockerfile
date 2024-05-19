FROM python:3.9-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    pkg-config \
    libhdf5-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# OpenCVをインストール
RUN apt-get update && apt-get install -y libopencv-dev python3-opencv

RUN pip install tensorflow

RUN pip install tf-keras

# MTCNNをインストール
RUN pip install mtcnn

# DeepFaceをインストール
RUN pip install deepface

RUN pip install --no-cache-dir Flask gunicorn matplotlib py-feat

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
