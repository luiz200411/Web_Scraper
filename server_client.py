from gevent import monkey; monkey.patch_all()
from bottle import route, run, template, static_file, post, get, request
import os
from main_client import main


@get('/')
def index():
	#i

	yield static_file("index.html", root="")

@post("/api")
def api():
	dicio = request.json
	main(dicio['dataini'], dicio['datafin'], dicio['es'], dicio['mei'])
	yield 0
	#yield os.system(f"py main_a.py {dicio['dataini']} {dicio['datafin']} {dicio['es']} {dicio['mei']}")


run(host='127.0.0.1', port=8080, server="gevent", debug=True)
