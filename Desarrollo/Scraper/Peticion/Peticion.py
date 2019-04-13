'''
Created on 9 may. 2018

@author: jairo

Descripcion: Esta clase se encarga de hacer la llamada a la web y devolver su respuesta
Metodos:
	-_set_url_proxy: Crea un opener con el proxy que se le pasa
	-_get_headers: Se encarga de crear un header para que la web piense que se hace una peticion desde un web browser normal
	-peticion: Una vez creado el opener y la cabecera, este metodo es el que realiza la peticion a la pagina
'''

import requests,random, socket,time,sys,pickle,ssl,io,gzip
from http.client import BadStatusLine
from bs4 import BeautifulSoup
from Peticion.Headers import Headers
from Proxy import Proxy

class Peticion:
	
	url = ""
	proxy = Proxy
	headers = ""
	status_code = ""
	html = ""
	sock = ""

	###################################################
	#                     PROXIES        		  #
	###################################################
	def get_proxy(self,log):
                host = socket.gethostbyname("localhost")
                port = 4999
                server_address=(host,port)
                #1.Inicializacion del socket
                if self.sock =="":
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #2.Conexion al puerto
                sock.connect((server_address))
                try:
                        print("Enviando: "+ str(self.proxy))
                        #3.Envio de peticion proxy
                        sock.sendall(pickle.dumps(self.proxy))
                        amount_received = 0
                        amount_expected = 1
                        while amount_received < amount_expected:
                                print("Recibiendo datos")
                                data=sock.recv(1024)
                                try:
                                        print(pickle.loads(data))
                                except Exception as e:
                                        print(e)
                                self.proxy = pickle.loads(data)
                                print("Proxy: "+str(self.proxy))
                                if len(str(self.proxy))> 0:
                                        amount_received +=1
                                else:
                                        amount_received = 0
                                print("Recibido: "+str(self.proxy.cadena)) 
                except Exception as e:
                        log.error("Clase: Peticion||Metodo: get_proxy||Error: "+str(e))
                        sys.exit()     
                finally:
                        sock.close()
                        return self.proxy
        ###################################################
	#                     PROXIES        		  #
	###################################################
	def get_url(self,url):
                self.url = url
                return self.url
	###################################################
	#                     CABECEREA     		  #
	###################################################
	def get_headers(self,url,log,browser="Random"):
                #1.Comprobamos si es http, https o ninguna
                if url.find("https://")> 0:
                        https = 1
                        http = 0
                        web =url[8:]
                elif url.find("http://")> 0 and url.find("https://")==0:
                        http = 1
                        https=0
                        web = url[7:]
                else:
                        http=0
                        https=0
                        web = url
                #2.Comprobamos si es .com ,.es o ninguna
                if url.find(".com")> 0:
                        com = 1
                        es= 0
                        web = web[0:web.find(".com")+4]
                elif url.find(".es")>0:
                        com = 0 
                        es = 1
                        web = web[0:web.find(".es")+4]
                else:
                        log.error("Clase: Peticion||Metodo: get_headers||Mensaje: La web elegida no cumple el formato correcto .com o .es.Por favor elija uno entre: .com, .es")
                        sys.exit()
                #Obtenemos el header correspondiente al buscador indicado
                headers = Headers(web,url,log)
                if browser =="Random":
                        headers = headers.Random
                elif browser =="Custom":
                        headers = headers.Custom  #Este es un generico que solo contiene el userAgent de Chrome para peticiones muy faciles
                elif browser =="Chrome":
                        headers = headers.Chrome
                elif browser =="Firefox":
                        headers = headers.Firefox
                elif browser =="Explorer":
                        headers  = headers.Explorer
                elif browser =="Safari":
                        headers = headers.Safari
                elif browser =="Opera":
                        headers = headers.Opera
                else:
                        log.error("Clase: Peticion||Metodo: get_headers||Mensaje: El browser elegido no existe.Por favor elija uno entre: Chrome, Firefox, Explorer, Safari, Opera, Custom, Random")
                        sys.exit()
                self.headers=headers
                return self.headers
	###################################################
	#                       REQUEST     	 	  #
	###################################################
	def peticion(self,log,scraper_id=None):
                if self.proxy is not None:
                        proxies = {"https": "http://%s"%(self.proxy.cadena)}
                else:
                        proxies = self.proxy
                try:
                        self.status=1
                        s = requests.Session()
                        req = requests.Request('GET',self.url,headers=self.headers)
                        prepped = req.prepare()
                        if proxies is None:
                                peticion = s.send(prepped,timeout=10)
                        else:
                                peticion = s.send(prepped,proxies=proxies,timeout=10)
                        return peticion
                except:
                        peticion = None
                return peticion

        ###################################################
	#   		     STATUS CODE	          #
	###################################################
	def get_status_code(self,peticion):
                if peticion is None:
                        self.status_code = 502 #De momento utilizo este codigo que significa error de proxy
                else:
                        self.status_code = peticion.status_code
                return self.status_code
	###################################################
	#	                HTML			  #
	###################################################
	def get_html(self,peticion):
                if self.status_code == 502:
                        self.html=None
                else:
                        try:
                                self.html = BeautifulSoup(peticion.content, "lxml")
                                peticion.close()
                        except:
                                self.html = None
                return self.html	
