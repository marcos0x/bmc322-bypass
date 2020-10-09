import zlib
import json
from flask import Flask, request, Response, url_for, render_template, jsonify
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from werkzeug._compat import to_bytes

app = Flask(__name__)

def obscure(dataStr):
    return b64e(zlib.compress(str(dataStr), 9))

def getLink(url, cuil, mail):
    oCuil = obscure(cuil)
    oMail = obscure(mail)
    return url+'?data='+oCuil+'&m='+oMail+'&utm_source=Email&utm_medium=Canales_Adquisicion'

@app.route('/api/links', methods=['POST'])
def links():
    data = request.get_json()
    url = 'https://stg-bmc322.globant.com/tramiteonline/eresumen/'
    cuils = data['cuils'].split(',')
    emails = data['emails'].split(',')
    index = 0
    links = []

    if data['url']:
        url = data['url']

    for cuil in cuils:
        if cuil:
            email = emails[0]

            if len(emails) > 1 and emails[index]:
                email = emails[index]

            links.append(getLink(url, cuil, email))
        index += 1

    return jsonify({ "links": links })

@app.route('/')
def home():
    return render_template('home.html')
