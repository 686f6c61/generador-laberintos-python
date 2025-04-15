# Generador de laberintos

![Laberinto](/assets/laberinto.png)

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2C2D72?style=for-the-badge&logo=pygame&logoColor=white)](https://www.pygame.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)

Un juego de laberintos generados proceduralmente con diferentes niveles de dificultad. Navega a través de complejos laberintos generados mediante algoritmos avanzados y encuentra la salida antes de que se acabe el tiempo.

## Versión

**Versión:** 0.2  
**Fecha:** Abril 2025  
**Creador:** [686f6c61](https://github.com/686f6c61)

## Características

- **Generación procedural de laberintos**: Cada partida es única gracias al algoritmo de generación basado en DFS (Depth-First Search)
- **Múltiples niveles de dificultad**: Desde fácil hasta extremo, con laberintos de tamaño y complejidad crecientes
- **Interfaz gráfica intuitiva**: Menús de navegación sencillos y visualización clara del laberinto
- **Indicador de dirección**: Flecha que apunta hacia la meta cuando no está visible en pantalla
- **Sistema de tiempo**: Contrarreloj para añadir presión y desafío
- **Controles sencillos**: Movimiento con las flechas del teclado

## Niveles de dificultad

- **Fácil**: 15x15 celdas, complejidad y densidad bajas
- **Normal**: 25x25 celdas, complejidad y densidad medias
- **Difícil**: 35x35 celdas, complejidad y densidad altas
- **Muy difícil**: 45x45 celdas, complejidad y densidad muy altas
- **Extremo**: 55x55 celdas, complejidad y densidad extremas

## Estructura del proyecto

```
laberinto/
├── assets/              # Recursos gráficos
├── src/                 # Código fuente
│   ├── configuracion/   # Configuraciones del juego
│   ├── generador/       # Algoritmos de generación de laberintos
│   ├── jugador/         # Lógica del personaje jugable
│   ├── renderizador/    # Renderizado de gráficos y pantallas
│   ├── utilidades/      # Funciones de utilidad
│   └── main.py          # Punto de entrada principal
├── requirements.txt     # Dependencias del proyecto
└── run.sh              # Script para ejecutar el juego
```

## Requisitos

- Python 3.x
- Pygame 2.5.2
- Numpy 1.26.0

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python src/main.py
```

o

```bash
./run.sh
```

## Controles

- **Flechas direccionales**: Mover al personaje
- **Botón Menú**: Volver al menú principal durante el juego
- **ESC**: Salir del juego

## Algoritmo de generación

El laberinto se genera utilizando una versión modificada del algoritmo de búsqueda en profundidad (DFS). Este algoritmo garantiza que siempre exista al menos un camino entre cualquier par de celdas del laberinto. Además, se añaden características adicionales como:

- Generación de callejones sin salida
- Creación de ciclos y rutas alternativas
- Posicionamiento estratégico de inicio y meta

## Licencia

Este proyecto está disponible como código abierto.

## Cómo jugar

1. Selecciona la dificultad en el menú principal
2. Usa las flechas del teclado para mover al personaje
3. Encuentra el camino desde el punto rojo (inicio) hasta el punto verde (meta)
4. Completa el laberinto antes de que se acabe el tiempo

## Niveles de dificultad

- **Fácil**: Laberinto pequeño (10x10) con tiempo generoso
- **Normal**: Laberinto mediano (15x15) con complejidad moderada
- **Difícil**: Laberinto grande (20x20) con mayor complejidad
- **Muy difícil**: Laberinto más grande (25x25) con alta complejidad
- **Extremo**: Laberinto enorme (30x30) con máxima complejidad

## Estructura del proyecto

```
laberinto/
├── src/                    # Código fuente
│   ├── configuracion/      # Configuración global
│   ├── generador/          # Generación de laberintos
│   ├── jugador/            # Lógica del jugador
│   ├── renderizador/       # Interfaz gráfica
│   ├── utilidades/         # Funciones auxiliares
│   └── main.py             # Punto de entrada
├── assets/                 # Recursos gráficos y sonidos
├── docs/                   # Documentación
├── requirements.txt        # Dependencias
├── run.sh                  # Script de ejecución
└── README.md               # Este archivo
```

## Licencia

Este proyecto es de código abierto y está disponible para cualquier uso educativo o personal.
