
"""
class Tropa:

    '''
    Clase en la que se encuentra todas las diferentes tropas

    ATRIBUTOS:
    -------------
    tropa_stats: Dic
    Diccionario empleado para almacenar las estadisticas de cada tropa

    recursos: int
    Número de recursos necesario para entrenar una tropa

    nombre: str
    Nombre de la tropa

    puntos_vida: float
    Puntos de vida de la tropa

    ataque: float
    Daño que hace la tropa

    METODOS:
    -----------
    añadir_tropa_stats: Metodo que añade la información de una cada tropa al diccionario tropa-stats (se activa cada vez que creas un objeto tropa, sea la tropa que sea)

    rellenar_tropa_stats: Metodo ligado a añadir_tropa_stats, se encarga de crear un objeto de cada tropa, siendo añadido inmediatamente al diccionario de las estadisticas mediante añadir_tropa_stats

    '''
    tropa_stats = {}
    def __init__(self,recursos=int, nombre=str, puntos_vida=float, ataque=float):
        self.nombre = nombre
        self.puntos_vida = puntos_vida
        self.ataque = ataque
        self.recursos=recursos


    def anadir_tropa_stats(self):
        Tropa.tropa_stats[self.nombre]=self   #Añadimos al diccionario el objeto, se puede acceder a él por el nombre de tropa


    @staticmethod
    def rellenar_tropa_stats():
        soldado = Soldado()    #Creamos un objeto de cada clase tropa
        caballero = Caballero()
        arquero = Arquero()
        ogro = Ogro()
        ballestero = Ballestero()
        mago = Mago()
        catapulta= Catapulta()
        escudero=Escudero()



class TropaAtaque(Tropa):

    '''
    Clase de la que heredarán las tropas de tipo "Ataque"
    '''

    def __init__(self,recursos=int, nombre=str, puntos_vida=float, ataque=float):
        super().__init__(recursos,nombre, puntos_vida, ataque)





class TropaDefensa(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Ataque"
    '''

    def __init__(self, recursos=int, nombre=str, puntos_vida=float, ataque=float):
        super().__init__(recursos, nombre, puntos_vida, ataque)





class TropaAlcance(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Ataque"
    '''
    def __init__(self, recursos=int, nombre=str, puntos_vida=float, ataque=float):
        super().__init__(recursos, nombre, puntos_vida, ataque)


# TROPAS DE ATAQUE
class Soldado(TropaAtaque):

    def __init__(self, recursos=50, nombre='soldado', puntos_vida=100, ataque=100):
        super().__init__(recursos,nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()

class Caballero(TropaAtaque):

    def __init__(self, recursos= 70, nombre='caballero', puntos_vida=200, ataque=85):
        super().__init__( recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()
# TROPAS DE DEFENSA
class Ogro(TropaDefensa):

    def __init__(self, recursos=80, nombre='ogro', puntos_vida=250, ataque=60):
        super().__init__( recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()

class Escudero(TropaDefensa):

    def __init__(self, recursos=50, nombre='escudero', puntos_vida=150, ataque=50):
        super().__init__(recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()

# TROPAS DE ALCANCE
class Arquero(TropaAlcance):

    def __init__(self,  recursos=80, nombre='arquero', puntos_vida=50, ataque=150):
        super().__init__( recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()


class Ballestero(TropaAlcance):

    def __init__(self, recursos=100, nombre='ballestero', puntos_vida=300, ataque=70):
        super().__init__( recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()


class Mago(TropaAlcance):

    def __init__(self, recursos=110, nombre='mago', puntos_vida=100, ataque=110):
        super().__init__(recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()


class Catapulta(TropaAlcance):

    def __init__(self, recursos=350, nombre='catapulta', puntos_vida=400, ataque=200):
        super().__init__(recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()

"""



