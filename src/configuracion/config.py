"""
Módulo de configuración para el generador de laberintos.

Este módulo contiene todas las constantes y configuraciones utilizadas en el juego,
incluyendo colores, tamaños, niveles de dificultad y otras configuraciones globales.
"""

# Configuración de la ventana
TITULO = "Generador de laberintos"
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 60

# Colores (formato RGB)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (128, 128, 128)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
CELESTE = (0, 191, 255)
NARANJA = (255, 165, 0)
MORADO = (128, 0, 128)

# Configuración del laberinto
TAMANO_CELDA = 30
GROSOR_PARED = 2

# Configuración del jugador
VELOCIDAD_JUGADOR = 5
COLOR_JUGADOR = AZUL
TAMANO_JUGADOR = int(TAMANO_CELDA * 0.7)

# Configuración de la meta
COLOR_META = VERDE

# Configuración de dificultad
NIVELES_DIFICULTAD = {
    "facil": {
        "tamano": (15, 15),  # (filas, columnas)
        "complejidad": 0.5,  # Factor de complejidad (0-1)
        "densidad": 0.5,     # Densidad de paredes (0-1)
        "tiempo_limite": 120  # Tiempo en segundos
    },
    "normal": {
        "tamano": (25, 25),
        "complejidad": 0.6,
        "densidad": 0.6,
        "tiempo_limite": 180
    },
    "dificil": {
        "tamano": (35, 35),
        "complejidad": 0.7,
        "densidad": 0.7,
        "tiempo_limite": 240
    },
    "muy dificil": {
        "tamano": (45, 45),
        "complejidad": 0.8,
        "densidad": 0.8,
        "tiempo_limite": 300
    },
    "extremo": {
        "tamano": (55, 55),
        "complejidad": 0.9,
        "densidad": 0.9,
        "tiempo_limite": 360
    }
}

# Configuración de fuentes
TAMANO_FUENTE_PEQUENA = 20
TAMANO_FUENTE_MEDIANA = 30
TAMANO_FUENTE_GRANDE = 40

# Configuración de animaciones
DURACION_ANIMACION = 0.3  # segundos
