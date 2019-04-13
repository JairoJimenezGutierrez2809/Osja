#encoding: utf-8
import zipfile
from io import BytesIO
import sys
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np

class ssl24proxies:
    ficheroDf = pd.DataFrame(columns =['CADENA'])
    paginasDf = pd.DataFrame(columns =['PAGINA'])

    #######################################
    #          OBTENER FICHERO            #
    #######################################	
    @classmethod
    def obtenerFichero(self,paginasDiccionario,log):
        #Declaramos las variables necesarias
        url="http://www.sslproxies24.top"
	#Abrimos la pagina de proxies
        peticion = self.__peticionPagina(url,log)
	#Obtenemos el enlace de la pagina de descarga
        html = self.__htmlPagina(peticion,log)
        for j in range(0,3):
            #Obtenemos la pagina de enlace del fichero
            paginaEnlace = self.__obtenerPaginaEnlace(html,log,j)
            check=0
            #Comprobamos que no tenemos ya esa pagina
            for indice_fila,fila in paginasDiccionario.iterrows():
                try:
                    pagina=fila['PAGINA']
                except Exception as e:
                    log.error("Proceso: ssl24proxies obtenerFichero||Mensaje: Error decodificando paginaDiccionario a utf8||Error: "+str(e))
                if paginaEnlace == pagina:
                    check=1
            if check==1:
                continue
            #Si no la tenemos seguimos el proceso
            else:
                #En caso de obtener la pagina, la aÃ±adimos a la lista de utilizadas y aÃ±adimos la propiedad
                paginasDiccionario = paginasDiccionario.append({'PAGINA': paginaEnlace}, ignore_index=True)
                self.paginasDf = paginasDiccionario
                #Obtenemos la pagina de descarga del fichero
                paginaFichero = self.__obtenerPaginaFichero(paginaEnlace,log)
                if paginaFichero is None:
                    continue
                else:
                    #Obtenemos el descargable
                    zip = self.__obtenerZip(paginaEnlace,paginaFichero,log)
                    unzipedFile = self.__descomprimirZip(zip,log)
                    fic =self.__extraerFichero(unzipedFile,log)
                    self.__rellenarFichero(fic,log)
                    
        while self.ficheroDf.empty:
            log.info("Proceso: ssl24proxies obtenerFichero||Mensaje:Esperando a un nuevo fichero")
            time.sleep(60*10)
            self.ObtenerFichero(paginasDiccionario,log)
        return self.ficheroDf
                

    #######################################
    #             ABRIR PAGINA            #
    #######################################
    @classmethod
    def __peticionPagina(self,url,log):
        max_intentos = 3
        intento = 1
        peticion = requests.get(url,timeout=10)
        while peticion.status_code != 200:
            intento=intento+1
            if intento == max_intentos:
                log.error("Proceso: ssl24proxies peticionPagina||Mensaje: Se ha alcanzado el numero maximo de intentos intentando abrir la pagina")
                sys.exit()
            peticion = requests.get(url,timeout=10)
        return peticion
    #######################################
    #             HTML PAGINA             #
    #######################################
    @classmethod
    def __htmlPagina(self,peticion,log):
        try:
            html = BeautifulSoup(peticion.content, "lxml")
            peticion.close()
        except Exception as e:
            log.error("Proceso: ssl24proxies htmlPagina||Mensaje: No se puede obtener el html de la pagina")
            sys.exit()
        return html

    #######################################
    #             PAGINA ENLACE           #
    #######################################
    @classmethod
    def __obtenerPaginaEnlace(self,html,log,j):
        paginas=html.find_all('h3', {'class': 'post-title entry-title'})
        if paginas is None:
            log.error("Proceso: ssl24proxies obtenerPaginaEnlace||Mensaje: Error al obtener la lista de paginas de ssl24proxies.Puede que el elemento haya cambiado de nombre")
            sys.exit()
        else:
            try:
                paginaEnlace=paginas[j].find('a').get('href')
                if paginaEnlace is None:
                    log.error("Proceso: ssl24proxies obtenerPaginaEnlace||Mensaje: Error al obtener la pagina de enlace de ssl24proxies. Puede que el elemento haya cambiado||Error:"+str(e))
                    sys.exit()
            except Exception as e:
                log.error("Proceso: ssl24proxies obtenerPaginaEnlace||Mensaje: Error al obtener la pagina de enlace de ssl24proxies. Puede que el elemento haya cambiado||Error:"+str(e))
                sys.exit()
            return paginaEnlace

    #######################################
    #            PAGINA FICHERO           #
    #######################################	
    @classmethod
    def __obtenerPaginaFichero(self,paginaEnlace,log):
        if self.__obtenerPaginaEnlace is None:
            paginaFichero = None
            return paginaFichero
        else:
            #Abrimos la pagina de enlace
            peticion = self.__peticionPagina(paginaEnlace,log) 
            #Buscamos el enlace de descarga
            html=self.__htmlPagina(peticion,log)
            try:
                paginas=html.find('div',{'class': 'post-body entry-content'}).find_all('a')
            except Exception as e:
                log.error("Proceso: ssl24proxies obtenerPaginaFichero||Mensaje: Error al obtener la pagina 1 del fichero de ssl24proxies. Puede que el elemento haya cambiado||Pagina:"+str(self.paginaEnlace)+"||Error:"+str(e))
                sys.exit()

            if len(paginas)==1:
                paginas = None
                return paginas
            else:
                for pagina in paginas:
                    if pagina.get('href') is None:
                        continue
                    else:
                        #url=enlace.getattr('href')
                        url = pagina.get('href')
                        break
                paginaFichero = url
                peticion = self.__peticionPagina(paginaFichero,log)
                html = self.__htmlPagina(peticion,log)
                try:
                    pagina = html.find('a', {'id': 'download-url'})
                except Exception as e:
                    log.error("Proceso: ssl24proxies obtenerPaginaFichero||Mensaje: Error al obtener la pagina 2 del fichero de ssl24proxies. Puede que el elemento haya cambiado||Pagina:"+str(self.paginaEnlace)+"||Error:"+str(e))
                    sys.exit()
                #Obtengo la pagina del fichero
                paginaFichero = pagina.get('href')
                return paginaFichero


    #######################################
    #            OBTENER FICHERO          #
    #######################################
    @classmethod					
    def __obtenerZip(self,paginaEnlace,paginaFichero,log):
        if paginaFichero is None:
            fichero = None
            return fichero
        else:
            peticion=self.__peticionPagina(paginaFichero,log)
            try:
                zipped = peticion.content
            except Exception as e:
                log.error("Proceso: ssl24proxies obtenerZip||Mensaje:No se ha podido abrir el descargable||Pagina:"+str(paginaEnlace)+"||Error:"+str(e))
                sys.exit()
            return zipped

    #######################################
    #        DESCOMPRIMIR FICHERO         #
    #######################################
    @classmethod							
    def __descomprimirZip(self,zipped,log):
	#Descomprimimos el fichero y lo guardamos en la ruta que deseamos
        try:
            unzipedFile= zipfile.ZipFile(BytesIO(zipped), "r")
        except Exception as e:
            log.error("Proceso: ssl24proxies descomprimirZip||Mensaje:No se puede descomprimir el fichero de ssl24proxies||Pagina:"+str(paginaEnlace)+"||Error:"+str(e))	
            sys.exit()
        return unzipedFile
    #######################################
    #            EXTRAER FICHERO          #
    #######################################
    @classmethod
    def __extraerFichero(self,unzipedFile,log):
        try:
            fh =pd.read_csv(unzipedFile.open('ssl.txt'),names=['CADENA'])
            unzipedFile.close()
        except Exception as e:
            log.error("Proceso: ssl24proxies extraerFichero||Mensaje:No se puede extraer el fichero descompromido de ssl24proxies||Pagina:"+str(paginaEnlace)+"||Mensaje:"+str(e))
            sys.exit()
        return fh
    #######################################
    #            RELLENAR FICHERO         #
    #######################################
    @classmethod
    def __rellenarFichero(self,fic,log):
        try:
            self.ficheroDf = self.ficheroDf.append(fic,ignore_index=True)
        except Exception as e:
            log.error("Proceso: ssl24proxies rellenarFichero||Mensaje:No se puede rellenar el fichero descompromido de ssl24proxies||Pagina:"+str(paginaEnlace)+"||Mensaje:"+str(e))
            sys.exit()
