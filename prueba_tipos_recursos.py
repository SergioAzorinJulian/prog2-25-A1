from tipos_recursos import Recurso

'''En este fichero voy a comprobar que la clase que he creado en tipos_recursos.py funciona'''

recurso1= Recurso('madera', 600, 100)
print(recurso1)
print(Recurso.creados)
datos = {'nombre': 'agua', 'cantidad': 200, 'regeneracion': 50}
recurso2 = Recurso.desde_dict(datos)
print(recurso2)
print(Recurso.creados)
print(recurso1.dict())