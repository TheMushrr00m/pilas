# -*- encoding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4 import QtCore

from pilasengine.depurador.modo_info import ModoInformacionDeSistema
from pilasengine.depurador.modo_radios_de_colision import ModoRadiosDeColision
from pilasengine.depurador.modo_puntos_de_control import ModoPuntosDeControl
from pilasengine.depurador.modo_area import ModoArea
from pilasengine.depurador.modo_posicion import ModoPosicion

class Depurador(object):

    def __init__(self, pilas):
        self.pilas = pilas
        self._modos = []
        self.lienzo = pilas.imagenes.crear_superficie(500, 500)

    def desactivar_todos_los_modos(self):
        self._modos = []

    def realizar_dibujado(self, painter):
        """Realiza un dibujado de los modos depuración habilitados.

        Este método se llama automáticamente desde el método
        '_dibujar_widget' que está definido en widget.py, es decir, se
        llama cada vez que se tiene que dibujar la pantalla (unas 60
        veces por segundo).
        """
        if self._modos:
            for m in self._modos:
                m.realizar_dibujado(painter)

    def cuando_dibuja_actor(self, actor, painter):
        """Este método se llama cada vez que se dibujar un actor en pantalla.

        Es importante notar que el objeto 'painter' que viene como
        argumento es en realidad un objeto que tiene estado: cualquier
        cosa que se dibuje va a 'heredar' las mismas transformaciones
        que tiene el actor.

        Por ejemplo, si el actor esta escalado a 2x lo que dibujes
        aquí va a salir 2 veces mas grande que su tamaño original.

        Para revertir o evitar estas transformaciones se pueden usar
        las propiedades x, y, escala, centro o rotacion del actor.
        """
        if self._modos:
            for m in self._modos:
                m.cuando_dibuja_actor(actor, painter)

    def obtener_modos_habilitados(self):
        """Retorna una lista con los nombres de los modos habilitados."""
        modos = [x.__class__.__name__ for x in self._modos]
        return modos

    def definir_modos(self, info=False, radios=False, posiciones=False,
                      puntos_de_control=False, areas=False,
                      fisica=False):
        """Permite habilitar o deshabilitar los modos depuración.

        Cada uno de los argumentos representa un modo depuración, el valor True
        habilita el modo, False lo deshabilita.
        """

        modos_habilitados = self.obtener_modos_habilitados()
        modos_solicitados = []

        if info:
            modos_solicitados.append('ModoInformacionDeSistema')

        if radios:
            modos_solicitados.append('ModoRadiosDeColision')

        if posiciones:
            modos_solicitados.append('ModoPosicion')

        if puntos_de_control:
            modos_solicitados.append('ModoPuntosDeControl')

        if areas:
            modos_solicitados.append('ModoArea')

        if fisica:
            modos_solicitados.append('ModoFisica')

        modos = set(modos_habilitados).symmetric_difference(modos_solicitados)

        if 'ModoInformacionDeSistema' in modos:
            self._alternar_modo(ModoInformacionDeSistema)

        if 'ModoPuntosDeControl' in modos:
            self._alternar_modo(ModoPuntosDeControl)

        if 'ModoRadiosDeColision' in modos:
            self._alternar_modo(ModoRadiosDeColision)

        if 'ModoArea' in modos:
            self._alternar_modo(ModoArea)

        if 'ModoFisica' in modos:
            self._alternar_modo(ModoFisica)

        if 'ModoPosicion' in modos:
            self._alternar_modo(ModoPosicion)

    def _alternar_modo(self, clase_del_modo):
        clases_activas = self.obtener_modos_habilitados()

        if clase_del_modo.__name__ in clases_activas:
            self._desactivar_modo(clase_del_modo)
        else:
            self._activar_modo(clase_del_modo)

    def _activar_modo(self, clase_del_modo):
        instancia_del_modo = clase_del_modo(self.pilas, self)
        self._modos.append(instancia_del_modo)

    def _desactivar_modo(self, clase_del_modo):
        instancia_a_eliminar = [x for x in self._modos
                                if x.__class__ == clase_del_modo]
        self._modos.remove(instancia_a_eliminar[0])
        instancia_a_eliminar[0].sale_del_modo()