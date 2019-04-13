#encoding: utf-8
'''
Created on 9 may. 2018

@author: jairo

Descripcion: Esta clase es el orquestador y se encarga de crear los diferentes scrapers para extraer los datos y hacer una exportacion final agrupando la info obtenida de cada scraper
Este orquestador tambien se encarga de solicitar proxies nuevos cuando alguno se ha quemado o de cambiar su estado cuando ha terminado el multiproceso

PASAR EN LUGAR DE SCRAPER_ID -> SstrID como string y en caso de convertirlo a entero ya se soluciona el problema
'''
from datetime import datetime
import time
from multiprocessing import Process,Lock,Manager
from Log import Log
from Limpieza import Limpieza
from Proxies.Codigos.Proxies import Proxies
import Import
import sys
from Arbol.Codigos.Arbol import *

##########################################################
#                       FUNCIONES                        #
##########################################################
def Inmuebles(web,diccionario,lista_input,resultados,lock):
	scraper_name = getScraperName()
	log = Log.initialize(web,scraper_name)
	url_array = getURLArray(list_input,lock)



##########################################################
#                       VARIABLES                        #
##########################################################

#1.Info solicitada
info = [['Idealista','Comprar','Viviendas','Arbol']]#,
		#['Idealista','Comprar','Viviendas','Inmuebles'],
		#['Idealista','Comprar','Viviendas','Bancos'],
		#['Idealista','Alquilar','Viviendas','Arbol'],
		#['Idealista','Alquilar','Viviendas','Inmuebles'],
		#['Idealista','Alquilar','Viviendas','Inmuebles']]

#2.Rutas 
path_entrada='Entrada'
path_resultados='Resultados'
path_errores='Errores'
path_logs = 'Logs'

#4.Resto variables
log = Log.initialize("Orquestador")
fecha=time.strftime('%Y%m%d')
resultados=[]
n_scrapers=	1
scrapers_pool=[]

#######################################################################
#			        FUNCIONES                             #
#######################################################################
def lanzarScraper(web,item,url_base,diccionario,lista_input,resultados,lock):
	i=0 #Inicializo el contador a 0
	#En funcion del item, lanzamos un determinado scraper
	if item == 'Arbol':
		for i in range(n_scrapers):
			try:
				scraper=Process(name = 'Scraper-%s'%str(i),target=Arbol,args=(web,url_base,diccionario,lista_input,resultados,lock))
				scrapers_pool.append(scraper)	 
				scraper.start()
			except Exception, e:
				log.error("Proceso: Orquestador||Mensaje:Ha fallado la creacion del scraper para el item Arbol (Multiprocessing)||Error:"+str(e))
				sys.exit()
	elif item == 'Inmuebles' or item == 'Bancos':
		for i in range(n_scrapers):
			try:
				scraper=Process(name = 'Scraper-%s'%str(i),target=Inmuebles,args=(web,url_base,diccionario,lista_input,resultados,lock))
				scrapers_pool.append(scraper)	 
				scraper.start()
			except Exception, e:
				log.error("Proceso: Orquestador||Mensaje:Ha fallado la creacion del scraper para el item Arbol (Multiprocessing)||Error:"+str(e))
				sys.exit()
	
	
	while scrapers_pool:
		for scraper in scrapers_pool:
			if not scraper.is_alive():		
				scraper.join()
				scraper.terminate()
				scrapers_pool.remove(scraper)
				del(scraper)		
		

#######################################################################
#			        EJECUCION                             #
#######################################################################
if __name__=='__main__':
	#multiprocessing.freeze_support()
	manager=Manager()
	lock = Lock()
	hora_inicio = str(datetime.now().time())
	
	#1.Limpieza Logs
	Limpieza.logs(path_logs,log)
	diccionario = Proxies(log)
	#diccionario.importar(log)
	
	#2.Ejecucion del proceso
	for element in info:
		web=element[0]
                transaccion=element[1]
                tipologia =element[2]
                item = element[3]
		
		if web == 'Idealista':
			url_base ='https://www.idealista.com'
		elif web == 'Fotocasa':
			url_base = 'https://www.fotocasa.es'
		else:
			log.error("Proceso: Orquestador||Mensaje: La web indicada no existe||Error: "+str(e))
			sys.exit()
		
		#2.1 Nombramiento de fichero de entrada y salida
		if item == 'Arbol':
			fichero_input = path_entrada+"/"+web+transaccion+tipologia
			fichero_output =path_resultados+"/"+fecha+"_Resultados_"+web+"_"+transaccion+"_"+tipologia+"_"+item
		elif item == 'Inmuebles':
			fichero_input=path_entrada+"/"+fecha+"_arbol_"+web+"_"+transaccion+"_"+tipologia
			fichero_output =path_resultados+"/"+fecha+"_Resultados_"+web+"_"+transaccion+"_"+tipologia+"_"+item
		elif item == 'Bancos':
			fichero_input=path_entrada+"/"+fecha+"arbol_"+web+"_"+transaccion+"_"+tipologia+"_bancos"	
			fichero_output =path_resultados+"/"+fecha+"_Resultados_"+web+"_"+transaccion+"_"+tipologia+"_"+item
		else:
			log.error("Proceso: Orquestador||Mensaje: El item seleccionado no existe.Por favor selecciono entre [Arbol,Inmuebles,Bancos]")
			sys.exit()
		
			
		#2.2 Creacion de lista a partir del fichero importado y creacion de lista de salida
		lista_input = Import.fichero(fichero_input,"csv",log)
		lista_input = manager.list(lista_input)
		resultados = manager.list(resultados)
		
		#2.3 Lanzamiento multiproceso en funcion del item seleccionado
		lanzarScraper(web,item,url_base,diccionario,lista_input,resultados,lock)
