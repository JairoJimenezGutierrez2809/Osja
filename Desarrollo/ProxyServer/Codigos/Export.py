#encoding: utf-8


'''
Created on 26 abr. 2018

@author: jairo

Descripcion: Esta clase se encarga de exportar los resultados obtenidos a un csv o un txt

'''
import pandas as pd
import numpy as np
import Import
import sys

def fichero(df,ruta,extension,log):
		#Exporto el dataFrame
		try:
			df.to_csv(ruta+"."+extension,index = True,header = True)
		except Exception as e:
			log.error("Proceso: Export fichero||Mensaje: Exportacion fichero fallida al crear||Error:"+str(e))
			sys.exit()	
	

#def fichero(lista,ruta,extension,modo,log):
#	try:
#		#Si el fichero existe, lo abro	
#		if extension =="csv":
#			output=io.open (('%s.%s' %(ruta,extension)) ,mode=modo,encoding="utf-8",newline='')
#			writer = csv.writer(output)
#		else:
#			output =open("%s.%s"%(ruta,extension),modo)
#		#Exporto linea a linea
#		if lista is not None:
#			if len(lista)==1:
#				writer.writerow(lista)
#			else:
#				for item in lista:
#					if item is not None:
#						if extension =="csv":
#							writer.writerow(item)
#						else:
#							output.write("%s\n"%item)
#					else:
#						continue
#		if extension =="txt":
#			output.close()
#	except Exception, e:
#		log.error("Proceso: Export fichero||Mensaje: Exportacion fichero fallida||Error:"+str(e))
#		sys.exit()