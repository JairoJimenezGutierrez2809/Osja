import random
import Peticion.Importar as Importar
import sys
from os import listdir


class UserAgents:

 ###################################################
  #                  INITIALIZATION            	  #
  ###################################################
	def __init__(self,log):
		#userAgentList
		ruta ="Peticion/UserAgentList/UserAgents.csv"  #Path of UserAgents
		#Initialize
		firefox = "Firefox"
		chrome = "Chrome"
		explorer = "Explorer"
		safari = "Safari"
		opera = "Opera"
		#Give value
		self.userAgentDf = self.load(ruta,log)
		self._Firefox = self.getUserAgent(firefox,log)
		self._Chrome = self.getUserAgent(chrome,log)
		self._Explorer = self.getUserAgent(explorer,log)
		self._Safari = self.getUserAgent(safari,log)
		self._Opera = self.getUserAgent(opera,log)
	
  ###################################################
  #                    PROPERTIES              	  #
  ###################################################
  #Define properties
	@property
	def Firefox(self):
		return self._Firefox
	@property
	def Chrome(self):
		return self._Chrome
	@property
	def Explorer(self):
		return self._Explorer
	@property
	def Safari(self):
		return self._Safari
	@property
	def Opera(self):
		return self._Opera
  ###################################################
  #                      SETTERS              	  #
  ###################################################
	#Define setters
	def setFirefox(self,userAgent):
		self._Firefox = userAgent
	def setChrome(self,userAgent):
		self._Chrome = userAgent
	def setExplorer(self,userAgent):
		self._Explorer = userAgent
	def setSafari(self,userAgent):
		self._Safari = userAgent
	def setOpera(self,userAgent):
		self._Opera = userAgent

  ###################################################
  #                LOAD USERAGENT LIST         	  #
	###################################################
	def load(self,ruta,log):
		try:
			df = Importar.fichero(ruta,log)
			return df
		except Exception as e:
			log.error("Clase: UserAgent||Metodo: load||Error: "+str(e))
			sys.exit()

  ###################################################
  #                  GET USERAGENT                  #
  ###################################################
	def getUserAgent(self,browser,log):
		#Seleccionamos en primer lugar únicamente aquellas filas donde este nuestro buscador
		try:
			BrowserDf=self.userAgentDf.loc[self.userAgentDf['Browser'] == browser]
			#Vemos el numero de filas obtenidas y seleccionamos una fila al azar
			n_filas = len(BrowserDf.index)
			filaRandom = random.randint(1,n_filas)
			userAgent = BrowserDf.iloc[filaRandom-1,1]
			return userAgent
		except Exception as e:
				log.error("Clase: UserAgent||Metodo: getUserAgent||Error: "+str(e))
				sys.exit()
