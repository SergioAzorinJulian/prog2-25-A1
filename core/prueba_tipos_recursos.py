from core.recursos import Recurso

'''En este fichero voy a comprobar que la clase que he creado en recursos.py funciona'''

recurso1= Recurso('madera', 600, 100)
print(recurso1)
print(Recurso.creados)
datos = {'nombre': 'agua', 'cantidad': 200, 'regeneracion': 50}
recurso2 = Recurso.desde_dict(datos)
print(recurso2)
print(Recurso.creados)
print(recurso1.to_dict())

recurso1.__isub__(20)
print(recurso1)
recurso2.__iadd__(10)
print(recurso2)
print(Recurso.creados)
recurso1.regenerar()
print(repr(recurso1))