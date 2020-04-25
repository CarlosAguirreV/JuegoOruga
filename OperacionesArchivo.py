#####################################
# Autor: Carlos Aguirre Vozmediano  #
# Version: 21-03-2019				#
# Descripcion: guardar y cargar 	#
#####################################

class OperacionesArchivo():
	def __init__(self):
		self.__nombreArchivo = "oruga.sav"
		self.__record = 0
		self.__skin = 0
		self.__musica = 1

	def guardar(self, record, skin, musica):
		cadenaRecord = str(format(record, '#04X')) + "\n"
		cadenaSkin = str(format(skin, '#04X')) + "\n"
		cadenaMusica = str(format(musica, '#04X'))
	
		try:
			archivo = open(self.__nombreArchivo, "w")
			archivo.write(cadenaRecord)
			archivo.write(cadenaSkin)
			archivo.write(cadenaMusica)
			archivo.close()
			return True

		except:
			print("*No se ha podido guardar en el archivo " + self.__nombreArchivo)
			return False

	def cargar(self):
		try:
			archivo = open(self.__nombreArchivo, "r")
			self.__record = int(archivo.readline()[0:-1], 16)
			self.__skin = int(archivo.readline()[0:-1], 16)
			self.__musica = int(archivo.readline(), 16)
			# El [0:-1] omite el ultimo caracter de la
			# linea que corresponde al salto de linea.
			
			archivo.close()
			return True

		except:
			print("*No se han encontrado datos de guardado")
			return False
			
	def borrar(self):
		try:
			archivo = open(self.__nombreArchivo, "w")
			archivo.write("")
			archivo.close()
		except:
			print("*No se ha podido borrar")
		

	def getDatos(self):
		return (self.__record, self.__skin, self.__musica)
		
