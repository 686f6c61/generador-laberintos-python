"""
Módulo principal del generador de laberintos.

Este módulo contiene la lógica principal del juego, incluyendo
la inicialización, el bucle principal y la gestión de estados.
"""

import sys
import pygame
from typing import Dict, Any, Optional

from configuracion.config import (
    ANCHO_VENTANA, ALTO_VENTANA, FPS, TITULO, NIVELES_DIFICULTAD
)
from generador.laberinto import Laberinto
from jugador.personaje import Jugador
from renderizador.pantalla import MenuPrincipal, MenuDificultad, PantallaJuego
from utilidades.helpers import Temporizador


class Juego:
    """
    Clase principal que gestiona el juego completo.
    
    Esta clase maneja la inicialización de pygame, la gestión de estados
    del juego y el bucle principal.
    """
    
    def __init__(self):
        """
        Inicializa el juego.
        """
        # Inicializar pygame
        pygame.init()
        pygame.display.set_caption(TITULO)
        
        # Crear ventana
        self.ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.reloj = pygame.time.Clock()
        
        # Estado actual del juego
        self.estado_actual = "menu_principal"
        
        # Dificultad actual
        self.dificultad_actual = "normal"
        
        # Crear menús
        self.menu_principal = MenuPrincipal()
        self.menu_dificultad = MenuDificultad()
        
        # Inicializar componentes del juego
        self._inicializar_juego()
    
    def _inicializar_juego(self) -> None:
        """
        Inicializa los componentes del juego según la dificultad seleccionada.
        """
        # Obtener configuración de dificultad
        config_dificultad = NIVELES_DIFICULTAD[self.dificultad_actual]
        
        # Crear laberinto
        filas, columnas = config_dificultad["tamano"]
        complejidad = config_dificultad["complejidad"]
        densidad = config_dificultad["densidad"]
        
        self.laberinto = Laberinto(filas, columnas, complejidad, densidad)
        
        # Crear jugador
        self.jugador = Jugador(self.laberinto)
        
        # Crear pantalla de juego
        self.pantalla_juego = PantallaJuego(self.laberinto, self.jugador)
        
        # Configurar tiempo límite
        tiempo_limite = config_dificultad["tiempo_limite"]
        self.pantalla_juego.temporizador.reiniciar(tiempo_limite)
        
        # Actualizar dificultad en el menú principal
        self.menu_principal.dificultad_actual = self.dificultad_actual
    
    def ejecutar(self) -> None:
        """
        Ejecuta el bucle principal del juego.
        """
        ejecutando = True
        
        while ejecutando:
            # Gestionar eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                
                # Pasar evento al estado actual
                self._manejar_evento_estado(evento)
            
            # Actualizar estado actual
            self._actualizar_estado()
            
            # Renderizar estado actual
            self._renderizar_estado()
            
            # Actualizar pantalla
            pygame.display.flip()
            
            # Controlar FPS
            self.reloj.tick(FPS)
        
        # Salir de pygame
        pygame.quit()
        sys.exit()
    
    def _manejar_evento_estado(self, evento: pygame.event.Event) -> None:
        """
        Maneja un evento según el estado actual del juego.
        
        Args:
            evento: Evento de pygame a manejar.
        """
        if self.estado_actual == "menu_principal":
            accion = self.menu_principal.manejar_evento(evento)
            if accion:
                if accion == "jugar":
                    self.estado_actual = "jugando"
                elif accion == "dificultad":
                    self.estado_actual = "dificultad"
                elif accion == "salir":
                    pygame.quit()
                    sys.exit()
        elif self.estado_actual == "dificultad":
            resultado = self.menu_dificultad.manejar_evento(evento)
            if resultado:
                accion = resultado.get("accion")
                if accion == "cambiar_dificultad":
                    self.dificultad_actual = resultado.get("dificultad")
                    self._inicializar_juego()
                    self.estado_actual = "menu_principal"
                elif accion == "menu_principal":
                    self.estado_actual = "menu_principal"
        elif self.estado_actual == "jugando":
            accion = self.pantalla_juego.manejar_evento(evento)
            if accion:
                if accion == "menu_principal":
                    self.estado_actual = "menu_principal"
    
    def _actualizar_estado(self) -> None:
        """
        Actualiza el estado actual del juego.
        """
        if self.estado_actual == "menu_principal":
            self.menu_principal.actualizar()
        
        elif self.estado_actual == "dificultad":
            self.menu_dificultad.actualizar()
        
        elif self.estado_actual == "jugando":
            accion = self.pantalla_juego.actualizar()
            if accion == "menu_principal":
                self.estado_actual = "menu_principal"
    
    def _renderizar_estado(self) -> None:
        """
        Renderiza el estado actual del juego.
        """
        if self.estado_actual == "menu_principal":
            self.menu_principal.dibujar(self.ventana)
        elif self.estado_actual == "dificultad":
            self.menu_dificultad.dibujar(self.ventana)
        elif self.estado_actual == "jugando":
            self.pantalla_juego.dibujar(self.ventana)


if __name__ == "__main__":
    # Crear y ejecutar juego
    juego = Juego()
    juego.ejecutar()
