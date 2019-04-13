# encoding: utf-8
'''
Created on 29 may. 2018

@author: jairo

Descripcion: Esta clase se encarga de realizar todas las importaciones de ficheros a la api
'''
import os.path as path
import io
import sys

def fichero(ruta,extension,log):
        lista=[]
        try:
                #Si el fichero existe, lo abro
                if path.exists(ruta+"."+extension):
                        #Si el fichero tiene extension csv
			if extension == "csv":
				fh=io.open(ruta+"."+extension,'r',encoding='utf-8')
                #Si el fichero tiene extension txt
                        else:
                                fh = io.open(ruta+"."+extension, 'r',encoding='utf-8').read().splitlines()
                #Para cada linea, aniadimos esta a la lista
                for line in fh:
			if line != "":
                                try:
					if extension == "csv":
						lista.append(line.strip().split(','))
                                        else:
                                                lista.append(line)
                                except Exception, e:
                                        log.error("Proceso: Import fichero||Mensaje:Error añadiendo linea del fichero||Linea:"+str(line)+"||Error:"+str(e))
                        else:
                                #si el fichero no existe, devuelvo la lista vacia
                                continue
                return lista
	except Exception, e:
		log.error("Proceso: Import fichero||Mensaje: Importacion fichero fallida||Error:"+str(e))    
		sys.exit()
