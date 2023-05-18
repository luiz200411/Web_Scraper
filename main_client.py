import requests
from sys import argv

def main(a, b, c, d):
	di = a
	df = b
	es = c
	mei = d

	#d

	r = requests.post("http://127.0.0.1:80/votbgjfuqrlgpzlogkxs", json={"dataini":di, "datafin":df, "es": es, "mei": mei})
	return 0
