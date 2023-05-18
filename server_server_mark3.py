from gevent import monkey; monkey.patch_all()
from bottle import route, run, template, static_file, post, get, request
from time import sleep
from scraper_server_mark3 import main
import os





@post("/votbgjfuqrlgpzlogkxs")
def api():
	dicio = request.json
	
	print(dicio)
	main(dicio['dataini'], dicio['datafin'], dicio['es'], dicio['mei'], com_email_func="Desativado", somente_nums=True, csv_ou_txt="txt",enviar_por_email=True)
	yield 0
	#yield os.system(f"python3 main-selenium-3.py {dicio['dataini']} {dicio['datafin']} {dicio['es']} {dicio['mei']}")
	



run(host='127.0.0.1', port=80, server="gevent")
