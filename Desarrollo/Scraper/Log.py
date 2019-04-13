import logging
import time

class Log:
    
    @classmethod
    def initialize(self,tipo,scraper_id=None):
        ruta = 'Logs'
        dia = time.strftime('%Y%m%d')  
        #Creacion del log     
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        #Creacion de file handler
        if scraper_id is None:
            fh = logging.FileHandler(ruta+'/'+dia+'_'+str(tipo)+'.log')
        else:
            fh = logging.FileHandler(ruta+'/'+dia+str(scraper_id)+"_"+str(tipo)+'.log')
        fh.setLevel(logging.DEBUG)
        #Creacion de console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        #Creacion de formato
        formatter = logging.Formatter('%(asctime)s||%(levelname)s||%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        #Adicion de handler al logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger
    
    @classmethod
    def close(self,log):
        x = list(log.handlers)
        for i in x:
            log.removeHandler(i)
            i.flush()
            i.close()
