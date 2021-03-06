import logging
import time

    
def initialize():
    ruta = "../Logs"
    dia = time.strftime('%Y%m%d')
    #Creacion del log
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    #Creacion de file handler
    fh = logging.FileHandler(ruta+'/'+dia+'_Proxies.log')
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
    
def close(log):
    x = list(log.handlers)
    for i in x:
        log.removeHandler(i)
        i.flush()
        i.close()
