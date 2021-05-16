import os

from flask import Flask, render_template, request, flash
from flask_uploads import IMAGES, UploadSet, configure_uploads

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'data/'
app.config['SECRET_KEY'] = os.urandom(24)
configure_uploads(app, photos)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        photos.save(request.files['photo'])
        flash('Photo saved successfully')
        return render_template('upload.html')
    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)