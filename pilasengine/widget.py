# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import sys
import traceback

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtOpenGL import QGLWidget

import fps

from pilasengine.controles import Controles


class BaseWidget(object):
    """Representa el componente que contiene toda la escena de pilas.

    Este widget puede contenerse dentro de una ventana de PyQt, o
    dentro de un maquetado mas complejo, como la ventana del intérprete
    o un editor.
    """

    def __init__(self, pilas, titulo, ancho, alto, capturar_errores=True):
        self.pilas = pilas
        super(BaseWidget, self).__init__()
        self.setMinimumSize(200, 200)
        self.activar_borrosidad()
        self.capturar_errores = capturar_errores
        self.definir_titulo(titulo)
        self.iniciar_interface(ancho, alto)
        self.pausa = False

    def iniciar_interface(self, ancho, alto):
        self.painter = QtGui.QPainter()
        self.setMouseTracking(True)
        self.mouse_x = 0
        self.mouse_y = 0

        self.original_width = ancho
        self.original_height = alto
        self.escala = 1

        self.fps = fps.FPS(60)  # 60 Cuadros por segundo.
        self.timer_id = self.startTimer(1000 / 100.0)

    def detener_bucle_principal(self):
        if self.timer_id:
            self.killTimer(self.timer_id)
            self.timer_id = None
        else:
            raise Exception("El bucle ya está detenido, no se puede detener nuevamente.")

    def reiniciar_bucle_principal(self):
        if self.timer_id:
            raise Exception("El bucle está en curso, no se puede reiniciar si se está ejecutando.")
        else:
            self.timer_id = self.startTimer(1000 / 100.0)

    def obtener_centro_fisico(self):
        """Retorna el centro de la ventana en pixels."""
        return self.original_width / 2, self.original_height / 2

    def obtener_area(self):
        """Retorna el tamaño real de la ventana."""
        return self.original_width, self.original_height

    def obtener_bordes(self):
        """Retorna los bordes de la pantalla en forma de tupla."""
        ancho, alto = self.obtener_area()
        return -ancho / 2, ancho / 2, alto / 2, -alto / 2

    def _realizar_actualizacion_logica(self):
        for _ in range(self.fps.actualizar()):
            self.pilas.realizar_actualizacion_logica()

    def procesar_error(self, e):
        titulo = repr(e)
        descripcion = traceback.format_exc(e)
        escena = self.pilas.escenas.Error(titulo, descripcion)

    def timerEvent(self, event):
        """Actualiza la simulación completa.

        Este método se llama automáticamente 100 veces por segundo, ya
        que se hace una llamada a 'startTimer' indicando esa frecuencia.
        """
        if not self.pausa:
            if self.capturar_errores:
                try:
                    self._realizar_actualizacion_logica()
                except Exception, e:
                    self.procesar_error(e)
            else:
                self._realizar_actualizacion_logica()
        else:
            self.pilas.realizar_actualizacion_logica_en_modo_pausa()

        # Pide redibujar el widget (Qt llamará a paintEvent después).
        self.update()

    def keyPressEvent(self, event):
        codigo_de_tecla = Controles.obtener_codigo_de_tecla_normalizado(event.key())

        if event.key() == QtCore.Qt.Key_Escape:
            self.pilas.eventos.pulsa_tecla_escape.emitir()

        self.pilas.eventos.pulsa_tecla.emitir(codigo=codigo_de_tecla,
                                              es_repeticion=event.isAutoRepeat(),
                                              texto=event.text())

        self.pilas.depurador.cuando_pulsa_tecla(codigo_de_tecla)

    def keyReleaseEvent(self, event):
        codigo_de_tecla = Controles.obtener_codigo_de_tecla_normalizado(event.key())

        self.pilas.eventos.suelta_tecla.emitir(codigo=codigo_de_tecla,
                                               es_repeticion=event.isAutoRepeat(),
                                               texto=event.text())

    def mousePressEvent(self, event):
        x, y = self.pilas.obtener_coordenada_de_pantalla_relativa(event.pos().x() / self.escala,
                                                                  event.pos().y() / self.escala)

        self.pilas.eventos.click_de_mouse.emitir(boton=event.button(), x=x, y=y)

    def mouseReleaseEvent(self, event):
        x, y = self.pilas.obtener_coordenada_de_pantalla_relativa(event.pos().x() / self.escala,
                                                                  event.pos().y() / self.escala)

        self.pilas.eventos.termina_click.emitir(boton=event.button(), x=x, y=y)

    def wheelEvent(self, event):
        self.pilas.escena_actual().mueve_rueda.emitir(delta=event.delta() / 120)

    def mouseMoveEvent(self, event):
        x, y = self.pilas.obtener_coordenada_de_pantalla_relativa(event.pos().x() / self.escala,
                                                                  event.pos().y() / self.escala)

        dx = x - self.mouse_x
        dy = y - self.mouse_y

        self.pilas.eventos.mueve_mouse.emitir(x=x, y=y, dx=dx, dy=dy)

        self.mouse_x = x
        self.mouse_y = y

    def _pintar_fondo(self):
        self.painter.setBrush(QtGui.QColor(200, 200, 200))
        size = self.size()
        w = size.width()
        h = size.height()
        self.painter.drawRect(0, 0, w - 1, h - 1)

    def paintEvent(self, e):
        self.painter.begin(self)
        self._pintar_fondo()
        self._dibujar_widget()
        self.painter.end()

    def resizeEvent(self, event):
        self._ajustar_canvas(self.width(), self.height())

    def _ajustar_canvas(self, w, h):
        escala_x = w / float(self.original_width)
        escala_y = h / float(self.original_height)
        escala = min(escala_x, escala_y)

        final_w = self.original_width * escala
        final_h = self.original_height * escala
        self.escala = escala

        x = w - final_w
        y = h - final_h

        self.setGeometry(x / 2, y / 2, final_w, final_h)
        self._centrar_canvas(w, h)

    def _centrar_canvas(self, w, h):
        dw = w - self.frameGeometry().width()
        dh = h - self.frameGeometry().height()
        self.move(dw / 2, dh / 2)

    def _dibujar_widget(self):
        # Suavizar efectos y transformaciones de imágenes.
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        self.painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, self._borrosidad)
        self.painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)

        self.painter.scale(self.escala, self.escala)

        self.pilas.realizar_dibujado(self.painter)

        if self.pausa:
            font = QtGui.QFont(self.painter.font().family(), 30)
            self.painter.setPen(QtCore.Qt.white)
            self.painter.setFont(font)
            w = self.original_width
            h = self.original_height
            self.painter.drawText(QtCore.QRect(0, 0, w, h), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, "en pausa")

    def activar_borrosidad(self):
        "Habilita transformaciones de buena calidad, como zoom y rotaciones."
        self._borrosidad = True

    def desactivar_borrosidad(self):
        "Deshabilita las transformaciones de buena calidad."
        self._borrosidad = False

    def definir_tamano_real(self):
        self.resize(self.original_width, self.original_height)

    def definir_titulo(self, titulo):
        self.setWindowTitle(titulo)

    def obtener_titulo(self):
        return self.windowTitle()

    def pausar(self):
        "Pasa al modo pausa."
        self.pausa = True

    def esta_en_modo_pausa(self):
        "Informa si el widget está o no en modo pausa."
        return self.pausa

    def avanzar_un_solo_cuadro(self):
        "Avanza un solo cuadro de animación estando en modo pausa."
        self.pilas.realizar_actualizacion_logica()
        self.pilas.forzar_actualizacion_de_interpolaciones()

    def continuar(self):
        "Quita el modo pausa."
        self.pausa = False


class WidgetConAceleracion(BaseWidget, QGLWidget):
    pass


class WidgetSinAceleracion(BaseWidget, QtGui.QWidget):
    pass
