# encoding=utf-8
'''
Created on 29 may. 2018

@author: jairo

Descripcion: Esta clase se encarga de realizar todas las importaciones de ficheros a la api
'''
import pandas as pd
import sys

def fichero(ruta,log):
        try:
                df = pd.read_csv(ruta,sep = ",",names=["Browser","UserAgent"],encoding = 'utf-8')
                return df
        except Exception as e:
                log.error("Metodo: Importar||Mensaje: Importacion fichero fallida||Error:"+str(e))    
                sys.exit()  
