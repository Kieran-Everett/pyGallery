import os
from datetime import datetime

from flask import Flask, render_template, request, flash
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gallery.db'
db = SQLAlchemy(app)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/data/'
app.config['SECRET_KEY'] = os.urandom(24)
configure_uploads(app, photos)


class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picName = db.Column(db.String(100), nullable=False, unique=True)
    tags = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, default=datetime.utcnow)
    uploadedBy = db.Column(db.String(40))

    def __repr__(self):
        return '<Picture %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:

        # really fancy, saves the photo (adding a '_n' if file already exists) and returns the name of the photo... i should really read things before spending an hour trying to get the name of the file through other methods
        pic_picName = photos.save(request.files['photo'])
        pic_tags = "" # saved like a csv probably
        pic_uploadedBy = "testUser" # hardcoding stuff temporarily

        new_pic = Gallery(picName=pic_picName, tags=pic_tags, uploadedBy=pic_uploadedBy)

        try:
            db.session.add(new_pic)
            db.session.commit()
            flash('Photo saved successfully')
            return render_template('upload.html')
        except:
            flash('Photo upload failed')
            return render_template('upload.html')
        
    return render_template('upload.html')


@app.route('/dbView')
def dbView():
    gallery = Gallery.query.order_by(Gallery.id).all()
    return render_template('dbView.html', gallery=gallery)


if __name__ == "__main__":
    app.run(debug=True)