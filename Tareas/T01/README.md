# IIC2233 - Programación Avanzada

## Tarea 01

## Manual SuperLuchin.py

Bienvenido usuario inexperto

SuperLuchin es un programa enfocado en la utilizacion efectiva de recursos al moemnto de
apagar un incendio, tomando como informacion de referencia los datos ingresados los usuarios
Anaf a la base de datos.

Al entrar en el programa te encontraras con un menu que te hara preguntas sencillas para
realizar las acciones requeridas por el usuario.

Capitulo 1: Usuarios y base de datos

1.1 Inicio de sesion

Al momento de inicar el programa este te pedira una confirmacion de que deseas inicar sesion,
una vez realizada la confirmacion este te pedira un usuario y contraseña para comprara con
la base de datos. Si este se encuentra en ella el programa atomaticamente permitira el uso
de las funciones asignadas a tal usuario luego de escribir la fecha de conexion.

Estas accion le permitira al usuario acceder a la base de datos dependiendo de sus privilegios
por un sencillo menu el cual pide numeros o letras para seleccionar entre las distintas 
opciones disponibles.

1.2 Menu de usuario

En el menu principal se le presentaran una gran variedad de opciones di el usuario ingresado
pertenece a la Anaf en otro caso el usuario tendra las siguientes opciones:

	0. Ver barra de estado superior generada automaticamente
	1. Ver los datos de un incendio si es que el usuario fue asignado a alguno
	f. cambiar la fecha actual
	x. cerrar sesion(Esta accion devuelve al usuario al inciso 1.1)

En el caso del usuario Anaf se detallara las acciones disponibles mas adelante, exeptuando
las opcion "f" y "x" que se mantienen entre todos los tipos de usuario(consultar arriba).

1.3 Leyendo la base de datos

	1.3.1 Anaf
		Todos los usuarios de tipo Anaf acceder a la lectura de la base de datos avanzada
		la cual les permitira acceder a las siguientes opciones:
		
			1. Leer usuarios
			2. leer incendios
			3. lerr recursos
			
		en todas las lecturas se le otorgara a el usuario 3 opciones las cuales consinten
		en leer todo el archivo, leer linea a linea o leer una linea especifica basado en id.
		
	1.3.2 Terreno (Bomberos o jefes de brigada)
		Estos usuarios tendran acceso a su recurso asignado gracias a la barra superior
		que se les presentara cada vez que ingresen al menu principal.
		Por otro lado si se les fue asignado asistir a un incio podran ver toda la 
		informacion relacionada al incendio durante su asignacion(acceso detallado en 1.2).
		
1.4 Intervernir base de datos

	La base de datos puede ser intervenida por los usuarios Anaf de las siguientes maneras
	 1. agregando un usuario
	 2. agregando un incendio
	 3. agregando un pronostico del clima
	En cualquiera de ellas aparecera un menu que especificara la informacion necesaria
	para que la accion se complete satisfactoriamente. Luego de que la informacion sea
	ingrsada esta se incluira en a la base de datos existente, si fuese el caso de que 
	un dato tenga que ser remplazado se le preguntara al usuario previamente antes de 
	sobreescribir.
	Cabe destacar que ningun usuario anaf tiene premitido eliminar libremente datos
	asi que la sobreescritura es la unica manera de alterar la base de datos en caso de 
	querer realizar una eliminacion.
	
2. Preguntas al sistema

	Una vez iniciado superluchin este creara todas las instancias de Recusrsos, Climas e 
	Incendios una unica vez ademas solo mantendra un usuario activo al la vez el cual
	sera sobrescrito en el programa en cada inicio de sesion.
	
	Las preguntas al sistema disponibles para el usuario Anaf son las siguientes:
	
		1. listado de incendios activos
		2. listado de incendios extintos
		3. listado de recursos mas explotados
		4. listado de recursos mas efectivos
		5. pedir una estrategia de extincion
		
	1.1 listado de incendios activos
	
		Simplemente despliega una lista de los incendios activos a la fecha actual.
		
	1.2 listado de incendios extintos
		
		Muestra un listado de los incendios que tienen puntos de poder menores o iguales
		a cero.
	
	1.3 listado de recursos mas usados(explotados)
		
		Muestra en orden decreciente los recursos que fueron mayormente utilizados
		
	1.4 listado de recursos mas efectivos
		
		Cumple la misma tarea que el 1.3 pero con los mas efectivos al momento de apagar
		incedios.
	
	1.5 pedir una estrategia de extincion
		
		Le solicita a SuperLuchin hacer el trabajo de la anaf que sera explicado en 3.

3. Estrategia de extincion

	Esta parte de SuperLuchin esta encargada de dejar sin trabajo a los trabajadores de 
	la anaf. Este inciso permite disponer de una estrategia la cual apague un incendio 
	especifico dependiendo de un criterio ademas de dar la opcion de simular el uso
	de un recurso especifico.
	
	3.1 Simular
	
		simula el trayecto de un recurso especifico hacia un incendio y los puntos
		de poder que le resta a este.
		
	A partir de la version SuperLuchin alpha 1.0.1 !!!
	
	3.2 Estrategia segun costo
	
		busca la manera mas efectiva de apagar un incendio al menor costo posible
	
	3.3 Estrategia segun velocidad
	
		Para esos incendios descontrolados busca la manera mas rapida de apagar el mismo
		
	3.4 Estrategia segun recursos utilizados
	
		En el momento que se necesitan aviones rusos este metodo trata de disminuir los 
		recursos utilizados para apagar el incendio
		
4. Notas importantes
	
	los incendios calculan sus puntos de poder dado cierto climas los cuales actulizan 
	sus caracteristicas automaticamente.

		






