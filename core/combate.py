

from tropas import *





class Batalla:


    @staticmethod
    def combate(Ejercito_Atk:list,Ejercito_Def:list):
        #print(Ejercito_Atk,Ejercito_Def)
        while Ejercito_Atk!=[] and Ejercito_Def!=[]:    #El bucle se repetirá hasta que uno de los ejercitos esté vacio
            print()
            max_tropas = max(len(Ejercito_Atk), len(Ejercito_Def))



            for i in range(max_tropas):
                if i < len(Ejercito_Atk):
                    Ejercito_Atk[i].atacar(Ejercito_Atk, Ejercito_Def)
                if i < len(Ejercito_Def):
                    Ejercito_Def[i].atacar(Ejercito_Def, Ejercito_Atk)

        if Ejercito_Atk!=[]:
            print('El ataque ha fallado')
            return False
        elif Ejercito_Def!=[]:
            print('El ataque ha sido un exito')
            return True


Soldado1=Soldado(5)
Arquero1=Arquero(5)
Gigante1=Gigante(5)
Soldado2=Soldado(5)
Arquero2=Arquero(5)

Ejercito_Atk=[Soldado1,Arquero1,Gigante1]
Ejercito_Def=[Soldado2,Arquero2]

Batalla.combate(Ejercito_Atk,Ejercito_Def)
