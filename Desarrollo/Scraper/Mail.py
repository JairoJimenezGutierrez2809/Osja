# encoding=utf-8
#Importamos los paquetes necesarios
from email.mime.text import MIMEText
import smtplib
from datetime import datetime
import sys


class Email:

	#Metodo encargado de enviar un mail al usuario en caso de encontrar algun error en el codigo
	@classmethod
	def send(self,log,mensaje,scraper_name=None):
		#Datos de envio
		from_address = 'osja.scraper@gmail.com'
		to_address = ['jairo.jimenez@nfq.es']
		#'oscar.hernandez.pinchete@gmail.com'
		if scraper_name is None:
			subject = str(datetime.now())+'- Scraper_Not_Identified'
		else:
			subject = str(datetime.now())+'- Scraper '+scraper_name
		message = mensaje
		
		#Conversion MIME
		mime_message=MIMEText(message)
		mime_message["From"]= from_address
		mime_message["To"]= ", ".join(to_address)
		mime_message["Subject"]= subject
		
		#Conexion gmail
		try:
			smtp = smtplib.SMTP("smtp.gmail.com", 587)
			smtp.ehlo()
			smtp.starttls()
			smtp.login(from_address, "Administrador*")
		except Exception, e:
			log.error("Proceso: Email send||Mensaje:Conexion gmail fallida||Error:"+str(e))
			sys.exit()
		
		#Envio de mensaje
		try:
			smtp.sendmail(from_address, to_address, mime_message.as_string())
		except Exception, e:
			log.error("Proceso: Email send||Mensaje:Envio mail fallido||Error:"+str(e))
			sys.exit()
		#Cierre gmail
		smtp.quit()
