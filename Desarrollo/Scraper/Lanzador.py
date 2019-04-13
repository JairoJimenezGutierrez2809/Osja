from Log import Log
import os

class Lanzador:

    def __init__(self):
        #Info que se desea extraer
        web = "[Idealista]"
        transaccion="[Alquilar]"
        #transaccion ="[Comprar,Alquilar]"
        tipologia ="[Viviendas]"
        info = "[Inmuebles,Bancos]"
        #info="[Arbol,Inmuebles,Bancos,DetalleInmueble]"
             
        #Inicializacion del log
        log = Log.initialize("lanzador", web)
         
        #Ejecucion
        log.info("Mensaje: Lanzando...||Web:"+str(web)+"||Transaccion:"+str(transaccion)+"||Tipologia:"+str(tipologia)+"||Info:"+str(info))
        try:
            Log.close(log)
            os.system("python Orquestador.py %s %s %s %s"%(web,transaccion,tipologia,info))
        except Exception,e:
            log.error("Mensaje: El lanzador no ha funcionado||Error:"+str(e))
            Log.close(log)
               
            
Lanzador()
        