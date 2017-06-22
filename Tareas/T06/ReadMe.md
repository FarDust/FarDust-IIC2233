# T06 - Progra Pop
 
##1.Funcionamiento
 
1. **Server**
 * Encontrado en el directorio **server** con el nombre de *main.py* esta clase se encarga de escuchar a los clientes mediate un protocolo de mensajeria en json.
2. **Connect**
 * Modulo encargado del el backend del programa, el cual contiene las interacciones con los objetos dentro del juego.
 * Otra función de este modulo es señalizarle a los objetos involucrados a quienes pueden atacar.
3. **Local**
 * Modulo encargado del frontend del juego, contiene la funcion ***read_styles()*** , la clase ***LeagueOfProgra*** y la clase ***StartMenu***.En su conjunto administran la parte visual del juego emitiendo señales a los demas integrates del juego para tomar desiciones.
 * La funcion ***read_styles()*** lee directamente de la carpeta *styles* la que contine archivos en formato ***.css**, con esto se logra una interfaz fácilmente personalizable con los conocimientos adecuados.
4. **Start Menu**    
 La estructura del directorio principal se divide en una serie de carpetas las cuales contienen las imagenes, scripts y descriptores de animaciones para el juego.
 1. **data**
     * La carpeta *data* contiene las constantes del juego en 2 tipos de formatos ***.properties** y ***.json**, los archivos properties estan detinados a guardar la informacion de los campeones [^1] y las cnfiguraciones globales. Por otro lado los archivos json estan destinados a los datos no mutables del juego ya que son mas dificiles de leer para el usuario inexperto.
     * Los archivos properties son leidos por una funcion en la carpeta *scripts* la cual se encarga de formatear estos archivos en un diccionario, a partir de ciertas reglas preconfiguradas.
 2. **IMGS**
     * Este directorio esta encargado de contener todas las imágenes y animaciones a utilizar en el juego (originalmente llamada resources), en primera instancia el directorio esta compuesto de 4 tipos de archivos: 
         *  ***.png** -> representando a las imagenes.
         *  ***.bat** -> encargado de ejecutar en consola las preview de las animaciones.
         *  ***.pyanim** -> un archivo python comun y corriente que es un derivado de el script principal ***animation.py*** en la carpeta *scripts*.
         *  ***.lop** -> archivo custom LeagueOfProgra el cual contiene el orden de los frames a solicitar.
 1. **objects**
     * Directorio que almacena todos los objetos funcionales del juego, por lo cual contiene todas las clases y sus herencias.
 1. **scripts**
     * Directorio encargado de almacenar funciones , modulos utiles y codigo basura :smile: . El directorio almacena la clase destinada a la emision de señales de movimiento y al paso de las animaciones.
     * El encargado de las animaciones es el script ***animation.py*** (en su versión 2.0) el cual contiene una clase que hereda de *QLabel* y contiene un QTimer que pasa las imágenes.
     * **PD :** Si buscan la version 1.0 de animation.py, esta se encuentra en el directorio **IMGS**, advierto que tengan miedo. :boom:
 1. **styles**
     * Como se menciono anteriormente esta carpeta esta detinada ha poder customizar la interfaz que incluye el juego, lamentablemente en desarrollo.