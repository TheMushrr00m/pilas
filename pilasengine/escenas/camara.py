# -*- encoding: utf -*-
import random

class Camara(object):
    """Representa la cámara principal de la escena.

    El objeto cámara permite desplazarse, hacer movimientos
    de automento, alejamiento e incluso rotaciones.

    Este objeto se puede acceder usando el atributos pilas.carama, por
    ejemplo:

        >>> pilas.camara.escala = [2]
        >>> pilas.camara.rotacion = [45]
    """

    def __init__(self, pilas, escena):
        self.pilas = pilas
        self.escena = escena
        self._x = 0
        self._y = 0
        self._escala = 1
        self._rotacion = 0

    def aplicar_transformaciones_completas(self, painter):
        centro_x, centro_y = self.pilas.obtener_centro_fisico()
        painter.translate(centro_x, centro_y)
        painter.scale(self._escala, self._escala)
        painter.rotate(-self._rotacion)

    def aplicar_translacion(self, painter):
        centro_x, centro_y = self.pilas.obtener_centro_fisico()
        painter.translate(centro_x, centro_y)

    def vibrar(self, intensidad=1, tiempo=0.5):
        valores = [x*intensidad for x in [-4, -3, -2, 2, 3, 4] * int(tiempo + 1)]
        cantidad_de_valores = float(len(valores)) + 1

        random.shuffle(valores)
        self.x = valores + [0], tiempo/cantidad_de_valores

        random.shuffle(valores)
        self.y = valores + [0], tiempo/cantidad_de_valores

    def obtener_escala(self):
        return self._escala

    def definir_escala(self, valor):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'escala', valor)

    def obtener_rotacion(self):
        return self._rotacion

    def definir_rotacion(self, valor):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'rotacion', valor)

    def obtener_x(self):
        return self._x

    def definir_x(self, valor):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'x', valor)

    def obtener_y(self):
        return self._y

    def definir_y(self, valor):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'y', valor)

    escala = property(obtener_escala, definir_escala, doc="Cambia el escala o cercanía de la cámara.")
    rotacion = property(obtener_rotacion, definir_rotacion, doc="Cambia la rotacion de la pantalla.")
    x = property(obtener_x, definir_x, doc="Cambia la posición x de la pantalla.")
    y = property(obtener_y, definir_y, doc="Cambia la posición y de la pantalla.")