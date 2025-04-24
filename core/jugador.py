from mapa import Mapa
from region import Region
from region_manager import RegionManager
from recursos import Recurso
from tropas import *
from edificios import *

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

        VOLVER

Mover tropa, y mover batallón consumen el turno, si mueves la tropa a territorio enemigo -> COMBATIR o ABORTAR
'''


class Jugador:

    def __init__(self, usuario, reino, mapa, recursos: list[Recurso] = [Recurso('madera', 100, 0, 100), Recurso('agua', 100, 0, 100),
                                                                 Recurso('piedra', 50, 0, 100), Recurso('hierro', 25, 0, 100),
                                                                 Recurso('oro', 50, 0, 100), \
                                                                 Recurso('caza', 400, 0, 400),
                                                                 Recurso('recoleccion', 400, 0, 400)],
                 conquista: list[tuple[int, int]] = []):
        self.usuario = usuario
        self.reino = reino
        self.mapa = mapa
        self.conquista = conquista  # Se debe actualizar en cada interacción
        self.recursos = recursos
        self.region_actual: tuple[int, int] = None  # La zona que esta consultando el jugador dentro del bucle principal

    def __str__(self):
        return f'Usuario: {self.usuario}'

    def mapa_grafico(self, mapa):
        pass
    def establecer_reino(self):
        '''
        Establece su reino, es decir, su primer territorio en el que maniobrar
        '''
        for region in self.mapa.reinos:
            if region.get_propietario() == 'Neutral':
                region.set_propietario(self.usuario)  
                region.set_nombre_reino(self.reino)
            break
    def ver_zona(self, region: tuple[int, int]):  # Actualiza a su vez la región actual
        self.region_actual = region
        return str(self.mapa.regiones[self.region_actual]), True if self.mapa.regiones[self.region_actual].get_propietario() == self.nombre else False

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

    @classmethod
    def mostrar_catalogo_edificios(cls):
        if not hasattr(cls,'edificios_objetos'):
            cls.edificios_objetos = {
            key.lower(): value
                for key, value in globals().items()
                if isinstance(value,type) and
                        (issubclass(value, Edificio))
                        and value is not Edificio
        }
        catalogo = ''
        for i in cls.edificios_objetos.values():
            catalogo += str(i()) + '\n'
        return cls.edificios_objetos, catalogo
    
    def add_tropa(self, tropa, cantidad):
        cantidad = int(cantidad) #El valor que se pasa a la API ES STR
        if tropa in self.__class__.tropas_objetos.keys():
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
            self.mapa.regiones[self.region_actual].tropas.append(nueva_tropa)
            return f'Tropa añadida correctamente'
        else:
            return f'Tropa: {tropa} no existe'

    def mover_tropa(self, destino: tuple[int, int], tropa, cantidad):
        cantidad = int(cantidad)
        if destino in self.conquista + self.mapa.regiones[self.region_actual].get_conexiones():
            if self.mapa.regiones[destino].get_propietario() == self.usuario or self.mapa.regiones[destino].get_propietario() == 'Neutral':
                if tropa in self.__class__.tropas_objetos.keys():
                    if tropa in self.mapa.regiones[self.region_actual].tropas:
                            tropa_mover = self.mapa.regiones[self.region_actual].tropas[self.mapa.regiones[self.region_actual].tropas.index(tropa)]
                            if  tropa_mover.cantidad > cantidad:
                                nueva_tropa = tropa_mover - cantidad
                                tropa_mover -= cantidad
                                if tropa in self.mapa.regiones[destino].tropas:
                                    tropa_destino = self.mapa.regiones[destino].tropas[self.mapa.regiones[destino].tropas.index(tropa)]
                                    tropa_destino += nueva_tropa
                                    return f'Tropa movida a {destino}',True
                                self.mapa.regiones[destino].tropas.append(nueva_tropa)
                                return f'Tropa movida a {destino}',True
                            elif tropa_mover.cantidad == cantidad:
                                nueva_tropa = self.mapa.regiones[self.region_actual].tropas[self.mapa.regiones[self.region_actual].tropas.index(tropa)]
                                self.mapa.regiones[self.region_actual].tropas.remove(tropa)
                                if tropa in self.mapa.regiones[destino].tropas:
                                    tropa_destino = self.mapa.regiones[destino].tropas[self.mapa.regiones[destino].tropas.index(tropa)]
                                    tropa_destino += nueva_tropa
                                    return f'Tropa movida a {destino}',True
                                self.mapa.regiones[destino].tropas.append(nueva_tropa)
                                return f'Tropa movida a {destino}',True

                            else:
                                return f'No dispones de {cantidad} {tropa}',True
                    return f'No dispones de {tropa} en la region',True
                else:
                    return f'Tropa: {tropa} no existe',True
            else:
                return f'La zona pertenece a {self.mapa.regiones[destino].get_propietario()}\n Combatir?',False #False cuando haya opción de combate
        else:
            return f'No puedes moverte a {destino}, fuera de rango',True

    def mover_batallon(self, destino: tuple[int, int]):
        pass

    def combatir(self,destino: tuple[int, int]):
        Ejercito_Atk = self.mapa.regiones[self.region_actual].tropas
        Ejercito_Def = self.mapa.regiones[destino].tropas
        texto_lista = []
        while Ejercito_Atk!=[] and Ejercito_Def!=[]:    #El bucle se repetirá hasta que uno de los ejercitos esté vacio

            max_tropas = max(len(Ejercito_Atk), len(Ejercito_Def)) #Cogemos la longitud del ejercito más grande
            for i in range(max_tropas):  #Repetimos el bucle hasta que lleguemos a la longitud del ejercito más grande
                if i < len(Ejercito_Atk):
                    texto_lista.append(Ejercito_Atk[i].atacar(Ejercito_Atk, Ejercito_Def))  #La tropa 'i' ataca al ejercito enemigo

                if i < len(Ejercito_Def):
                    texto_lista.append(Ejercito_Def[i].atacar(Ejercito_Def, Ejercito_Atk))  #La tropa 'i' ataca al ejercito enemigo


        if Ejercito_Atk==[]:    #Si el ejercito de ataque se ha quedado sin tropas...
            texto_lista.append('El ataque fracasó.')
            return texto_lista  
        elif Ejercito_Def==[]:  #Si el ejercito de defensa se ha quedado sin tropas...
            texto_lista.append('Ataque exitoso.')
            return texto_lista

    def construir_edificio(self, edificio):
        if edificio in self.__class__.edificios_objetos.keys():
            costo = self.__class__.edificios_objetos[edificio].costo
            if all(self.recursos[self.recursos.index(recurso)] >= recurso for recurso in costo):
                for recurso in costo:
                    self.recursos[self.recursos.index(recurso)] -= recurso
                self.mapa.regiones[self.region_actual].edificios.append(self.__class__.edificios_objetos[edificio]())
                return f'Edificio: {edificio} construido'
            else:
                return 'Recursos insuficientes'
            
        else:
            return f'Edificio: {edificio} no reconocido'

    def actualizar_conquista(self) -> None:
        for coordenada,region in self.mapa.regiones.items():
            if region.get_propietario() == self.usuario:
                self.conquista.append(coordenada)
    def mostrar_recursos(self) -> str:
        recursos_str = ''
        for recurso in self.recursos:
            recursos_str += str(recurso) + '\n'
        return recursos_str
    def __eq__(self,other):
        if self.usuario == other:
            return True
        else:
            return False
