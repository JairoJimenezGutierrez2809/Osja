import multiprocessing
from Peticion.Peticion import Peticion,Headers
from multiprocessing import Process,Lock, Manager
from Log import Log
from ProxyServer.Codigos import Proxy


#def prueba(i,diccionario):
#	log=Log.initialize("prueba",i)
#	#print(diccionario.lista[0])
#	peticion = Peticion()
#	proxy = peticion.get_proxy(diccionario,log)
#	print(proxy.cadena)
def coger_proxy():
	log = Log.initialize("prueba")
	p = Peticion()
	#headers=Headers(log)
	p.proxy = p.get_proxy(log)
	print(p.proxy.cadena)
	
if __name__=="__main__":
	multiprocessing.freeze_support()
	lock = Lock()
	manager=Manager()
	scrapers_pool=[]

	for i in range(10):
		scraper=Process(name = 'prueba',target=coger_proxy)
		scrapers_pool.append(scraper)	 
		scraper.start()
		scraper.join()
		while scrapers_pool:
			for scraper in scrapers_pool:
				if not scraper.is_alive():		
					scraper.join()
					scraper.terminate()
					scrapers_pool.remove(scraper)
					del(scraper)



