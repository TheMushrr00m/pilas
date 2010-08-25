# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import os

from PySFML import sf

import pilas

def cargar(ruta):
    """Intenta cargar la imagen indicada por el argumento ``ruta``.

    Por ejemplo::

        import pilas

        imagen = pilas.imagen.cargar("mi_archivo.png")

    En caso de éxito retorna el objeto Image, que se puede asignar
    a un Actor.

    El directorio de búsqueda de la imagen sigue el siguiente orden:

        * primero busca en el directorio actual.
        * luego en 'data'.
        * por último en el directorio estándar de la biblioteca.

    En caso de error genera una excepción de tipo IOError.
    """

    ruta = pilas.utils.obtener_ruta_al_recurso(ruta)

    # Genera el objeto image y lo retorna.
    image = sf.Image()
    image.LoadFromFile(ruta)

    return image
