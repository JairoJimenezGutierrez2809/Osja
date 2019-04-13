import sys 
sys.path.append('..')
from Log import Log
from Peticion import Peticion

if __name__=="__main__":
    log = Log.initialize("prueba")
    p = Peticion()
    url = "https://www.idealista.com"
    p.headers = p.get_headers(url,log)
    #for i in range(3):
    #    print("Entra:"+str(i))
    #    proxy = p.get_proxy(log)