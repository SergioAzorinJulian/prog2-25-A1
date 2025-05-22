# Kingdom Craft

Prepárate para la batalla en Kingdom Craft, un juego de estrategia medieval desarrollado para la asignatura Programación 2 (GIA). 
Gestiona recursos, alza majestuosos edificios y comanda tus tropas en combates estratégicos para conquistar el mapa y grabar tu nombre en la historia.

## Autores

* (Coordinador) [Sergio Azorín Julián](https://github.com/SergioAzorinJulian)
* [Mario Berná Berná](https://github.com/MarioBernaBerna)
* [María Cantó Cartagena](https://github.com/super170603)
* [José Francisco Hurtado Valero](https://github.com/jf-hurtado)
* [Tomás Marzullo](https://github.com/tomasMarzullo)
* [Carlos Peñalver Mora](https://github.com/carlos-pmora)

## Profesor
[//]:[Miguel A. Teruel](https://github.com/materuel-ua)

## Requisitos
[//]:  -Creación del mapa y las conexiones entre las distintas regiones (José Francisco Hurtado Valero) 

-Generación aleatoria de recursos y distribución por el mapa (José Francisco Hurtado Valero)

-Creación de un catálogo variado de tropas con distintos niveles y roles (Tomás Marzullo)

-Implementación de un sistema de combate estratégico (Sergio Azorín Julián) 

-Creación de los diferentes tipos de recursos (María Cantó Cartagena)

-Gestión de recursos y su procesamiento (Carlos Peñalver Mora) 

-Creación de los diferentes tipos de edificios y sus niveles (Carlos Peñalver Mora) 

-Creación y gestión de la API (Mario Berná Berná) 

-Cohesionar la lógica de la partida (Mario Berná Berná)

-Funcionalidades de guardado y carga de partida en formatos binario (Sergio Azorín Julián) 


## Instrucciones de instalación y ejecución

Sigue estos pasos para instalar y ejecutar Kingdom Craft en tu sistema operativo.

### Prerrequisitos

*   Python 3.x
*   pip (gestor de paquetes de Python)
*   Git

### Instalación

1.  **Clona el repositorio:**

    ```bash
    git clone https://github.com/SergioAzorinJulian/prog2-25-A1.git
    ```

2.  **Navega al directorio del proyecto:**

    ```bash
    cd prog2-25-A1
    ```

3.  **Crea un entorno virtual (recomendado):**

    *   **Linux/macOS:**

        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

    *   **Windows:**

        ```bash
        python -m venv .venv
        .venv\Scripts\activate
        ```

4.  **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

### Configuración de la Base de Datos (MySQL)

El proyecto utiliza MySQL para almacenar el ranking de usuarios y resúmenes de partidas.

1.  **Instala el Servidor MySQL:** Sigue la documentación oficial de MySQL para tu sistema operativo.
2.  **Crea una base de datos:** Crea una nueva base de datos para el juego (por ejemplo, `kingdom_craft_db`).
3.  **Configura la conexión a la base de datos:** Actualiza los detalles de conexión en el archivo `prog2-25-A1/core/mysql_base.py` con tus credenciales de MySQL y el nombre de la base de datos.

### Ejecución

    
1.  **Inicia la API de Flask:** 

    ```bash
    python prog2-25-A1/core/api.py
    ```

    La API se ejecutará por defecto en `http://127.0.0.1:5000/`.

    > NOTA:
    >Está en pythonanywhere activo hasta Agosto de 2025, por lo que este paso se debe omitir si se accede antes de esa fecha.

2.  **Ejecuta el juego:**

    Ejecuta el archivo principal del juego:

    ```bash
    python prog2-25-A1/core/ejemplo_definitivo.py
    ```

    Esto iniciará la interfaz interactiva del juego.

## Posibles mejoras

Basándonos en la implementación actual, se sugieren las siguientes mejoras:

*   **Mejora de la Interfaz Gráfica:** Desarrollar una interfaz gráfica de usuario más avanzada y atractiva utilizando Pygame u otra librería, mejorando la visualización del mapa y las interacciones.
*   **Ampliación de Contenido:** Introducir una mayor variedad de edificios con habilidades únicas y tropas con atributos y roles más diferenciados para aumentar la profundidad estratégica.
*   **Sistema de Combate Avanzado:** Implementar mecánicas de combate más complejas, incluyendo posicionamiento táctico, moral de las tropas y diferentes tipos de ataque/defensa.
*   **Inteligencia Artificial:** Desarrollar un sistema de IA para oponentes controlados por la máquina, permitiendo el juego en solitario.
*   **Funcionalidades Multijugador:** Mejorar la experiencia multijugador con combate en tiempo real, chat integrado y salas de espera para partidas.
*   **Mundos Persistentes:** Implementar un sistema para que los mundos de juego persistan y evolucionen incluso cuando los jugadores no estén conectados.
*   **Expansión del Comercio:** Ampliar el sistema del mercader ambulante con precios más dinámicos, objetos raros y rutas comerciales estratégicas.
*   **Eventos Aleatorios y Misiones:** Introducir eventos inesperados y misiones para ofrecer desafíos adicionales y recompensas a los jugadores.
*   **Manejo de Errores:** Implementar un manejo de errores más robusto y validaciones exhaustivas en todo el código.
*   **Refactorización del Código:** Realizar una refactorización del código para mejorar su organización, legibilidad y facilitar el mantenimiento.

## Resumen de la API

La API de Kingdom Craft proporciona una serie de puntos finales para gestionar usuarios, amigos, partidas y acciones dentro del juego. A continuación, se presenta un resumen de las funcionalidades principales:

### Autenticación

*   **Registro de usuario:**
    *   `POST /auth/signup`
    *   Parámetros: `user`, `password`
*   **Inicio de sesión:**
    *   `GET /auth/login`
    *   Parámetros: `user`, `password`
    *   Retorna un token JWT para futuras peticiones.

### Gestión de Usuarios

*   **Ranking global:**
    *   `GET /users/ranking`
    *   Requiere JWT.
    *   Retorna la lista de usuarios ordenada por ranking.
*   **Lista de amigos:**
    *   `GET /users/friends`
    *   Requiere JWT.
    *   Retorna la lista de amigos del usuario autenticado.
*   **Enviar solicitud de amistad:**
    *   `POST /users/friend-requests`
    *   Requiere JWT.
    *   Parámetros: `id_solicitud` (ID del usuario al que enviar la solicitud).
*   **Solicitudes de amistad recibidas:**
    *   `GET /users/friend-requests`
    *   Requiere JWT.
    *   Retorna la lista de usuarios que han enviado una solicitud.
*   **Aceptar solicitud de amistad:**
    *   `POST /users/friend-requests/<id>/accept`
    *   Requiere JWT.
    *   Parámetros: `id` (ID del usuario que envió la solicitud).
*   **Rechazar solicitud de amistad:**
    *   `POST /users/friend-requests/<id>/reject`
    *   Requiere JWT.
    *   Parámetros: `id` (ID del usuario que envió la solicitud).
*   **Notificaciones no leídas:**
    *   `GET /users/mail/notificaciones`
    *   Requiere JWT.
    *   Retorna el número de notificaciones nuevas.
*   **Marcar notificaciones como leídas:**
    *   `PUT /users/mail`
    *   Requiere JWT.
*   **Ver buzón de notificaciones:**
    *   `GET /users/mail`
    *   Requiere JWT.
    *   Retorna los mensajes no leídos.
*   **Invitaciones a partidas privadas:**
    *   `GET /users/game_requests`
    *   Requiere JWT.
    *   Retorna las partidas privadas a las que el usuario ha sido invitado.
*   **Mis partidas:**
    *   `GET /users/my_games`
    *   Requiere JWT.
    *   Retorna las partidas en las que participa el usuario.

### Gestión de Partidas

*   **Crear partida:**
    *   `POST /games`
    *   Requiere JWT.
    *   Parámetros (en el cuerpo de la petición JSON): `privada` (booleano), `invitado` (string, opcional si privada es True), `size` (int), `terrenos` (lista o string, opcional), `reino` (string).
*   **Partidas públicas disponibles:**
    *   `GET /games`
    *   Requiere JWT.
    *   Retorna las partidas públicas en estado "Esperando" a las que el usuario puede unirse.
*   **Unirse a partida:**
    *   `PUT /games/<id>/join`
    *   Requiere JWT.
    *   Parámetros: `id` (ID de la partida), `reino` (string).
*   **Iniciar partida:**
    *   `PUT /games/<id>/start`
    *   Requiere JWT.
    *   Parámetros: `id` (ID de la partida).
*   **Cancelar partida:**
    *   `POST /games/<id>/cancel`
    *   Requiere JWT.
    *   Parámetros: `id` (ID de la partida).
*   **Estado de la partida:**
    *   `GET /games/<id>/game_state`
    *   Requiere JWT.
    *   Parámetros: `id` (ID de la partida).
    *   Retorna el estado actual de la partida (`Esperando`, `Empezada`, `Finalizada`).
*   **Estado del jugador en partida:**
    *   `GET /games/<id>/player_state`
    *   Requiere JWT.
    *   Parámetros: `id` (ID de la partida).
    *   Retorna el estado del jugador autenticado en esa partida.
*   **Ganador de la partida:**
    *   `GET /games/<id>/winner`
    *   Requiere JWT.
    *   Parámetros: `id` (ID de la partida).
    *   Retorna el usuario ganador.

### Acciones en Partida (dentro de una partida específica `/games/<id>/player/`)

*   **Ver información de una zona:**
    *   `POST /games/<id>/player/ver_zona`
    *   Requiere JWT.
    *   Parámetros (en el cuerpo de la petición JSON): `zona` (tupla de enteros representando las coordenadas).
    *   Retorna información detallada de la región.
*   **Ver recursos del jugador:**
    *   `GET /games/<id>/player/ver_recursos`
    *   Requiere JWT.
    *   Parámetros: `id` (ID de la partida).
    *   Retorna la lista de recursos del jugador autenticado.
*   **Ver mapa gráfico del jugador:**
    *   `GET /games/<id>/player/ver_mapa`
    *   Requiere JWT.
    *   Parámetros: `id` (ID de la partida).
    *   Retorna una representación gráfica del mapa desde la perspectiva del jugador.
*   **Cambiar turno:**
    *   `PUT /games/<id>/player/cambiar_turno`
    *   Requiere JWT.
    *   Parámetros: `id` (ID de la partida).
*   **Ver catálogos (tropas y edificios):**
    *   `GET /games/<id>/player/catalogos`
    *   Requiere JWT.
    *   Parámetros: `id` (ID de la partida).
    *   Retorna los catálogos de tropas y edificios disponibles con sus costos y características.
*   **Añadir tropas:**
    *   `POST /games/<id>/player/add_tropa`
    *   Requiere JWT.
    *   Parámetros (en el cuerpo de la petición JSON): `tropa` (string, nombre de la tropa), `cantidad` (int).
*   **Mover tropa:**
    *   `PUT /games/<id>/player/mover_tropa`
    *   Requiere JWT.
    *   Parámetros (en el cuerpo de la petición JSON): `destino` (tupla de enteros, coordenadas de destino), `tropa` (string, nombre de la tropa), `cantidad` (int).
*   **Mover batallón completo:**
    *   `PUT /games/<id>/player/mover_batallon`
    *   Requiere JWT.
    *   Parámetros (en el cuerpo de la petición JSON): `destino` (tupla de enteros, coordenadas de destino).
*   **Construir edificio:**
    *   `POST /games/<id>/player/edificio`
    *   Requiere JWT.
    *   Parámetros (en el cuerpo de la petición JSON): `edificio` (string, nombre del edificio).
*   **Mejorar edificio:**
    *   `PUT /games/<id>/player/edificio`
    *   Requiere JWT.
    *   Parámetros (en el cuerpo de la petición JSON): `edificio` (string, nombre del edificio a mejorar).
*   **Combatir:**
    *   `PUT /games/<id>/player/combatir`
    *   Requiere JWT.
    *   Parámetros (en el cuerpo de la petición JSON): `atacantes` (tupla de enteros, coordenadas de la región atacante), `defensores` (tupla de enteros, coordenadas de la región defensora).
    *   Retorna el resultado del combate y el estado de la partida.
