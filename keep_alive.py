from flask import Flask
from threading import Thread
from flask_cors import CORS


app = Flask('')
CORS(app)

@app.route('/')
def home():
	return "Hello I'm alive!"

def run():
	app.run(host='0.0.0.0', port=8080, debug=True)

def keep_alive():
	t = Thread(target=run)
	t.start()