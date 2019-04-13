#encoding: utf-8
'''
Created on 26 abr. 2018
@author: jairo
'''
import Log,socket,sys,Import,Export,os,pickle
from datetime import datetime
from time import time
from Proxy import Proxy
from ssl24proxies import ssl24proxies
import pandas as pd
import numpy as np

class ProxyProvider:
    host = socket.gethostbyname("localhost")
    port = 4999
    server_address=(host,port)
    sock = None    
		
    @classmethod
    def __init__(self,log):
        fecha=str(datetime.today().strftime('%Y%m%d'))
        ruta="../ProxiesList/"+fecha
        ruta_proxies =ruta+"/"+fecha+"_listaProxies"
        ruta_paginas=ruta+"/"+fecha+"_paginasProxies"
        #0.Declaracion de variables
        extension = "csv"
		
	#1.Importamos el DataFrame de proxies
        if os.path.exists(ruta)==False:
            log.info("Proceso: ProxyProvider init||Mensaje: inicializando lista proxies")
            self.proxyDf = pd.DataFrame(columns=['CADENA','ESTADO','SITUACION'])
            self.paginasDf = pd.DataFrame(columns = ['PAGINA'])
            self.importar(ruta,ruta_proxies,ruta_paginas,log)
            log.info("Proceso: ProxyProvider init||Mensaje: Lista proxies inicializada")
        else:
            log.info("Proceso: Proxies init||Mensaje: inicializando lista proxies")
            self.proxyDf = Import.fichero(ruta_proxies,extension,log)
            self.paginasDf = Import.fichero(ruta_paginas,extension,log)
            log.info("Proceso: ProxyProvider init||Mensaje: Lista proxies inicializada")
		
	#2.Inicializacion del socket
        self.socketInitialize(log)
		
	#3.Conexion al puerto
        self.connect(log)
		
	#4.Listening
        self.listen(1,log) #una conexion de momento
        while True:
            #Wait for a connection
            connection, client_address =self.sock.accept()
            try:
                data = self.receive(connection)
                p = self.unpickleObject(data,log)
                if p.cadena == "":
                    proxy = None
                else:
                    proxy = p
                proxy = self.darProxy(ruta,ruta_proxies,ruta_paginas,log,proxy)
                data = self.pickleObject(proxy,log)
                self.send(connection,data,log)
            finally:
                self.disconnect(connection,log)	
	
    ########################################
    #         IMPORTAR DICCIONARIO         #
    ########################################
    @classmethod
    def importar(self,ruta,ruta_proxies,ruta_paginas,log):
        #Importamos la lista
        log.info("Proceso: ProxyProvider importar||Mensaje: Importando fichero proxies")
        fichero = ssl24proxies.obtenerFichero(self.paginasDf,log)

	#Añadimos a esta lista las nuevas columnas de estado y situacion
        fichero['ESTADO'] = Proxy.Estado.no_uso
        fichero['SITUACION']=Proxy.Situacion.nuevo
        #Añadimos a esta lista a la que tenemos
        self.proxyDf = fichero
        #Añadimos la lista de paginas al dataframe que tenemos
        self.paginasDf = ssl24proxies.paginasDf
        #Exportamos la nueva lista
        self.exportar(ruta,ruta_proxies,ruta_paginas,log)
        log.info("Proceso: ProxyProvider importar||Mensaje: Proceso de importacion finalizado")
	
    ########################################
    #         EXPORTAR DICCIONARIO         #
    ########################################
    @classmethod
    def exportar(self,ruta,ruta_proxies,ruta_paginas,log):
        extension = "csv"
        if os.path.exists(ruta)==False:
            os.makedirs(ruta)

        Export.fichero(self.proxyDf, ruta_proxies, extension, log)
        Export.fichero(self.paginasDf, ruta_paginas, extension, log)
		
    ########################################
    #                DAR PROXY             #
    ########################################
    @classmethod
    def darProxy(self,ruta,ruta_proxies,ruta_paginas,log,proxy=None):
	#Si tenemos un proxy que actualizar, lo actualizamos
        if proxy is not None:
            self.updateProxyList(proxy,log)
            #Si terminamos con el proxy, lo liberamos
            if proxy.situacion == proxy.Situacion.nuevo:
                return
	#En caso de que el proxy estuviese quemado o que no tengamos todavía proxy, elegimos uno nuevo
        proxy = self.newProxy(log)
        while proxy is None:
            self.importar(ruta,ruta_proxies,ruta_paginas,log)
            proxy = self.newProxy(log)
        return proxy
		
    ########################################
    #          ACTUALIZAR PROXYLIST        #
    ########################################
    #Actualiza el objeto Proxy y la lista
    @classmethod
    def updateProxyList(self,proxy,log):
        for indice_fila,fila in self.proxyDf.iterrows():
            if indice_fila == proxy.id:
                fila['CADENA'] = proxy.cadena
                fila['ESTADO'] = proxy.estado
                fila['SITUACION'] = proxy.situacion
                if fila['SITUACION'] == Proxy.Situacion.quemado:
                    self.proxyDf.append({'CADENA': fila['CADENA'],'ESTADO':fila['ESTADO'],'SITUACION':fila['SITUACION']},ignore_index=True)
                    self.proxyDf.delete(indice_fila)
                    return
                else:
                    return
            else:
                return
	
    ########################################
    #               NUEVO PROXY            #
    ########################################
    @classmethod
    def newProxy(self,log):
        proxy=Proxy()
        i=0     #Contador de proxies vivos
        for indice_fila,fila in self.proxyDf.iterrows():
            if fila['ESTADO'] == Proxy.Estado.no_uso and fila['SITUACION']==Proxy.Situacion.nuevo:
                i=i+1
                proxy.id = indice_fila
                proxy.cadena = fila['CADENA']
                proxy.estado = fila['ESTADO']
                proxy.situacion = fila['SITUACION']
                fila['ESTADO'] = Proxy.Estado.uso
                fila['SITUACION'] = Proxy.Situacion.nuevo
                return proxy
            else:
                continue
        #Si no hay proxis vivos, no devolvemos nada
        if i==0:
            return None
			
    ########################################
    #           INITIALIZE SOCKET          #
    ########################################
    @classmethod
    def socketInitialize(self,log):
        try:
            if self.sock is None:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            log.error("Clase: ProxyProvider||Metodo: socketInitialize||Mensaje: Error inicializando el socket||Error: "+str(e))
            sys.exit()
			
    ########################################
    #                 LISTENER             #
    ########################################
    @classmethod
    def listen(self,n_connections,log):
        try:
            self.sock.listen(n_connections)
        except Exception as e:
            log.error("Clase: ProxyProvider||Metodo: listen||Mensaje: Error intentando escuchar del puerto||Error: "+str(e))
            sys.exit()
			
    ########################################
    #                CONNECTION            #
    ########################################
    @classmethod
    def connect(self,log):
        try:
            self.sock.bind((self.server_address))
        except Exception as e:
            log.error("Clase: ProxyProvider||Metodo: connect||Mensaje: Error creando conexion||Error: "+str(e))
            sys.exit()
			
    ########################################
    #              DISCONNECTION           #
    ########################################
    @classmethod
    def disconnect(self,connection,log):
        try:
            connection.close()
        except Exception as e:
            log.error("Clase: ProxyProvider||Metodo: disconnect||Mensaje: Error cerrando conexion||Error: "+str(e))
            sys.exit()
			
    ########################################
    #                  SENDER              #
    ########################################
    @classmethod
    def send(self,connection,data,log):
        try:
            print(data)
            connection.sendall(data)
        except Exception as e:
            log.error("Clase: ProxyProvider||Metodo: send||Mensaje: Error enviando informacion||Error: "+str(e))
            sys.exit()
			
    ########################################
    #                 RECEIVER             #
    ########################################
    @classmethod
    def receive(self,connection):
        try:
            return connection.recv(1024)
        except Exception as e:
            log.error("Clase: ProxyProvider||Metodo: receive||Mensaje: Error recibiendo informacion||Error: "+str(e))
            sys.exit()
	    
    ########################################
    #                PICK OBJETO           #
    ########################################
    @classmethod
    def pickleObject(self,proxy,log):
        try:
            #Escribimos el objeto dentro del fileObject
            data = pickle.dumps(proxy)
            return data
        except Exception as e:
            log.error("Clase: ProxyProvider||Metodo: pickleObject||Mensaje: Error creando objeto pickle||Error: "+str(e))
            sys.exit()
			
    ########################################
    #                LOAD OBJETO           #
    ########################################
    @classmethod
    def unpickleObject(self,data,log):
        try:
            #Cargamos el objeto en la variable proxy
            proxy = pickle.loads(data)
            print(proxy)
            return proxy
        except Exception as e:
            log.error("Clase: ProxyProvider||Metodo: unpickleObject||Mensaje: Error obteniendo objeto pickle||Error: "+str(e))
            sys.exit()



if __name__=='__main__':
    log = Log.initialize()
    provider = ProxyProvider(log)
