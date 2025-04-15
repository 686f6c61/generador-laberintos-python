"""
Módulo de funciones auxiliares para el generador de laberintos.

Este módulo contiene funciones de utilidad que pueden ser usadas
por diferentes componentes del juego.
"""

import time
import pygame
from typing import Tuple, List, Dict, Any, Optional


def calcular_centro_celda(fila: int, columna: int, tamano_celda: int) -> Tuple[int, int]:
    """
    Calcula las coordenadas del centro de una celda en el laberinto.
    
    Args:
        fila: Número de fila de la celda.
        columna: Número de columna de la celda.
        tamano_celda: Tamaño de la celda en píxeles.
        
    Returns:
        Tupla con las coordenadas (x, y) del centro de la celda.
    """
    x = columna * tamano_celda + tamano_celda // 2
    y = fila * tamano_celda + tamano_celda // 2
    return (x, y)


def calcular_posicion_celda(x: int, y: int, tamano_celda: int) -> Tuple[int, int]:
    """
    Calcula la fila y columna de una celda a partir de coordenadas en píxeles.
    
    Args:
        x: Coordenada x en píxeles.
        y: Coordenada y en píxeles.
        tamano_celda: Tamaño de la celda en píxeles.
        
    Returns:
        Tupla con (fila, columna) de la celda.
    """
    fila = y // tamano_celda
    columna = x // tamano_celda
    return (fila, columna)


def formatear_tiempo(segundos: int) -> str:
    """
    Formatea un tiempo en segundos a formato mm:ss.
    
    Args:
        segundos: Tiempo en segundos.
        
    Returns:
        Cadena con el tiempo formateado como mm:ss.
    """
    minutos = segundos // 60
    segundos_restantes = segundos % 60
    return f"{minutos:02d}:{segundos_restantes:02d}"


def dibujar_texto(superficie: pygame.Surface, texto: str, tamano: int, 
                 x: int, y: int, color: Tuple[int, int, int], 
                 centrado: bool = True) -> None:
    """
    Dibuja texto en una superficie de pygame.
    
    Args:
        superficie: Superficie de pygame donde dibujar.
        texto: Texto a dibujar.
        tamano: Tamaño de la fuente.
        x: Coordenada x donde dibujar el texto.
        y: Coordenada y donde dibujar el texto.
        color: Color del texto en formato RGB.
        centrado: Si es True, el texto se centra en las coordenadas (x, y).
    """
    fuente = pygame.font.Font(None, tamano)
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect()
    
    if centrado:
        rect_texto.center = (x, y)
    else:
        rect_texto.topleft = (x, y)
        
    superficie.blit(superficie_texto, rect_texto)


def interpolar_color(color1: Tuple[int, int, int], 
                    color2: Tuple[int, int, int], 
                    factor: float) -> Tuple[int, int, int]:
    """
    Interpola entre dos colores según un factor.
    
    Args:
        color1: Color inicial en formato RGB.
        color2: Color final en formato RGB.
        factor: Factor de interpolación entre 0 y 1.
        
    Returns:
        Color interpolado en formato RGB.
    """
    r = int(color1[0] + (color2[0] - color1[0]) * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * factor)
    return (r, g, b)


class Temporizador:
    """Clase para manejar el tiempo transcurrido y límites de tiempo."""
    
    def __init__(self, tiempo_limite: Optional[int] = None):
        """
        Inicializa un nuevo temporizador.
        
        Args:
            tiempo_limite: Tiempo límite en segundos. Si es None, no hay límite.
        """
        self.tiempo_inicio = time.time()
        self.tiempo_limite = tiempo_limite
        self.tiempo_pausado = 0
        self.pausado = False
        self.tiempo_pausa_inicio = 0
    
    def reiniciar(self, tiempo_limite: Optional[int] = None) -> None:
        """
        Reinicia el temporizador.
        
        Args:
            tiempo_limite: Nuevo tiempo límite en segundos. Si es None, 
                          se mantiene el anterior.
        """
        self.tiempo_inicio = time.time()
        if tiempo_limite is not None:
            self.tiempo_limite = tiempo_limite
        self.tiempo_pausado = 0
        self.pausado = False
    
    def pausar(self) -> None:
        """Pausa el temporizador."""
        if not self.pausado:
            self.pausado = True
            self.tiempo_pausa_inicio = time.time()
    
    def reanudar(self) -> None:
        """Reanuda el temporizador si estaba pausado."""
        if self.pausado:
            self.tiempo_pausado += time.time() - self.tiempo_pausa_inicio
            self.pausado = False
    
    def obtener_tiempo_transcurrido(self) -> int:
        """
        Obtiene el tiempo transcurrido en segundos.
        
        Returns:
            Tiempo transcurrido en segundos (entero).
        """
        if self.pausado:
            return int(self.tiempo_pausa_inicio - self.tiempo_inicio - self.tiempo_pausado)
        return int(time.time() - self.tiempo_inicio - self.tiempo_pausado)
    
    def obtener_tiempo_restante(self) -> Optional[int]:
        """
        Obtiene el tiempo restante en segundos.
        
        Returns:
            Tiempo restante en segundos o None si no hay límite.
        """
        if self.tiempo_limite is None:
            return None
        
        tiempo_restante = self.tiempo_limite - self.obtener_tiempo_transcurrido()
        return max(0, tiempo_restante)
    
    def ha_terminado(self) -> bool:
        """
        Verifica si se ha agotado el tiempo.
        
        Returns:
            True si se ha agotado el tiempo, False en caso contrario.
        """
        if self.tiempo_limite is None:
            return False
        
        return self.obtener_tiempo_restante() <= 0
