from datetime import datetime
import os
import sys


class Limpieza:
    @classmethod
    def logs(self,path,log):
        date_format='%Y%m%d'
        fecha_actual= datetime.strptime(datetime.today().strftime('%Y%m%d'),date_format)
        #Eliminacion de los logs anteriores
        if len(os.listdir(path))>0:
            try:
                log.info("Proceso: Limpieza Logs||Mensaje: Borrando logs previos")
                for item in os.listdir(path):
                    fecha_fichero=datetime.strptime(datetime.strptime(item[0:8],'%Y%m%d').date().strftime('%Y%m%d'),date_format)
                    delta=fecha_actual-fecha_fichero
                    if delta.days > 2:
                        os.remove(path+"/"+item)
                log.info("Proceso: Limpieza Logs||Mensaje: Proceso de limpieza de logs completado")
            except Exception, e:
                log.error("Proceso: Limpieza Logs||Mensaje: Error realizando limpieza de logs||Error: "+str(e))
                sys.exit()
