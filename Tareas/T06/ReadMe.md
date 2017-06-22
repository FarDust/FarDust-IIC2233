# T06 - Progra Pop
 
##1.Funcionamiento
 
1. **Server**
 * Encontrado en el directorio **server** con el nombre de *main.py* esta clase se encarga de escuchar a los clientes mediante un protocolo de mensajería en json con el objetivo de poder agregar distintos clientes de manera sencilla, solo conociendo el protocolo.
 * El servidor al momento de detectar una conexión crea un **Theread** para el usuario ademas de generar su respectivo Lock para no interrumpir cuando se mande un archivo en formato no estandar (*JSON*).
 * Una vez generado el handshake con el cliente y comprobar los *hash* de las contraseñas de los usuarios, ya creados, luego agrega al usuario y su socket correspondiente a un diccionario para su fácil acceso por parte del servidor.
 * Ya conectado el servidor cierra la capacidad del usuario mientras este conectado realizar multiples conexiones y abre a este mismo nuevas instrucciones comenzando la fase de escucha.
 * La mayoría de las instrucciones estan en diccionarios JSON los cuales siempre deben tener una llave "status" que indica el el área a la que pertenece, estas llaves son las mismas para el cliente y la interfaz.
 * Por otro lado para el manejo de archivos el servidor reduce los archivos ****.wav*** directamente a 20 segundos con la funcion *wav_mini* del archivo ***wav_mini_op_420.py***.
 * El manejo de usuarios se realiza gracias a la base de datos ***users.csv*** y el directorio ***users_secure*** el cual guarda los hash de las contraseñas, cabe destacar que el servidor permite cualquier estacionario en la contraseña solo dependiendo del cliente que envia su contrasea encriptada al momento de crear el usuario o iniciar sesión.
2. **Connect**
 * Encargado de generar la conexión de la interfaz con el servidor y trabajar las operaciones de calculo necesarias, funciona con un Thread de escucha y una función de escucha conectada a la interfaz mediante señales.
 * Es el encargado del envió de archivos y hashear la contraseña al momento de crear un usuario, ademas le envia a la interfaz las señales emitidas por el servidor de login success y signin success permitiendo a esta ultima  cambiar de fase.
 * Al momento de recibir errores desde el servidor estos son entregados con las llaves "status" ***signin*** o ***login*** y "success" la cual contendra un booleano.
 * La mayoria de los mensajes de interfaz son directamente transmitidos a la inbterfaz para que se encargue del movimiento de los objetos visuales.
3. **Local**
 * Encargado del frontend del juego tiene la funcion de presentar las multiples opciones y anunciar al usuario las respuestas correctas.
 * Esta constantemente pidiendo al Cliente el nuevo estado del juego el cual en teoria deberia enviar el servidor, pero por razones de deployment quedaron a cargo de un QTimer el cual emite una señal cada una constante de 1 seg.
 * Se encarga de mostrar los graficos solo si el servidor lo permite por lo cual la existencia de salas o el accesso a ellas son imposibles sin el cliente.
 * Local funciona como un microservidor para el resto de la interfaz enviando señales a las interfases subordinadas, como las salas de juego siendo la unica interfaz que puede bloquearla el StartMenu.
 * La interfaz se reinicia al momento de perder conexion con el servidor y esta no muestra los errores desde el servidor como lo hace StartMenu por razones de comodidad del usuario.
 * Esta Interfaz es facilmente modificable mediante el archivo master.css encontrado el el directorio ***styles*** lo cual la vuelve modificable visualmente a la larga.
 * **Siempre** y cuando no ocurra un error fatal de la aplicacion, la Local enviara la señal correspondiente para la desconexion correcta del servidor.
4. **Start Menu**    
 * Cumple con la mision de realizar el hadshake con el servidor enviando los datos de inicio de session como texto plato al cliente.
 * Esta interfaz muestra todos los errores conocidos y dessonocidos que envie el seridor en relacion al inicio de session generando una alerta de lo mas molesta que se puede. :boom:
 * Esta interfaz le da el paso a **Local** cuando el cliente lo indica, esto dado que local,  no puede generar ninguna instruccion de handshake.
 * Esta interfaz vuelve a aparecer cada vez que se pierde la conexion con el servidor , asi evitando falsos positivos.
 * Por razones de rendimiento recomiendo que se abra una instancia para generar el signin y se genere otra para el login, ya que la estabilidad d la interfaz no es la mejor del universo.
 * Esta interfaz en modificable de la misma manera que Local.
 * Prefiera el uso de *Enter*.