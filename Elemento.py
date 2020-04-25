#####################################
# Autor: Carlos Aguirre Vozmediano  #
# Version: 20-03-2019				#
# Descripcion: elementos a usar		#
#####################################

# Un elemento comun para todo
class Elemento():
	def __init__(self, x, y):
		self.__x = x
		self.__y = y
		
	def getX(self):
		return self.__x
	
	def getY(self):
		return self.__y
	
	def setX(self, x):
		self.__x = x
		
	def setY(self, y):
		self.__y = y
		
	def __str__(self):
		return "X: " + str(self.__x) + ", Y: " + str(self.__y)

# Representa un cuadro de la cuadricula
class Cuadrado(Elemento):
	def __init__(self, x, y, rectangulo):
		Elemento.__init__(self, x, y)
		self.__rectangulo = rectangulo
	
	def getRectangulo(self):
		return self.__rectangulo

# Representa la cabeza y la cola del protagonista
class Protagonista(Elemento):
	def __init__(self, x, y):
		Elemento.__init__(self, x, y)
		self.__xInicial = x
		self.__yInicial = y
		self.__direccion = 0
		self.__coleccionCola = []
		
	def reiniciarPosicion(self):
		Elemento.setX(self, self.__xInicial)
		Elemento.setY(self, self.__yInicial)
		self.setDireccion(0)
		self.__coleccionCola = []
		
	def getDireccion(self):
		return self.__direccion
	
	def setDireccion(self, direccion):
		self.__direccion = direccion
		
	def aumentarCola(self):
		self.__coleccionCola.append((-1, -1))
		
	def getCola(self):
		return self.__coleccionCola
		
	def actualizarCoordenadasCola(self):
		if len(self.__coleccionCola) >= 1:
			# El primer eslabon pende de la cabeza por lo que se trata por separado
			valorAnterior = self.__coleccionCola[0]
			self.__coleccionCola[0] = (Elemento.getX(self), Elemento.getY(self))
		
			# Los demas valores se actualizan en funcion del eslabon anterior
			valorActual = (0, 0)
			for i in range(1, len(self.__coleccionCola), 1):
				valorActual = self.__coleccionCola[i]
				self.__coleccionCola[i] = valorAnterior
				valorAnterior = valorActual

# Representa la comida
class Comida(Elemento):
	def __init__(self, x, y):
		Elemento.__init__(self, x, y)
		self.__comido = True
	
	def isComido(self):
		return self.__comido
		
	def setComido(self, valor):
		self.__comido = valor
