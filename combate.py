from tropas import *
class Combate:
    escenario_batalla={'atacantes':['','',''],'defensores':['','','']}
    @staticmethod
    def preparando_combate(tropas_ataque:dict,tropas_defensa:dict):

        Combate.escenario_batalla["atacantes"]=['','','']
        for j in range(1,3):
            for _ in range(0,2):
                if tropas_ataque[list(tropas_ataque.keys())[j]]==j+1:
                    Combate.escenario_batalla['atacantes'].append(list(tropas_ataque.keys())[j])



        Combate.escenario_batalla["defensores"] = ['','','']

        for i in range(1,3):
            for _ in range(0,2):
                if tropas_ataque[list(tropas_ataque.keys())[i]] == i:
                    Combate.escenario_batalla['defensores'].append(list(tropas_ataque.keys())[i])
        print(Combate.escenario_batalla)
    @staticmethod
    def inicio_combate(tropas_ataque:dict,tropas_defensa:dict):




Combate.preparando_combate(tropas_ataque,tropas_defensa)
Combate.inicio_combate(tropas_ataque,tropas_defensa)
























