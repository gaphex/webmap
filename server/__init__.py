# -*- coding: utf-8 -*-

import sys, traceback
import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    with open('banks.json', 'rb') as f:
		results = json.loads(f.read()) 
    return render_template('index.html', errors=[], results=results)

if __name__ == "__main__":
    app.run()