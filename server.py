
import os
from flask import Flask, render_template, request,redirect, url_for, jsonify
from load_pages import *
import subprocess as sp

app = Flask(__name__)

ranks = hashmap_pagerank()


@app.route("/")
def home():	
	return render_template('index.html')


@app.route("/verDocumento",methods=['GET'])
def verDocumento():
    nameDocument=request.args.get('documento')
    consulta=f"hadoop dfs -cat /input/{nameDocument}"
    #consulta=f"cat {nameDocument}"
    #print(f"consulta {consulta}")
    output = sp.getoutput(consulta)
    #print(f"output {output}")
    return output

@app.route("/search", methods=["POST"])        
def search():
	page_rank = {}

	words = request.form['busqueda']
	
	#print(f"recibido: '{words}'")

	words = words.lower().split()
	
	#Realizar busqueda
	response  = search_query(words)

	print(response)
	print("--------------------------")
	#lista almacenar resultados
	pagelist = []

	if not len(response):
		print("No encontro nada")
		return jsonify([])

	else:

		for lista in response:

			for page in lista[0]:

				if page in page_rank:
					
					page_rank[page][1] += ' '+lista[1]
				else:	
					page_rank[page] = [ranks[page], lista[1]]

		#if not len(page_rank):		
		#	return jsonify([])			
		page_rank = {}
		for k, v in sorted(page_rank.items(), reverse=True, key=lambda item: item[1][0]):
			page_rank[f"{k} ({v[0]})"]=f"{k}"


		#print(pagelist)
		#return jsonify(pagelist)
		return render_template("resultados.html",
			busqueda=words,
        	resultados=page_rank
        )
	#os.system('bash java.sh '+words)
	#print (response)

if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0', port=5000)
