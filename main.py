from flask import *
import os
from core.Interfaces import tagProcess, jsonifyTagData

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/get_classes', methods=['get', 'post'])
def get_classes():
    tags = tagProcess('./models/COCO_classes_with_tag.json').process()
    data = jsonifyTagData(tags).action()
    return data


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
    app.run()
