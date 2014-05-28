# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


from pilasengine.actores.actor import Actor


class Aceituna(Actor):

    def iniciar(self):
        self.imagen = "aceituna.png"
        self.radio_de_colision = 15

    def actualizar(self):
        pass

    def terminar(self):
        pass
