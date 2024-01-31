import os
import requests
import json
import cv2
from flask import Flask, flash, request, redirect, url_for, jsonify,render_template
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract


'''
#pytesseract.pytesseract.tesseract_cmd = r'd:\tesseract-ocr-setup-3.02.02.exe'

# Pytesseract code for extract
def ocr_core(filename):
    text = pytesseract.image_to_string(Image.open(filename))  
    return text

'''


UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','tif','tiff'])

app = Flask(__name__)

# function to check the file extension
def allowed_file(filename):  
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def fn2(filename):       
    img = cv2.imread(filename)
    height, width, _ = img.shape
    # REshaping image
    roi = img[0: height, 400: width]


    # Ocr
    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
    file_bytes = io.BytesIO(compressedimage)
    result = requests.post(url_api,
                files = {'filename': file_bytes},
                data = {"apikey": "K84366492888957",
                        "language": "eng"})
    result = result.content.decode()
    result = json.loads(result)

    parsed_results = result.get("ParsedResults")[0]
    text_detected = parsed_results.get("ParsedText")

    return (text_detected)

# test Home page
@app.route('/')
def home_page():  
    return render_template('index.html')


#  Upload function
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():  
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        

        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):

            # Outer fn OCR_core for extract the file 
            extracted_text = fn2(filename)

            return render_template('upload.html',
                                   msg='Successfully processed',
                                  extracted_text=extracted_text,
                                 img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')



if __name__ == '__main__':  
    app.run()

