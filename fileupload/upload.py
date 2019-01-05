
import os
from flask import Blueprint, Flask, render_template, request
from werkzeug import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import base64
from flask_jwt_extended import jwt_required


appUpload = Blueprint('appUpload', 'appUpload', url_prefix='', template_folder='fileupload')

@appUpload.route('/upload')
def upload():
   return render_template('upload.html')
	
@appUpload.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join("uploads", secure_filename(f.filename)))
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully', 201

@appUpload.route('/uploadbase64', methods = ['GET', 'POST'])
@jwt_required
def uploadbase64():
   if request.method == 'POST':
      
      data = dict(request.form)
      print(data['name'][0])
      with open("uploads/{}".format(data['name'][0]), "wb") as fh:
         fh.write(base64.decodebytes(data['imageBase64'][0].encode()))

      return 'file uploaded successfully', 201