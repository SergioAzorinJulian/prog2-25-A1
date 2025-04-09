
import random
import region
from tropas import *
from copy import deepcopy
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


"""

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
   # @staticmethod
    #def preparacion_combate(tropas_Atk:list,tropas_Def:list):
        '''
        PARAMETROS
        --------------
        posAtk: tuple
        coordenadas de la zona que va a atacar

        posDef: tuple
        coordenadas de la zona que va a defender
        '''







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

        ejercito_vivo = 'Ninguno'         #Inicializamos la variable como si no hubiese ningún ejercito vivo, para así calcular estadisticas de las primeras filas


        while Ejercito_Atk!=[] and Ejercito_Def!=[]:    #El bucle se repetirá hasta que uno de los ejercitos esté vacio




            for posicion in range(0,len(Ejercito_Atk)):
                Ejercito_Atk[posicion].atacar(Ejercito_Atk,Ejercito_Def)
            for posicion in range(0,len(Ejercito_Def)):
                Ejercito_Def[posicion].atacar(Ejercito_Def,Ejercito_Atk)
ejercito1=[]
ejercito1.append(deepcopy(Tropa.tropa_stats['soldado']))
ejercito1[0].cantidad=10

ejercito2=[]
ejercito1.append(deepcopy(Tropa.tropa_stats['arquero']))
ejercito1[0].cantidad=10

ejercito1.append(deepcopy(Tropa.tropa_stats['ogro']))
ejercito1[1].cantidad=10
Batalla.combate()





            '''
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
            '''


