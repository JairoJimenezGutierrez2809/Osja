#Proxy server
import socket,time,sys,pickle
from Scraper.ProxyServer.Codigos.Proxy import Proxy


class aplicacion():
        host = socket.gethostbyname("localhost")
        port = 4999
        server_address=(host,port)
        sock = None

        def __init__(self):
                #Inicializacion del socket
                if self.sock is None:
                        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                else:
                        self.sock = sock
		
		#Conexion al puerto
                self.connect()
                try:
                        message = 1
                        print("Enviando: "+ str(message))
                        mensaje = self.pickleObject(message)
                        self.send(mensaje)
                        amount_received = 0
                        amount_expected = 1
                        while amount_received < amount_expected:
                                print("Entra")
                                data = self.receive()
                                proxy = self.unpickleObject(data)
                                amount_received +=1
                                print("Recibido: "+str(proxy.cadena))
                        
                finally:
                        self.disconnect()
                        
        def connect(self):
                self.sock.connect((self.server_address))
        #Desconexion
        def disconnect(self):
                self.sock.close()
	#Metodo de envio
        def send(self,data):
                self.sock.sendall(data)
	#Metodo de recepcion
        def receive(self):
                return self.sock.recv(1024)
	#Pick Object
        def pickleObject(self,proxy):
                #Escribimos el objeto dentro del fileObject
                data = pickle.dumps(proxy)
                return data
			
	#Load Object
        def unpickleObject(self,data):
                #Cargamos el objeto en la variable proxy
                proxy = pickle.loads(data)
                print(proxy)
                return proxy

        
		
if __name__ =="__main__":
	aplicacion()
