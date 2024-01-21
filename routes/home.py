from flask import render_template, Blueprint, session, redirect, url_for, jsonify, request, render_template_string
from static.python.paths import files as file, routes as route
import requests, uuid, json

import sqlite3

home = Blueprint('home', __name__)

############################# Home Home #############################


@home.route(route['home'])
def home_home():
    if "bid" in session:
        return render_template(file['home'])
    else:
        return redirect(url_for('auth.login'))
    
############################# Home Home #############################


@home.route(route['bankInfo'])
def bankInfo():
    if "bid" in session:
        try:
            conn = sqlite3.connect(file['db'])
            cursor = conn.cursor()
            bankDetailsQuery = "SELECT * FROM bank"
            transactionsDetailsQuery = "SELECT * FROM transactions ORDER BY tid DESC"
            bankDetails = cursor.execute(bankDetailsQuery).fetchall()[0]
            transactionsDetails = cursor.execute(transactionsDetailsQuery).fetchall()


        except Exception as e:
            print(e)
        finally:
            conn.close()


        return render_template(file['bankInfo'], bankDetails=bankDetails, transactionsDetails=transactionsDetails)
    else:
        return redirect(url_for('auth.login'))


############################# Macro #############################
@home.route(route['macro'], methods=['POST'])
def render_macro():
    data = request.json['data']
    rendered_macro = render_template_string(
        '{% from "macros.html" import customer %}{{ customer(data) }}', data=data)
    return jsonify({'html': rendered_macro})


############################ Temp ############################
@home.route("/temp")
def temp():
    return render_template("temp.html")




############################# Customer Short Info #############################
@home.route('/translate', methods=['GET', 'POST'])
def translate():
    data = request.json['data']
    key = "dc91f0fe80224b99b4a602afe488255d"
    endpoint = "https://api.cognitive.microsofttranslator.com"
    location = "centralindia"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': 'hi'
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': data
    }]

    req = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = req.json()
    
    ttext = response[0]['translations'][0]['text']
    return jsonify(ttext)