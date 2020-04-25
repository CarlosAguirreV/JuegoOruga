#####################################
# Autor: Carlos Aguirre Vozmediano  #
# Version: 21-03-2019				#
# Descripcion: clase principal		#
#####################################

# Importar librerias
import pygame, sys, random, time, Elemento, OperacionesArchivo
from pygame.locals import *

# Creditos
print("\nCreditos:\n - Juego programado por: Carlos Aguirre")
print(" - Fuente de texto: Kids - Copyright (c) 1992 Corel Corporation.")
print(" - Musica: Samba Isobel (Fragmento) - Kevin Mac Leod")
print("\nUn poco de historia:")
print("  El conocido juego de la serpiente nacio en 1976 bajo el nombre de")
print("  Blockade, desarrollado por la empresa Gremlin. La primera version")
print("  para ordenador la programo P. Trefonas en 1978, se dio a conocer")
print("  bajo el nombre de Worm (gusano). No fue hasta 1998 que se hizo")
print("  famoso a nivel internacional, puesto que los moviles Nokia traian")
print("  pregrabado de fabrica dicho juego. Convirtiendose con el tiempo")
print("  en todo un clasico.\n")

# Colores
colorAzul = (10,10,90)
colorAzulClaro = (100,100,190)
colorVerde = (100,190,100)
colorVerde2 = (60,100,60)
colorRojo = (190,100,100)
colorNegro = (0,0,0)
colorBlanco = (255,255,255)
colorGris = (155,155,155)

# Imagenes
imgCabeza = pygame.image.load("recursos/imgCabeza.png")
imgCuerpo = pygame.image.load("recursos/imgCuerpo.png")
imgComida = pygame.image.load("recursos/imgComida.png")
imgSuelo = pygame.image.load("recursos/imgSuelo.png")
imgAltOn = pygame.image.load("recursos/imgAltOn.png")
imgAltOff = pygame.image.load("recursos/imgAltOff.png")

