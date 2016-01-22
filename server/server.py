# -*- coding: utf-8 -*-

import sys, traceback
import json
import os
import threading
import time
from flask import Flask, render_template, request

app = Flask(__name__)

results = None
results_time = 0

def update_results():
	global results, results_time
	if time.time() - results_time >= 60*15:
		with open('banks.json', 'rb') as f:
			results = json.load(f)
		results_time = time.time()

@app.route('/')
def index():
	update_results()
	return render_template('index.html', errors=[], results=results)
	
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1488)