#!!!!!!!!!!!!!!!!
#CODIGO DE PRUEBA PARA EL COMBATE, ES NECESARIO REGIONES Y TROPAS PARA EJECUTAR
#!!!!!!!!!!!!!!!!
"""
Region.Regiones[(0,0)]=Region((0,0),'terreno',False) #Creamos dos regiones vacias
Region.Regiones[(0,1)]=Region((0,1),'terreno',False)


Region.agregar_tropa(Region.Regiones[(0,0)],'ballestero',5) #Añadimos tropas a cada region

Region.agregar_tropa(Region.Regiones[(0,0)],'caballero',5)

Region.agregar_tropa(Region.Regiones[(0,0)],'ogro',5)

Region.agregar_tropa(Region.Regiones[(0,1)],'catapulta',2)

Region.agregar_tropa(Region.Regiones[(0,1)],'mago',5)

Region.agregar_tropa(Region.Regiones[(0,1)],'ogro',5)

Region.agregar_tropa(Region.Regiones[(0,1)],'escudero',5)

import random    #Vamos a emplear la libreria random
"""
import Region
import Tropa
class Batalla:
    '''
    Clase dedicada al desarrollo del combate

    ATRIBUTOS
    ------------
    La clase no presenta constructor, ya que solo usa staticmethods.

    METODOS
    -----------
    preparacion_combate: Metodo que cogerá las posiciones de las regiones que se van a enfrentar, a continuación crea los ejercitos que se van a enfrentar

    combate: Metodo que debe recoger dos listas con los ejercitos que se van a enfrentar y calculará quien ha ganado


    '''
    @staticmethod
    def preparacion_combate(posAtk:tuple,posDef:tuple):
        '''
        PARAMETROS
        --------------
        posAtk: tuple
        coordenadas de la zona que va a atacar

        posDef: tuple
        coordenadas de la zona que va a defender
        '''

        tropas_def =Region.Regiones[posDef]._tropas  #Recogemos las tropas que hay en la posicion 'popDef'
        tropas_atk=Region.Regiones[posAtk]._tropas   #Recogemos las tropas que hay en la posicion 'posAtk'

        Ejercito_Atk = []      #Inicializamos una lista que nos servirá para almacenar las tropas que atacarán
        Ejercito_Def = []      #Inicializamos una lista que nos servirá para almacenar las tropas que defenderán

        for _ in range(0,len(tropas_def.keys())):      #Añadimos listas vacias dentro de la lista Ejercito_Atk/Def para rellenarlas
            Ejercito_Def.append([])

        for _ in range(0,len(tropas_atk.keys())):
            Ejercito_Atk.append([])

        for keys_tropasAtk in tropas_atk.keys():                        #Rellenamos las listas de manera aleatoria
            orden_random=random.randint(0,len(Ejercito_Atk)-1)

            while Ejercito_Atk[orden_random]!=[]:                      #Crea numero aleatorios hasta que encuentra una lista que no esté llena
                orden_random = random.randint(0, len(Ejercito_Atk)-1)

            Ejercito_Atk[orden_random].append(keys_tropasAtk)            #Añade el nombre de la tropa
            Ejercito_Atk[orden_random].append(tropas_atk[keys_tropasAtk])  #Añade el número de tropas

        for keys_tropasDef in tropas_def.keys():                      #Rellenamos las listas de manera aleatoria
            orden_random = random.randint(0, len(Ejercito_Def) - 1)

            while Ejercito_Def[orden_random] != []:                    #Crea numero aleatorios hasta que encuentra una lista que no esté llena
                orden_random = random.randint(0, len(Ejercito_Def) - 1)

            Ejercito_Def[orden_random].append(keys_tropasDef)              #Añade el nombre de la tropa
            Ejercito_Def[orden_random].append(tropas_def[keys_tropasDef])   #Añade el número de tropas

        return Ejercito_Atk,Ejercito_Def      #Devolvemos los ejercitos creados, con sus tropas ordenadas de manera aleatoria


    @staticmethod

    def combate(Ejercito_Atk:list,Ejercito_Def:list):
        '''
            PARAMETROS
            ------------
            Ejercito_Atk: list
            lista con las tropas del ejercito de ataque (proporcionada por el metodo "preparacion_combate)"

            Ejercito_Def: list
            lista con las tropas del ejercito de defensa (proporcionada por el metodo "preparacion_combate)"

        '''

        print(Ejercito_Atk)
        print(Ejercito_Def)
        Tropa.rellenar_tropa_stats()       #Rellenamos el diccionario tropa_stats de la clase Tropa, para poder coger las estadisticas de cada tropa
        print(Tropa.tropa_stats)
        ejercito_vivo = 'Ninguno'         #Inicializamos la variable como si no hubiese ningún ejercito vivo, para así calcular estadisticas de las primeras filas




        '''
                    TABLA PARA LAS VENTAJAS POR TIPO DE TROPA
                    -------------------------------------------------
                          |       Ataque     |      Defensa       |       Alcance
                      ------------------------------------------------------------------                  
                          |                  |                    |
                Ataque    |       neutro     |      debil         |       fuerte
                          |                  |                    |
                       ------------------------------------------------------------------                
                          |                  |                    |
                Defensa   |      fuerte      |       netro        |       debil
                          |                  |                    |
                        -----------------------------------------------------------------
                          |                  |                    |
                Alcance   |      debil       |        fuerte      |       neutro
                          |                  |                    |
                        ----------------------------------------------------------------

                    la ventaja de las tropas de ataque es un bonus en daño
                    la ventaja de las tropas de defensa es un bonus en vida
                    la ventaja de las tropas de alcance es un pequeño bonus en ambas
                    '''





        while Ejercito_Atk!=[] and Ejercito_Def!=[]:    #El bucle se repetirá hasta que uno de los ejercitos esté vacio


            if ejercito_vivo == 'Def' or ejercito_vivo == 'Ninguno':    #Esto se ejecutará al principio, o si la linea anterior de ejercito ha muerto
                Ataque_Atk = Tropa.tropa_stats[Ejercito_Atk[0][0]].ataque * Ejercito_Atk[0][1]          #Calculamos el ataque de la siguiente linea del ejercito
                print(Ataque_Atk)
                if isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]],TropaAtaque) and isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]],TropaAlcance):    #Si se trata de una situación de ventaja aplicamos bonus
                    Ataque_Atk+= (Ataque_Atk*0.2)//1               #Aplicamos el bonus por tipo
                    print('Ataque vs Alcance',Ataque_Atk)

                elif isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]], TropaAlcance) and isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]], TropaDefensa): #Si se trata de una situación de ventaja aplicamos bonus
                    Ataque_Atk += (Ataque_Atk * 0.1) // 1         #Aplicamos el bonus por tipo
                    print('Alcance vs Defensa', Ataque_Atk)

            if ejercito_vivo == 'Atk' or ejercito_vivo == 'Ninguno': #Esto se ejecutará al principio, o si la linea anterior de ejercito ha muerto

                Ataque_Def = Tropa.tropa_stats[Ejercito_Def[0][0]].ataque * Ejercito_Def[0][1]       #Calculamos la vida de la siguiente linea del ejercito
                print(Ataque_Def)

                if isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]],TropaAtaque) and isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]],TropaAlcance): #Si se trata de una situación de ventaja aplicamos bonus
                    Ataque_Atk+= (Ataque_Atk*0.2)//1       #Aplicamos el bonus por tipo
                    print('Ataque vs Alcance', Ataque_Def)

                elif isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]], TropaAlcance) and isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]], TropaDefensa): #Si se trata de una situación de ventaja aplicamos bonus
                    Ataque_Atk += (Ataque_Atk * 0.1) // 1         #Aplicamos el bonus por tipo
                    print('Alcance vs Defensa', Ataque_Def)

            if ejercito_vivo == 'Def' or ejercito_vivo == 'Ninguno': #Esto se ejecutará al principio, o si la linea anterior de ejercito ha muerto

                Vida_Atk = Tropa.tropa_stats[Ejercito_Atk[0][0]].puntos_vida * Ejercito_Atk[0][1]         #Calculamos la vida de la siguiente linea del ejercito
                print(Vida_Atk)
                if isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]],TropaDefensa) and isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]],TropaAtaque): #Si se trata de una situación de ventaja aplicamos bonus
                    Vida_Atk+= (Vida_Atk*0.2)//1     #Aplicamos el bonus por tipo
                    print('Defensa vs Ataque', Vida_Atk)

                elif isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]], TropaAlcance) and isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]], TropaDefensa): #Si se trata de una situación de ventaja aplicamos bonus
                    Vida_Atk += (Vida_Atk * 0.1) // 1       #Aplicamos el bonus por tipo
                    print('Alcance vs Defensa', Vida_Atk)

            if ejercito_vivo == 'Atk' or ejercito_vivo == 'Ninguno': #Esto se ejecutará al principio, o si la linea anterior de ejercito ha muerto

                Vida_Def = Tropa.tropa_stats[Ejercito_Def[0][0]].puntos_vida * Ejercito_Def[0][1]       #Calculamos la vida de la siguiente linea del ejercito
                print(Vida_Def)
                if isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]],TropaDefensa) and isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]],TropaAtaque): #Si se trata de una situación de ventaja aplicamos bonus
                    Vida_Def+= (Vida_Def*0.2)//1         #Aplicamos el bonus por tipo
                    print('Defensa vs Ataque', Vida_Def)

                elif isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]], TropaAlcance) and isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]], TropaDefensa): #Si se trata de una situación de ventaja aplicamos bonus
                    Vida_Def += (Vida_Def * 0.1) // 1          #Aplicamos el bonus por tipo
                    print('Alcance vs Defensa', Vida_Def)


            while Vida_Atk > 0 and Vida_Def > 0:     #Se ejecutará hasta que una de las filas de los ejercitos tenga vida=0 o negativa (es decir, ha muerto)


                Vida_Atk-=Ataque_Def      #El ejercito atacante causa daño
                print(Vida_Atk)
                Vida_Def-=Ataque_Atk      #El ejercito defensor causa daño
                print(Vida_Def)

                if Vida_Atk <= 0:         #Si se muere el ejercito atacante...
                    print(Ejercito_Atk)
                    print(Ejercito_Atk[0][0],'Ha sido derrotado (Atk)')
                    Ejercito_Atk.remove(Ejercito_Atk[0])     #Eliminamos de la lista las tropas muertas
                    print(Ejercito_Atk)
                    ejercito_vivo='Def'         #Indicamos que el ejercito que sigue vivo es el defensor (para no calcular de nuevo sus estadisticas iniciales)

                if Vida_Def <= 0:          #Si se muere el ejercito defensor...
                    print(Ejercito_Def)
                    print(Ejercito_Def[0][0], 'Ha sido derrotado (Def)')
                    Ejercito_Def.remove(Ejercito_Def[0])  #Eliminamos de la lista las tropas muertas
                    print(Ejercito_Def)
                    ejercito_vivo = 'Atk'     #Indicamos que el ejercito que sigue vivo es el atacante (para no calcular de nuevo sus estadisticas iniciales)

                if Vida_Def <= 0 and Vida_Atk <= 0:  #Si en el mismo turno han muerto las lineas de los dos ejercitos...
                    ejercito_vivo ='Ninguno'   #Indicamos que ningún ejertito está vivo (para calcular estadisticas iniciales de la siguiente fila)

            if Ejercito_Atk==[] and Ejercito_Def==[]:      #Si el ejercito de ataque y defensa han muerto a la vez...
                print('AMBOS EJERCITOS HAN MUERTO EN BATALLA')
                return 1
            elif Ejercito_Atk==[]:
                print('LA DEFENSA HA SIDO EFECTIVA')     #Si el ejercito de ataque ha muerto...
                return 2
            elif Ejercito_Def==[]:
                print('LA ZONA HA SIDO CAPTURADA')        #Si el ejercito de defensa ha muerto...
                return 3




Ejercito_Atk,Ejercito_Def=Batalla.preparacion_combate((0,0),(0,1))
Batalla.combate(Ejercito_Atk,Ejercito_Def)