class Juego():
	def __init__(self):
		# Elementos comunes
		self.__salir = False
		self.__vecesParaBorrarDatos = 10
		self.__puntuacion = 0
		self.__puntuacionAnterior = 0
		self.__controlGuardado = OperacionesArchivo.OperacionesArchivo()
		self.__skinOriginal = 0
		self.__musica = 1
		
		# Cargar datos anteriormente guardados (si los hay)
		if self.__controlGuardado.cargar():
			datos = self.__controlGuardado.getDatos()
			self.__puntuacionAnterior = datos[0]
			self.__skinOriginal = datos[1]
			self.__musica = datos[2]
		
		# De pygame
		pygame.init()
		self.__dimensionVentana = (500, 500)
		self.__crearVentana(self.__dimensionVentana)
		self.__fuenteTextoMini = pygame.font.Font("recursos/fntKidsn.ttf", 20)
		self.__fuenteTexto = pygame.font.Font("recursos/fntKidsn.ttf", 30)
		self.__fuenteTextoGrande = pygame.font.Font("recursos/fntKidsn.ttf", 50)
		pygame.mixer.music.load("recursos/sndSambaIsobel.ogg")
		self.sonidoMordisco = pygame.mixer.Sound("recursos/sndMordisco.ogg")
		
		self.__cuadrosCuadricula = 20
		self.__crearCuadrados()
		self.__protagonista = Elemento.Protagonista(10, 10)
		self.__comidaAleatoria = Elemento.Comida(-1, -1)
		self.__reloj = pygame.time.Clock()
		self.__empezar()

	def __crearVentana(self, dimensiones):
		"""Crea la ventana, le da un titulo y le pone un icono"""
		self.__ventana = pygame.display.set_mode(dimensiones)
		self.__ponerTituloVentana()
		pygame.mouse.set_visible(False)
		pygame.display.set_icon(pygame.image.load("recursos/imgIcono.png"))
	
	def __ponerTituloVentana(self):
		if self.__skinOriginal:
			pygame.display.set_caption("Juego de la serpiente")
		else:
			pygame.display.set_caption("Juego de la oruga")
	
	def __crearCuadrados(self):
		"""Aqui se crea cada cuadro de la cuadricula"""
		self.__coleccionCuadrados = []
		tamanioCuadrados = 20 # Pixeles
		margen = 40 # Margen superior e izquierdo en pixeles
		
		coordenadaX = margen
		coordenadaY = margen
		
		for y in range(0, self.__cuadrosCuadricula):
			for x in range(0, self.__cuadrosCuadricula):
				elemento = Elemento.Cuadrado(x, y, (coordenadaX, coordenadaY, tamanioCuadrados, tamanioCuadrados))
				self.__coleccionCuadrados.append(elemento)
				
				coordenadaX += tamanioCuadrados + 1
			
			coordenadaX = margen
			coordenadaY += tamanioCuadrados + 1
	
	def __empezar(self):
		"""Aqui se definen las acciones a realizar a cada vuelta de reloj"""
		# Musica
		if self.__musica:
			pygame.mixer.music.play(-1)
		
		# Bucle infinito
		while(not self.__salir):
			self.__eventos()
			self.__generarNuevaPosicionComida()
			self.__moverProtagonista()
			self.__comprobarColisiones()
			self.__refrescar()
			self.__reloj.tick(5) # Max 60
		
		# Guardar los posibles cambios como la musica o el skin
		self.__controlGuardado.guardar(self.__puntuacionAnterior, self.__skinOriginal, self.__musica)
		print("\n¡Hasta otra!")
		
		pygame.quit()
		sys.exit()
		
	def __eventos(self):
		"""Controla todos los eventos"""
		for evento in pygame.event.get():
			if evento.type == QUIT:
				self.__salir = True
			
			if evento.type == KEYDOWN:
				self.__definirDireccion(evento.key)
	
	def __definirDireccion(self, teclaPulsada):
		"""Define la direccion en la que se mueve el protagonista
		1 Arriba, 2 Abajo, 3 Izquierda, 4 Abajo y 0 Quieto"""
		direccionAnterior = self.__protagonista.getDireccion()
		cantidadEslabones = len(self.__protagonista.getCola())
		
		if teclaPulsada in (K_UP, K_w) and (not direccionAnterior == 2 or cantidadEslabones < 2):
			self.__protagonista.setDireccion(1)
			
		if teclaPulsada in (K_DOWN, K_s) and (not direccionAnterior == 1 or cantidadEslabones < 2):
			self.__protagonista.setDireccion(2)
			
		if teclaPulsada in (K_LEFT, K_a) and (not direccionAnterior == 4 or cantidadEslabones < 2):
			self.__protagonista.setDireccion(3)
			
		if teclaPulsada in (K_RIGHT, K_d) and (not direccionAnterior == 3 or cantidadEslabones < 2):
			self.__protagonista.setDireccion(4)
			
		if teclaPulsada == K_F1:
			self.__skinOriginal = 1
			self.__ponerTituloVentana()
			
		if teclaPulsada == K_F2:
			self.__skinOriginal = 0
			self.__ponerTituloVentana()
			
		if teclaPulsada == K_m:
			if self.__musica:
				self.__musica = 0
				pygame.mixer.music.stop()
			else:
				self.__musica = 1
				pygame.mixer.music.play(-1)
				
		if teclaPulsada == K_DELETE:
			if self.__vecesParaBorrarDatos > 1:
				self.__vecesParaBorrarDatos -= 1
				print("*Pulsa otras " + str(self.__vecesParaBorrarDatos) + " veces la tecla SUPR para borrar los datos guardados.")
			elif self.__vecesParaBorrarDatos <= 1:
				print("--DATOS BORRADOS--\n")
				self.__controlGuardado.borrar()
				self.__reiniciar()
				self.__puntuacionAnterior = 0
				self.__skinOriginal = 0
				self.__musica = 1
				pygame.mixer.music.play(-1)
				self.__ponerTituloVentana()
				self.__vecesParaBorrarDatos = 10
			
	def __moverProtagonista(self):
		"""Mueve al protagonista y la cola si la tiene"""
		# Actualiza todas las coordenadas de la cola
		self.__protagonista.actualizarCoordenadasCola()
		
		direccion = self.__protagonista.getDireccion()
		
		if direccion == 1: # Arriba
			self.__protagonista.setY(self.__protagonista.getY() - 1)
			
		elif direccion == 2: # Abajo
			self.__protagonista.setY(self.__protagonista.getY() + 1)
			
		elif direccion == 3: # Izquierda
			self.__protagonista.setX(self.__protagonista.getX() - 1)
			
		elif direccion == 4: # Derecha
			self.__protagonista.setX(self.__protagonista.getX() + 1)
	
	def __generarNuevaPosicionComida(self):
		"""Si la comida ha sido comida, se genera una nueva posicion"""
		if self.__comidaAleatoria.isComido():
			
			xCabeza = self.__protagonista.getX()
			yCabeza = self.__protagonista.getY()
			valorNuevo = (xCabeza, yCabeza)
			
			x, y = 0, 0
			# No me termina de gustar esta forma, revisala
			while valorNuevo == (xCabeza, yCabeza) or valorNuevo in self.__protagonista.getCola():
				x = random.randint(0, self.__cuadrosCuadricula - 1)
				y = random.randint(0, self.__cuadrosCuadricula - 1)
				valorNuevo = (x, y)
			
			self.__comidaAleatoria.setX(x)
			self.__comidaAleatoria.setY(y)
			self.__comidaAleatoria.setComido(False)
	
	def __comprobarColisiones(self):
		"""Comprueba si el protagonista ha colisionado con algo"""
		xProta = self.__protagonista.getX()
		yProta = self.__protagonista.getY()
		
		# Comprobar colisiones con los limites de la cuadricula
		if xProta < 0 or xProta > self.__cuadrosCuadricula - 1 or yProta < 0 or yProta > self.__cuadrosCuadricula - 1:
			self.__reiniciar()
			
		# Comprobar colisiones con la comida aleatoria
		if not self.__comidaAleatoria.isComido():
			if xProta == self.__comidaAleatoria.getX() and yProta == self.__comidaAleatoria.getY():
				if self.__musica:
					self.sonidoMordisco.play()
					
				self.__comidaAleatoria.setComido(True)
				self.__puntuacion += 10
				self.__protagonista.aumentarCola()
		
		# Comprobar si el protagonista se esta comiendo su propia cola
		if (self.__protagonista.getX(), self.__protagonista.getY()) in self.__protagonista.getCola():
			self.__reiniciar()
	
	def __reiniciar(self):
		"""Reinicia la posicion del protagonista y los puntos"""
		nuevoRecord = self.__puntuacion > self.__puntuacionAnterior
		if nuevoRecord:
			self.__controlGuardado.guardar(self.__puntuacion, self.__skinOriginal, self.__musica)
			self.__puntuacionAnterior = self.__puntuacion
			for i in range(0, 2):
				self.__refrescar(colorAzulClaro, True)
				time.sleep(0.5)
				self.__refrescar(colorRojo, True)
				time.sleep(0.5)
				self.__refrescar(colorVerde, True)
				time.sleep(0.5)
		else:
			self.__refrescar(colorAzulClaro)
			time.sleep(0.7)
			
		self.__protagonista.reiniciarPosicion()
		self.__comidaAleatoria.setComido(True)
		self.__puntuacion = 0
	
	def __refrescar(self, colorFondo = colorNegro, mensajeNuevoRecord = False):
		"""Pinta todo en pantalla"""
		# Pintar el fondo
		self.__ventana.fill(colorFondo)
		
		# Pintar los cuadros de la cuadricula
		for elemento in self.__coleccionCuadrados:
			xActual = elemento.getX()
			yActual = elemento.getY()
			
			# Pintar cabeza protagonista
			if xActual == self.__protagonista.getX() and yActual == self.__protagonista.getY():
				if self.__skinOriginal:
					pygame.draw.rect(self.__ventana, colorVerde, elemento.getRectangulo())
				else:
					self.__ventana.blit(imgCabeza, elemento.getRectangulo())
				continue
			
			# Pintar cola protagonista
			if ((xActual, yActual) in self.__protagonista.getCola()):
				if self.__skinOriginal:
					pygame.draw.rect(self.__ventana, colorVerde2, elemento.getRectangulo())
				else:
					self.__ventana.blit(imgCuerpo, elemento.getRectangulo())
				continue
			
			# Pintar comida
			if xActual == self.__comidaAleatoria.getX() and yActual == self.__comidaAleatoria.getY():
				if not self.__comidaAleatoria.isComido():
					if self.__skinOriginal:
						pygame.draw.rect(self.__ventana, colorRojo, elemento.getRectangulo())
					else:
						self.__ventana.blit(imgComida, elemento.getRectangulo())
					continue
			
			# Pintar cuadro normal
			if self.__skinOriginal:
				pygame.draw.rect(self.__ventana, colorAzul, elemento.getRectangulo())
			else:
				self.__ventana.blit(imgSuelo, elemento.getRectangulo())
		
		# Pintar puntuacion
		textoPuntuacion = self.__fuenteTexto.render("Puntuacion: " + str(self.__puntuacion), True, colorBlanco)
		self.__ventana.blit(textoPuntuacion, (10, 465))
		
		# Indicar que ponga F1 o F2
		textoPuntuacion = self.__fuenteTexto.render("F1/F2", True, colorGris)
		self.__ventana.blit(textoPuntuacion, (410, 465))
		
		# Pintar record anterior
		if self.__puntuacionAnterior > 0:
			textoPuntuacion = self.__fuenteTexto.render("Record: " + str(self.__puntuacionAnterior), True, colorGris)
			self.__ventana.blit(textoPuntuacion, (10, 5))
		
		# Si se ha batido el record, entonces muestra un mensaje
		if mensajeNuevoRecord:
			textoPuntuacion = self.__fuenteTextoGrande.render("¡NUEVO RECORD!", True, colorBlanco)
			self.__ventana.blit(textoPuntuacion, (40, 230))
		
		# Pintar icono y letra musica
		textoPuntuacion = self.__fuenteTextoMini.render("M", True, colorGris)
		self.__ventana.blit(textoPuntuacion, (474, 53))
		if(self.__musica):
			self.__ventana.blit(imgAltOn, (465, 20))
		else:
			self.__ventana.blit(imgAltOff, (465, 20))
		
		# Actualizar toda la ventana
		pygame.display.update()
	
	
	
# Llamar al juego para que empiece.
Juego()
