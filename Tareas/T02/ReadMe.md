# Bienvenido a Pandemic.py

Pandemic es un juego lineal en el cual se le otorgara la posibilidad al usuario 
continuarlouna vez abandonada la partida.

El juego conciste en asesinar humanitariamente el mundo con la expansion de
una enfermedad que extrañamente aumenta su tasa de mortalidad, a medida que 
pasan los dias.

1 Funcionamiento General:
El juego se organiza en varios menus, los cuales dan las opciones posibles
explicitamente.Por lo cual el usuario deberera escribir el simbolo ubicado
antes del punto y luego presionar enter para hacer efectiva su respuesta

1.0 Enfermedad
	Al momento de iniciar una nueva partida el juego le solicitara seleccionar
	su arma de destruccion masiva las cuales son:
		
		- Bacteria: enfermedad que no destaca en nada pero no posee grandes
			deventajas al mismo tiempo.
			
		- Virus: enfermedad de rapida expansion, una mortalidad inquietante,
			gran resistencia a la medicina y muy sutil.
			
		-Parasito: enefermedad con baja contagiosidad, mortalidad extrema y
			casi indetectable.

1.1 Inicio
Una vez inicana una partida el usuario dispondra de 4 opciones:
	-"Pasar dia" la cual genera un avanze en el horizonte temporal del juego.
	-"Estadisticas" este menu permitara al usuario obtener informacion visual
		de la pandemia en curso.
	-"Guardar" al seleccionar esta accion todos los componentes del juego se
		guardaran en la carpeta 'current' del directorio del juego.
	-"Salir" al igual que todos lo menus del juego esta opcion simplemente
		expulsa al jugador del menu actual (En el menu principal lo destierra).

1.2 Pasar dia

Al momento que el todopoderoso jugador selecciona esta opcion, todo el mundo una
vez congelado en el tiempo vuelve a moverce un dia en el futuro.

Al ocurrir este acontecimiento en el mundo pueden ocurrir los siguientes eventos:
	-Infeccion de 0 a 6 personas por infectado en un pais.
	-Muerte de personas en un pais basados en una probabilidad.
	-Expansion de la enfermedad por vias de comunicacion abiertas.
	-3 acciones correctivas por parte de los gobiernos
	-Descubrimiento de la enfermedad
	-Descubrimiento de la cura
	-Sanacion de los infectados
	-etc...
	
Todo acontecimiento se podra ver diarimente en el apartado "Estadisticas".
El los porcentajes de limpios, infectados o muertos se mostraran diarimente
junto a una barra de progreso.

1.3 Estadisticas

Este menu son los sentidos del jugador en el juego, ya que perimiten ver en
aspecto global la informacion mas importante:

	-"Por pais": Permite escribir un pais y saber sus estadisticas actuales o
		las acciones que el pais propondra en el dia actual.
		
	-"Mundo": Despliega una lista de paises a pedido.
	
	-"Tasas": muestra la informacion de infectados y muertos desde el dia 0
		ademas muestra el promedio de muertes e infecciones por dia
		
	-"Sucesos": Muestra el resumen diario almacenado en "sucesos.txt"

1.4 Ganar o perder
	
	El juego se gana al exterminar a todo ser humano del planeta, por
	contraparte el juego se perdera si no quedan infectados en el mundo
	
2. Funcionamientos Internos relevantes:
	
2.1 Guardar y cargar:

	Cada clase que almacena informacion importante posee un metodo guardar,
	el cual toma una caracteristica importante del objeto para asignarle
	un nombre y lo guarda en la carpeta "current".
	
	Por otro lado, todos los objetos cargan de la manera inversa a la que 
	fueron guardados.
	
2.2 Grafo?

	-Quien necesita un grafo cuando puedes hacer un grafo.
	Los objetos del juego se organizan de tal manera que cada pais funciona
	como nodo en el mundo siendo las conexiones de los paises mediante
	objetos con propiedades especiales.
	
2.3 Mundo

	El planeta se genera instanciando multiples objetos dentro de otros
	de esta manera el mundo al ser creado deja un estructura reconocible
	facilmente modificable.
	
2.4 Menus

	Los menu se articulan en su mayoria dentro del archivo "Pandemic.py"
	exeptuando el resultante del menu estadistico el cual es parte del mundo
	
2.5 Super_lista y Posicionado:

	La super_lista es muy parecida a una lista solo que trae metodos adicionales
	para trabajarla ccomo cola a la vez.
	Por otro lado el Posicionado es un objeto el cual usa Lista de super_lista
	para ordenar obejtos en dos listas a la vez de manera mas sencilla.
	
2.6 Cambios relevantes en calculos:

	Todo cambio relacionado a las formulas del proframa deberian estar comentados
	para mayor facilidad al momento de buscarlas.
	
	
	


