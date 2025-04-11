"""
### PRUEBA 1 ###
try:
    # Importar las clases necesarias
    from core.mapa import Mapa

    # Inicializar el mapa con 5 filas y 5 columnas
    mapa = Mapa(5, 5)

    # Crear nodos y conexiones
    nodos = mapa.crear_nodos()
    conexiones = mapa.crear_aristas(nodos)

    # Asignar terrenos a los nodos
    mapa.anyadir_terreno(conexiones)

    # Asignar zonas y generar recursos
    mapa.asigna_zonas()

    # Mostrar el mapa con la distribución de terrenos
    print("Mapa con distribución de terrenos:")
    print(mapa)

    # Mostrar detalles de cada región
    print("\nDetalles de cada región:")
    for region in mapa.get_regiones().values():
        print(region)

    # Generar lugares aleatorios en el mapa
    mapa.region_manager.generar_lugares_aleatorios(cantidad=3)

    # Mostrar regiones con lugares especiales
    print("\nRegiones con lugares especiales:")
    for info in mapa.region_manager.mostrar_regiones_con_lugares():
        print(info)

except Exception as e:
    print(f"Error durante la ejecucion del mapa: {e}")
"""

"""
### PRUEBA 2 ###
try:
    # Importar las clases necesarias
    from core.mapa import Mapa
    from core.region_manager import RegionManager
    from core.region import Region

    # Inicializar el mapa con 5 filas y 5 columnas
    mapa = Mapa(5, 5)

    # Crear nodos y conexiones
    nodos = mapa.crear_nodos()
    conexiones = mapa.crear_aristas(nodos)

    # Asignar terrenos a los nodos
    mapa.anyadir_terreno(conexiones)

    # Asignar zonas y generar recursos
    mapa.asigna_zonas()

    # Mostrar el mapa con la distribución de terrenos
    print("Mapa con distribución de terrenos:")
    print(mapa)

    # Mostrar detalles de cada región
    print("\nDetalles de cada región:")
    for region in mapa.get_regiones().values():
        print(region)

    # Generar lugares especiales aleatoriamente en el mapa
    mapa.region_manager.generar_lugares_aleatorios(cantidad=3)

    # Mostrar regiones con lugares especiales
    print("\nRegiones con lugares especiales:")
    for info in mapa.region_manager.mostrar_regiones_con_lugares():
        print(info)

    # Asignar un propietario a una región específica
    region_especifica = list(mapa.get_regiones().values())[0]
    RegionManager.asignar_propietario_a_region(region_especifica, "Jugador1")
    print(f"\nPropietario asignado a la región {region_especifica.get_posicion()}: {region_especifica.get_propietario()}")

    # Verificar recursos faltantes y forzar su aparición
    mapa.region_manager.verificar_recursos_faltantes()

    # Mostrar detalles actualizados de cada región
    print("\nDetalles actualizados de cada región:")
    for region in mapa.get_regiones().values():
        print(region)

except Exception as e:
    print(f"Error durante la ejecución del mapa: {e}")
"""

""" 
### PRUEBA 3 ###
try:
    # Importar las clases necesarias
    from core.mapa import Mapa
    from core.region_manager import RegionManager
    from core.region import Region

    # Inicializar el mapa con 5 filas y 5 columnas
    mapa = Mapa(5, 5)

    # Crear nodos y conexiones
    nodos = mapa.crear_nodos()
    conexiones = mapa.crear_aristas(nodos)

    # Asignar terrenos a los nodos
    mapa.anyadir_terreno(conexiones)

    # Asignar zonas y generar recursos
    mapa.asigna_zonas()

    # Mostrar el mapa con la distribución de terrenos
    print("Mapa con distribución de terrenos:")
    print(mapa)

    # Mostrar detalles de cada región
    print("\nDetalles de cada región:")
    for region in mapa.get_regiones().values():
        print(region)

    # Generar lugares especiales aleatoriamente en el mapa
    mapa.region_manager.generar_lugares_aleatorios(cantidad=3)

    # Mostrar regiones con lugares especiales
    print("\nRegiones con lugares especiales:")
    for info in mapa.region_manager.mostrar_regiones_con_lugares():
        print(info)

    # Verificar recursos faltantes y forzar su aparición
    mapa.region_manager.verificar_recursos_faltantes()

    # Mostrar detalles actualizados de cada región
    print("\nDetalles actualizados de cada región:")
    for region in mapa.get_regiones().values():
        print(region)

except Exception as e:
    print(f"Error durante la ejecución del mapa: {e}")
"""
