#FROM python:3
FROM --platform=linux/arm64 python:3.11.1  AS arm64
#FROM --platform=linux/amd64 python:3.11.1-alpine AS amd64
# use python:3.11.0rc2-slim for less vulnerabilities ? (from `docker scan`)
# use python:3.8.6 for no pip dependencies build errors ?
# use python:alpine for reduced size
# => python:3.8.6-alpine

WORKDIR /usr/src/SoundBoxBot

RUN python3 -m pip install --upgrade pip

COPY requirements.txt ./
#RUN pip3 install --extra-index-url https://alpine-wheels.github.io/index --no-cache-dir -r requirements.txt # if wheels dependencies build errors when using alpine
#RUN pip3 install --no-cache-dir -r requirements.txt    # because PyNaCl wheel build is very very long?
RUN pip3 install -r requirements.txt
RUN apt update && apt install ffmpeg -y
COPY . .

CMD [ "python", "./main.py" ]
