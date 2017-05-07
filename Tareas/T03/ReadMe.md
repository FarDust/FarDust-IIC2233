#T03: RQL DataBase

##1.Funcionamiento

1.  **Interprete**
  * El funcionamiento  principal del programa ocurre a través de la función  interpretar encontrada en el archivo interprete.py. Esta función recursiva analiza la consulta y asegura si la puede resolver si esto es así se llamara a si misma para obtener el resultado de las subconsultas si es que están presentes.
  * La función en si devuelve una tupla de datos la cual contiene en strings los mensajes obtenidos desde la consulta principal, vale destacar que la función **interpretar()** es la que se hace cargo de resolver los errores en RQL.
  * Las principales consultas encontradas se realizan con la llamada a un diccionario que recoge las funciones de sub-modulos al iniciar el programa, este diccionario mas el diccionario *"asignar"* se usan para que la función compruebe si un **str** es  o no una variable y si este puede ser asignado como tal. 
  * Todas las funciones invocadas reciben las consultas ya procesadas por **interpretar()** exceptuando los casos especiales.
  * **Nota:** se añadió un decorador a interpretar() por en caso de ocurrir un error indeterminado atraparlo desde ahí por parte del que este modificando el programa.
2. **comando "do_if"**
  * Comando especial que junto a **interpretar()** discierne entre dos consultas, este comando se trata de manera especial por parte del interprete ya que este le entrega directamente a **do_if()** las consultas sin interpretar, así evitando resolver consultas innecesarias.
  * Vale destacar que do_if() debe resivir el argumento de interprete graph, ya que si en la consulta se requiere graficar que se muestren los gráficos correspondientes a la consulta.
3. **comando "asignar"**
  * El comando **asignar()** es el segundo comando tratado de manera especial por el interprete. ya que siempre el interprete le entregara a la función  la primera consulta sin interpretar, por lo cual si ocurre el caso de no entregarse un string después de *'asignar'* la función automáticamente rechazara la consulta.
  * Por otro lado el modulo *basic.py* al arrancar obtiene todas las llaves de diccionario de las funciones de RQL por lo cual si la variable a asignar esta en las llaves sera inmediatamente rechazada. 
4. **comando "graficar"**
  * El comando graficar recibe una opción especial por parte del interprete para discernir si este mostrara o no los gráficos creados.
5. **comandos generales**
 * **crear_funcion()**: Crear una distribución de probabilidad la cual depende de una variable.
 * **extraer_columna()**: Dado un nombre de archivo retorna un generador el cual es copiado por *interpretar()* al ser solicitado siempre y cuando este este asignado a una variable.
 *  **filtrar()**: Filtra un iterable respecto a _{==,<,>,>=,<=,!=}_ y un valor , devuelve un generador.
 *  **operar()**: Opera sobre una serie de datos dada una función.
 *  **evaluar()**: Dado un intervalo la los resultados de la función dada.
 *  **LEN()**: Devuelve la longitud de un iterable
 *  **PROM()**: Retorna el promedio de un conjunto de datos.
 *  **DESV()**: Retorna la desviación estándar de un conjunto de datos.
 *  **VAR()**: Retorna *DESV()*^2.
 *  **MEDIAN()**: Retorna la mediana de un conjunto de datos.
 *  **comparar_columna()**: Comapara dos conjuntos de datos y retorna un booleano.
 *  **comparar**: Compara dos datos y retorna un booleano.

##2. Interfaz
 * La interfaz de RQL recibe consultas con los nombres del os comando en forma de **str** y las entrega a *Interpretar()* para su proceso, en el caso de que las consultas generen errores determinados RQL devolverá el error determinado en consola mediante un str o en su defecto lo escribirá en el archivo *colsultas.txt*.Por otro lado al recibir alguna consulta que genere un error indeterminado RQL simplemente no agregara nada a la interfaz o archivo , sino que devolvera un mensaje en consola para su futura reparación. 