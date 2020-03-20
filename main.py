#!/usr/bin/env python3

from flask import *
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import cv2 as cv
import json
import shutil
import requests

# My sources
from core.Interfaces import tagProcess, jsonifyTagData, jsonifyData, getFilesFromRequest, getDataFromRequest, b64Process
from core.Detection import yoloIMG, YOLODetect, YOLOPreprocessWithTarget
from core.settings import Settings

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config['RESULT_FOLDER'] = './static/results'
app.config['RESULT_IMGS'] = './static/resultIMGS'

base = os.path.dirname(os.path.realpath(__file__))
anchors = os.path.join(base, './models/yolo_anchors.txt')
classes = os.path.join(base, './models/coco_classes.txt')
model = os.path.join(base, './models/yolov3_416.h5')

_config = None


# Seen pages
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/still_under_development')
def still_under_development():
    return render_template('stillUnderDevelopment.html')


@app.route('/processing')
def processing():
    percentage = request.cookies.get('percentage')
    print(percentage)
    return render_template('loading.html', percentage=percentage)


@app.route('/result')
def result():
    option = 'decode'
    processed = {}
    filename = request.cookies.get('filename')
    targetCount = request.cookies.get('targetCount')
    targetCount = b64Process(
        targetCount, option
    ).action()

    result = json.load(
        open(
            os.path.join(
                app.config['RESULT_FOLDER'],
                filename
            ), 'r'
        )
    )
    os.remove(
        os.path.join(
            app.config['RESULT_FOLDER'], filename
        )
    )
    for key in result.keys():
        processed[key] = key.replace(':', '-')

    return render_template('result.html', count=targetCount, filename=filename, durations=result, ids=processed)


# Temp data pages
@app.route('/percentage', methods=['GET', 'POST'])
def percentage():
    percentage = request.form['percentage']
    resp = make_response('abc')
    resp.set_cookie('percentage', percentage, domain='127.0.0.1')
    return resp


@app.route('/get_classes', methods=['get', 'post'])
def get_classes():
    tags = tagProcess('./models/COCO_classes_with_tag.json').process()
    data = jsonifyTagData(tags).action()
    return data


@app.route('/uploads', methods=['GET', 'POST'])
def uploads():
    global _config
    option = 'encode'
    file = getFilesFromRequest('files').action()

    filename = secure_filename(file.filename + "_" + str(datetime.today()))
    filename = b64Process(filename, option).action()
    filename = ''.join(chr(c) for c in filename)

    file.save(os.path.join(
        app.config['UPLOAD_FOLDER'],
        filename
    ))
    _config = getDataFromRequest().action()

    resp = make_response('ok')
    resp.set_cookie('filename', filename)

    for cfg, value in _config.items():
        resp.set_cookie(cfg, b64Process(value, option).action())

    return resp


@app.route('/configs')
def configs():
    global _config
    return jsonifyData(_config).action()


@app.route('/process')
def process():
    option = 'decode'
    filename = request.cookies.get('filename')
    frameSkip = b64Process(request.cookies.get('frameSkip'), option).action()
    target = b64Process(request.cookies.get('target'), option).action()

    detector = YOLODetect(model, anchors, classes)
    resp = make_response('ok')

    destination = os.path.join(
        app.config['RESULT_IMGS'],
        filename
    )
    os.mkdir(destination)

    start_predict = 0
    final = {}
    targetCount = 0

    rstJson = open(
        os.path.join(
            app.config['RESULT_FOLDER'], filename
        ), 'w+'
    )

    vid = cv.VideoCapture(
        os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        )
    )
    settings = Settings(vid)
    while not settings.current_frame() == settings.get_frames_count():
        ret, frame = vid.read()
        if not ret:
            continue
        if start_predict % int(frameSkip) == 0:
            duration = settings.get_current_SEC()
            settings.format_to_HMS(duration)
            duration = settings.duration

            frame = yoloIMG(frame).preprocess_to()

            _, box_count, predicted_classes = detector.detect(frame)

            frame = yoloIMG(frame).rollback()

            result = YOLOPreprocessWithTarget(
                [predicted_classes, box_count], duration,
                target
            ).process_outputs()
            final.update(result)

            targetCount += result[duration]['target']

            cv.imwrite(
                os.path.join(
                    destination, duration
                ) + '.jpg', frame
            )

        percentage = (settings.current_frame() / settings.get_frames_count()) * 100
        requests.post('http://127.0.0.1:8080/percentage', data={'percentage': int(percentage)})

        start_predict += 1

    option = 'encode'
    json.dump(final, rstJson)

    resp.set_cookie(
        'targetCount',
        b64Process(
            str(targetCount), option
        ).action()
    )

    return resp


# Cache clearer
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
