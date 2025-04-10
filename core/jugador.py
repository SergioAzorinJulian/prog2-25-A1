from mapa import Mapa
from region import Region
from region_manager import RegionManager
from recursos import Recurso
from tropas import *

'''
PLANTEAMIENTO DEL MENÚ DEL JUGADOR:
    VER MAPA GRÁFICO -> La idea seria mostrar tus zonas con una X, las de nadie con ? y las del enemigo con O (No es prioridad para el viernes)
        Se podría quizá dibujar un grafo, pero ya se verá ... 

    ACCEDER A ZONA:
        (SE MUESTRA LA INFORMACIÓN DE LA ZONA), Se actualiza self.region_actual a la zona que esta viendo
        AÑADIR TROPAS -> Se crean tropas en la zona actual, consume recursos:[] (escribir que recurso consume cada tropa el que lo sepa)
            Tropas normales -> Comida y Agua
            Tropas de asedio (elefantes y arietes) -> Comida, Agua y Madera

        MOVER_TROPA -> Se mueve la tropa indicada a destino, es necesario implementar un método que permita restar cant a la instancia del obj tropa, y otro para sumarlo en caso de que en destino ya esté esa tropa
            Para movimientos dentro de tu dominio -> Puedes avanzar 2 (o 3, ya se ve en el desarrollo) "casillas" en un turno
            Para movimientos en zonas neutras o enemigas -> Puedes avanzar una zona por turno

        MOVER_BATALLÓN -> Lo mismo pero mueve todas las tropas de una

        CONSTRUIR EDIFICIO -> Construye edificios, escribir aquí edificios y recursos que consumen crearlos -> []

        AÑADIR FAMILIA -> Añade familias, escribir aquí que recurso consume añadir cada familia -> []
            Sistema de generación de familias:
                Se parte de una cantidad inicial (6 o las que se definan) y cada 2 o 3 (o X) turnos se hace "recuento" de recursos del reino;
                es decir, si se tiene comida y agua "de sobra" (superavit) vendra 1 o 2 (o Y) familias nuevas al reino; de igual manera, si para 
                el turno X no tienes suficiente agua y comida para sustentar al pueblo (déficit) se empezaran a ir las familias del reino; pero 
                más paulatinamente, porque sino podría llegar un punto crítico en el que no haya familias, y por tanto tampoco quien trabaje ...

        VOLVER

Mover tropa, y mover batallón consumen el turno, si mueves la tropa a territorio enemigo -> COMBATIR o ABORTAR
'''


class Jugador:
    def __init__(self, usuario, mapa, recursos: list[Recurso] = [Recurso('madera', 100, 0), Recurso('agua', 100, 0),
                                                                 Recurso('piedra', 50, 0), Recurso('hierro', 25, 0),
                                                                 Recurso('oro', 25, 0), \
                                                                 Recurso('caza', 400, 0),
                                                                 Recurso('recoleccion', 400, 0)],
                 conquista: list[tuple[int, int]] = []):
        self.usuario = usuario
        self.mapa = mapa
        self.conquista = conquista  # Se debe actualizar en cada interacción
        self.recursos = recursos
        self.region_actual: tuple[int, int] = None  # La zona que esta consultando el jugador dentro del bucle principal

    def mapa_grafico(self, mapa):
        pass

    def ver_zona(self, region: tuple[int, int]):  # Actualiza a su vez la región actual
        self.region_actual = region
        return str(self.mapa.regiones[self.region_actual])

    @classmethod
    def mostrar_catalogo(cls):
        if not hasattr(cls, 'tropas_objetos'):
            cls.tropas_objetos = {
                key.lower(): value
                for key, value in globals().items()
                if isinstance(value, type) and (
                        issubclass(value, TropaAtaque) or
                        issubclass(value, TropaDefensa) or
                        issubclass(value, TropaAlcance) or
                        issubclass(value, TropaEstructura)) and value not in (
                   TropaAtaque, TropaDefensa, TropaEstructura,
                   TropaAlcance)}  # isinstance -> objeto, issubclas-> objeto
        catalogo = ''
        for i in cls.tropas_objetos.values():
            catalogo += str(i()) + '\n'

        return cls.tropas_objetos, catalogo

    def add_tropa(self, cls, tropa, cantidad):
        if tropa in self.__class__.tropas_obetos.keys():
            for recurso in self.recursos:
                if recurso == self.__class__.tropas_objetos[tropa].recursos:
                    if recurso.cantidad >= self.__class__.tropas_objetos[tropa].recursos.cantidad * cantidad:
                        recurso -= self.__class__.tropas_objetos[tropa].recursos * cantidad
                    else:
                        return f'Cantidad insuficiente de {self.__class__.tropas_objetos[tropa].recursos.nombre}'
            nueva_tropa = self.__class__.tropas_objetos[tropa](cantidad=cantidad)
            for i in self.mapa.regiones[self.region_actual].tropas:
                if nueva_tropa == i:
                    i += nueva_tropa
                    return f'Tropa añadida correctamente'
            return self.mapa.regiones[self.region_actual].tropas.append(nueva_tropa)
        else:
            return f'Tropa: {tropa} no existe'

    def mover_tropa(self, destino: tuple[int, int], tropa, cantidad):
        # AÑADIR COMPROBACIÓN: destino pertenece a conquista + self.mapa.regiones[self.region_actual].get_conexiones
        if tropa in self.__class__.tropas_obetos.keys():
            for i in self.mapa.regiones[self.region_actual].tropas:
                if i.nombre.lower() == tropa:  # tropa debe ser minúscula
                    if i.cantidad > cantidad:
                        nueva_tropa = i - cantidad
                        for tropa_destino in self.mapa.regiones[destino].tropas:
                            if nueva_tropa == tropa_destino:
                                tropa_destino += nueva_tropa
                                return f'Tropa movida a {destino}'
                        self.mapa.regiones[destino].tropas.append(nueva_tropa)
                        return f'Tropa movida a {destino}'
                    elif i.cantidad == cantidad:
                        nueva_tropa = i
                        self.mapa.regiones[self.region_actual].tropas.remove(i)
                        for tropa_destino in self.mapa.regiones[destino].tropas:
                            if nueva_tropa == tropa_destino:
                                tropa_destino += nueva_tropa
                                return f'Tropa movida a {destino}'
                        self.mapa.regiones[destino].tropas.append(nueva_tropa)
                        return f'Tropa movida a {destino}'

                    else:
                        return f'No dispones de {cantidad} {i.nombre}'
            return f'No dispones de {tropa} en la region'
        else:
            return f'Tropa: {tropa} no existe'

    def mover_batallon(self, destino: tuple[int, int]):
        pass

    def combatir(destino: tuple[int, int]):
        pass

    def construir_edificio(self, edificio):
        pass

    def add_familia(region: tuple[int, int], familia):
        pass
'''
    def regenerar_recursos():
        pass

    def actualizar_conquista():
        pass

    def actualizar_tropas():
        pass
'''