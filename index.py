import zlib
import json
from flask import Flask, request, Response, url_for, render_template, jsonify
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

app = Flask(__name__)

with app.test_request_context():
    url_for('static', filename='styles.css')

def obscure(data):
    return b64e(zlib.compress(data, 9))

def unobscure(obscured):
    return zlib.decompress(b64d(obscured))

def getLink(url, cuil, mail):
    oCuil = obscure(cuil)
    oMail = obscure(mail)
    return url+'?data='+oCuil+'&m='+oMail+'&utm_source=Email&utm_medium=Canales_Adquisicion'

@app.route('/api/links', methods=['POST'])
def links():
    # data = request.get_json()
    data = request.get_json()
    url = data['url']
    cuils = data['cuils'].split(',')
    emails = data['emails'].split(',')
    index = 0
    links = []
    for cuil in cuils:
        if len(emails) > 1:
            email = emails[index]
        else:
            email = emails[0]
            pass
        links.append(getLink(url, cuil, email))
        index += 1
        pass

    return jsonify({
        "links": links
    })

@app.route('/')
def index():
    return render_template('template.html')
