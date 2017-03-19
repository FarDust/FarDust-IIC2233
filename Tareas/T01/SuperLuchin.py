# SuperLuchín Alpha v1.0.0

from menu import LogIn
from leer import Users
from usuarios import Terreno, Sudo

rutaDeUsuarios = Users()

usuarioActual = LogIn().entrada()
if usuarioActual != ".":
    if rutaDeUsuarios.completar(usuarioActual)["recurso_id"] == "":
        usuarioActivo = Sudo(rutaDeUsuarios.completar(usuarioActual))
    else:
        usuarioActivo = Terreno(rutaDeUsuarios.completar(usuarioActual))
else:
    # instanciar nuevamente LogIn()
    pass

print(usuarioActivo.nombre)
