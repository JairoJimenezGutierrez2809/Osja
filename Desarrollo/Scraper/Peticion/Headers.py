#encoding: utf-8
#Esta clase contiene todos los web-browser que utiliza la aplicacion
import random
import sys
from Peticion.UserAgent import UserAgents

class Headers:
    
    ###########################
    #      INITIALIZATION     #
    ###########################
    def __init__(self,web,url,log):
        #UserAgents  
        self.userAgents=UserAgents(log)
        #Give value
        self._Firefox = self.getFirefox(web,log)
        self._Chrome = self.getChrome(web,url,log)
        self._Explorer = self.getExplorer(web,log)
        self._Safari = self.getSafari(log)
        self._Opera = self.getOpera(web,url,log)
        self._Custom = self.getCustom(log)
        self._Random = self.getRandom(web,url,log)
        

    ###########################
    #        PROPERTIES       #
    ###########################
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
    @property
    def Custom(self):
        return self._Custom
    @property
    def Random(self):
        return self._Random

    ###########################
    #          GETTERS        #
    ###########################
    #Define setters
    def getFirefox(self,web,log):
        userAgent = self.userAgents.Firefox
        headers = {'Accept':'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
				   'Accept-Encoding':'gzip, deflate, br',
				   'Accept-Language':'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
				   'Connection':'keep-alive',
				   'DNT':'1',
				   'Host':web,
				   'Upgrade-Insecure-Requests':'1',
				   'User-Agent': userAgent}
        
        return headers

    def getChrome(self,web,url,log):
        userAgent =self.userAgents.Chrome
        #path ya que en ocasiones te pide que indiques la direccion desde la que accedes a dicha url
        if len(url)<=25:
            path = url
        else:
            path = url[25:]
        #Header
        headers = {'authority': web,
                   'method': 'GET',
                   'path': path,
                   'scheme': 'https',
                   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'accept-encoding': 'gzip, deflate, br',
                   'accept-language': 'es-ES,es;q=0.9',
                   'cache-control': 'max-age=0',
                   'upgrade-insecure-requests': '1',
                   'User-Agent': userAgent}
        return headers
    
    def getExplorer(self,web,log):
        userAgent = self.userAgents.Explorer
        headers = {'Accept': '*/*',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'es-ES, es; q=0.8, en-US; q=0.5, en; q=0.3',
                   'Cache-Control': 'no-cache',
                   'Host': web,
                   'User-Agent': userAgent}
        return headers
    
    def getSafari(self,log):
        userAgent = self.userAgents.Safari
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'es-ES',
                   'User-Agent': userAgent}
        return headers
    
    def getOpera(self,web,url,log):
        userAgent = self.userAgents.Opera
        #path ya que en ocasiones te pide que indiques la direccion desde la que accedes a dicha url
        if len(url)<=25:
            path = url
        else:
            path = url[25:]
        headers = {'authority': web,
                   'method': 'GET',
                   'path': path,
                   'scheme': 'https',
                   'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'accept-encoding': 'gzip, deflate, br',
                   'accept-language': 'es-ES,es;q=0.9',
                   'cache-control': 'max-age=0',
                   'upgrade-insecure-requests': '1',
                   'User-Agent': userAgent}
        return headers

    def getCustom(self,log):
        userAgent = self.userAgents.Chrome
        headers = {'User-Agent': userAgent}
        return headers

    def getRandom(self,web,url,log):
        chrome= self.getChrome(web,url,log)
        firefox = self.getFirefox(web,log)
        explorer = self.getExplorer(web,log)
        safari = self.getSafari(log)
        opera = self.getOpera(web,url,log)
        headers = [chrome,firefox,explorer,safari,opera]
        headers = random.choice(headers)
        return headers
	
    ###########################
    #          SETTER         #
    ###########################
    def setFirefox(self,headers):
        self._Firefox = headers
    def setChrome(self,headers):
        self._Chrome = headers
    def setExplorer(self,headers):
        self._Explorer = headers
    def setSafari(self,headers):
        self._Safari = headers
    def setOpera(self,headers):
        self._Opera = headers
    def setCustom(self,headers):
        self._Custom = headers
    def setRandom(self,headers):
        self._Random = headers
    