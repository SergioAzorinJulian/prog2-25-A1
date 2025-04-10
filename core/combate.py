from tropas import *

class Batalla:
    '''
Clase que contiene el bucle del combate
'''

    @staticmethod
    def combate(Ejercito_Atk:list,Ejercito_Def:list):
        '''

        Contiene el bucle de combate


        PARAMETROS
        ------------
        Ejercito_Atk: Ejercito que se dispone a atacar (lista formada por objetos tropa)

        Ejercito_Def: Ejercito que va a defender (lista formada por objetos tropa)

        '''

        while Ejercito_Atk!=[] and Ejercito_Def!=[]:    #El bucle se repetirá hasta que uno de los ejercitos esté vacio
            texto = ''
            max_tropas = max(len(Ejercito_Atk), len(Ejercito_Def)) #Cogemos la longitud del ejercito más grande
            for i in range(max_tropas):  #Repetimos el bucle hasta que lleguemos a la longitud del ejercito más grande

                if i < len(Ejercito_Atk):
                    texto += '\n'
                    texto+=Ejercito_Atk[i].atacar(Ejercito_Atk, Ejercito_Def)  #La tropa 'i' ataca al ejercito enemigo

                if i < len(Ejercito_Def):
                    texto += '\n'
                    texto+=Ejercito_Def[i].atacar(Ejercito_Def, Ejercito_Atk)  #La tropa 'i' ataca al ejercito enemigo


        if Ejercito_Atk==[]:    #Si el ejercito de ataque se ha quedado sin tropas...
            texto += '\n'
            texto+='Ataque fracaso'
            print(texto)
            return texto  #Devolvemos que el ataque ha sido un fracaso
        elif Ejercito_Def==[]:  #Si el ejercito de defensa se ha quedado sin tropas...
            texto+='\n'
            texto+='Ataque exitoso'
            print(texto)
            return texto    #Devolvemos que el ataque ha sido un exito



Soldado1=Soldado(3)
Arquero1=Arquero(2)
Arquero2=Arquero(5)
Gigante1=Gigante(3)
Gigante2=Gigante(2)
Soldado2=Soldado(3)

Soldado3=Soldado(5)
Canon1=Canon(1)
Ejercito_Atk=[Canon1,Arquero1]
Ejercito_Def=[Gigante1,Soldado1]

Batalla.combate(Ejercito_Atk,Ejercito_Def)

