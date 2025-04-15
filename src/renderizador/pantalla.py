"""
Módulo de renderizado para el generador de laberintos.

Este módulo contiene las clases para manejar la interfaz gráfica del juego,
incluyendo la pantalla principal, menús y efectos visuales.
"""

import pygame
from typing import Tuple, List, Dict, Any, Optional, Callable

from configuracion.config import (
    ANCHO_VENTANA, ALTO_VENTANA, FPS, NEGRO, BLANCO, GRIS, 
    ROJO, VERDE, AZUL, AMARILLO, CELESTE, NARANJA, MORADO,
    TAMANO_FUENTE_PEQUENA, TAMANO_FUENTE_MEDIANA, TAMANO_FUENTE_GRANDE,
    NIVELES_DIFICULTAD, TITULO, TAMANO_CELDA
)
from utilidades.helpers import dibujar_texto, formatear_tiempo, Temporizador, calcular_centro_celda


class Boton:
    """
    Clase que representa un botón interactivo en la interfaz.
    """
    
    def __init__(self, x: int, y: int, ancho: int, alto: int, texto: str, 
                 color: Tuple[int, int, int] = AZUL, 
                 color_hover: Tuple[int, int, int] = CELESTE,
                 tamano_fuente: int = TAMANO_FUENTE_MEDIANA):
        """
        Inicializa un nuevo botón.
        
        Args:
            x: Coordenada x del centro del botón.
            y: Coordenada y del centro del botón.
            ancho: Ancho del botón en píxeles.
            alto: Alto del botón en píxeles.
            texto: Texto a mostrar en el botón.
            color: Color del botón en formato RGB.
            color_hover: Color del botón cuando el ratón está encima.
            tamano_fuente: Tamaño de la fuente del texto.
        """
        self.rect = pygame.Rect(0, 0, ancho, alto)
        self.rect.center = (x, y)
        self.texto = texto
        self.color = color
        self.color_hover = color_hover
        self.tamano_fuente = tamano_fuente
        self.hover = False
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja el botón en la superficie proporcionada.
        
        Args:
            superficie: Superficie de pygame donde dibujar el botón.
        """
        color_actual = self.color_hover if self.hover else self.color
        
        # Dibujar rectángulo del botón
        pygame.draw.rect(superficie, color_actual, self.rect, border_radius=10)
        pygame.draw.rect(superficie, NEGRO, self.rect, 2, border_radius=10)
        
        # Dibujar texto del botón
        dibujar_texto(superficie, self.texto, self.tamano_fuente, 
                     *self.rect.center, BLANCO)
    
    def actualizar(self, pos_mouse: Tuple[int, int]) -> bool:
        """
        Actualiza el estado del botón según la posición del ratón.
        
        Args:
            pos_mouse: Tupla con las coordenadas (x, y) del ratón.
            
        Returns:
            True si el botón está siendo clickeado, False en caso contrario.
        """
        self.hover = self.rect.collidepoint(pos_mouse)
        return self.hover


class Menu:
    """
    Clase base para los diferentes menús del juego.
    """
    
    def __init__(self):
        """
        Inicializa un nuevo menú.
        """
        self.botones = []
    
    def manejar_evento(self, evento: pygame.event.Event) -> Optional[str]:
        """
        Maneja los eventos del menú.
        
        Args:
            evento: Evento de pygame a manejar.
            
        Returns:
            Acción a realizar o None si no hay acción.
        """
        return None
    
    def actualizar(self) -> Optional[str]:
        """
        Actualiza el estado del menú.
        
        Returns:
            Acción a realizar o None si no hay acción.
        """
        return None
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja el menú en la superficie proporcionada.
        
        Args:
            superficie: Superficie de pygame donde dibujar el menú.
        """
        pass


class MenuPrincipal(Menu):
    """
    Menú principal del juego.
    """
    
    def __init__(self):
        """
        Inicializa el menú principal.
        """
        super().__init__()
        
        # Crear botones
        centro_x = ANCHO_VENTANA // 2
        
        self.botones = [
            Boton(centro_x, 200, 300, 60, "Jugar", VERDE),
            Boton(centro_x, 300, 300, 60, "Seleccionar dificultad", AZUL),
            Boton(centro_x, 400, 300, 60, "Salir", ROJO)
        ]
        
        # Dificultad actual
        self.dificultad_actual = "normal"
        
        # Información de versión y creador
        self.version = "Versión: 0.2 - Abril 2025"
        self.creador = "Creador: github.com/686f6c61"
        self.fuente_info = pygame.font.Font(None, TAMANO_FUENTE_PEQUENA)
        self.texto_version = self.fuente_info.render(self.version, True, GRIS)
        self.texto_creador = self.fuente_info.render(self.creador, True, GRIS)
        self.rect_version = self.texto_version.get_rect(bottomleft=(10, ALTO_VENTANA - 30))
        self.rect_creador = self.texto_creador.get_rect(bottomleft=(10, ALTO_VENTANA - 10))
    
    def manejar_evento(self, evento: pygame.event.Event) -> Optional[str]:
        """
        Maneja los eventos del menú principal.
        
        Args:
            evento: Evento de pygame a manejar.
            
        Returns:
            Acción a realizar o None si no hay acción.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Clic izquierdo
            pos_mouse = pygame.mouse.get_pos()
            
            # Verificar clicks en botones
            if self.botones[0].actualizar(pos_mouse):
                return "jugar"
            elif self.botones[1].actualizar(pos_mouse):
                return "dificultad"
            elif self.botones[2].actualizar(pos_mouse):
                return "salir"
                
        return None
    
    def actualizar(self) -> Optional[str]:
        """
        Actualiza el estado del menú principal.
        
        Returns:
            Acción a realizar o None si no hay acción.
        """
        pos_mouse = pygame.mouse.get_pos()
        
        # Solo actualizar el estado hover de los botones
        for boton in self.botones:
            boton.actualizar(pos_mouse)
        
        return None
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja el menú principal en la superficie proporcionada.
        
        Args:
            superficie: Superficie de pygame donde dibujar el menú.
        """
        # Dibujar fondo
        superficie.fill(BLANCO)
        
        # Dibujar título
        dibujar_texto(superficie, "Generador de laberintos", TAMANO_FUENTE_GRANDE, 
                     ANCHO_VENTANA // 2, 100, NEGRO)
        
        # Dibujar botones
        for boton in self.botones:
            boton.dibujar(superficie)
        
        # Dibujar dificultad actual
        dibujar_texto(superficie, f"Dificultad: {self.dificultad_actual}", 
                     TAMANO_FUENTE_PEQUENA, ANCHO_VENTANA // 2, 500, NEGRO)
        
        # Dibujar información de versión y creador
        superficie.blit(self.texto_version, self.rect_version)
        superficie.blit(self.texto_creador, self.rect_creador)


class MenuDificultad(Menu):
    """
    Menú de selección de dificultad.
    """
    
    def __init__(self):
        """
        Inicializa el menú de dificultad.
        """
        super().__init__()
        
        # Crear botones para cada nivel de dificultad
        centro_x = ANCHO_VENTANA // 2
        y_inicial = 150
        espaciado = 70
        
        colores = [VERDE, AZUL, NARANJA, MORADO, ROJO]
        
        self.botones = []
        for i, dificultad in enumerate(NIVELES_DIFICULTAD.keys()):
            self.botones.append(
                Boton(centro_x, y_inicial + i * espaciado, 300, 50, 
                     dificultad.capitalize(), colores[i])
            )
        
        # Botón para volver al menú principal
        self.boton_volver = Boton(centro_x, y_inicial + len(self.botones) * espaciado + 50, 
                                 200, 50, "Volver", GRIS)
    
    def manejar_evento(self, evento: pygame.event.Event) -> Optional[Dict[str, Any]]:
        """
        Maneja los eventos del menú de dificultad.
        
        Args:
            evento: Evento de pygame a manejar.
            
        Returns:
            Diccionario con la acción y parámetros, o None si no hay acción.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Clic izquierdo
            pos_mouse = pygame.mouse.get_pos()
            
            # Verificar clicks en botones de dificultad
            for i, boton in enumerate(self.botones):
                if boton.actualizar(pos_mouse):
                    dificultad = list(NIVELES_DIFICULTAD.keys())[i]
                    return {"accion": "cambiar_dificultad", "dificultad": dificultad}
            
            # Verificar click en botón volver
            if self.boton_volver.actualizar(pos_mouse):
                return {"accion": "menu_principal"}
                
        return None
    
    def actualizar(self) -> Optional[Dict[str, Any]]:
        """
        Actualiza el estado del menú de dificultad.
        
        Returns:
            Diccionario con la acción y parámetros, o None si no hay acción.
        """
        pos_mouse = pygame.mouse.get_pos()
        
        # Solo actualizar el estado hover de los botones
        for boton in self.botones:
            boton.actualizar(pos_mouse)
        
        # Actualizar botón volver
        self.boton_volver.actualizar(pos_mouse)
        
        return None
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja el menú de dificultad en la superficie proporcionada.
        
        Args:
            superficie: Superficie de pygame donde dibujar el menú.
        """
        # Dibujar fondo
        superficie.fill(BLANCO)
        
        # Dibujar título
        dibujar_texto(superficie, "Seleccionar dificultad", TAMANO_FUENTE_GRANDE, 
                     ANCHO_VENTANA // 2, 80, NEGRO)
        
        # Dibujar botones de dificultad
        for boton in self.botones:
            boton.dibujar(superficie)
        
        # Dibujar botón volver
        self.boton_volver.dibujar(superficie)


class PantallaCarga:
    """
    Clase que representa la pantalla de carga.
    """
    
    def __init__(self, mensaje: str = "Cargando..."):
        """
        Inicializa la pantalla de carga.
        
        Args:
            mensaje: Mensaje a mostrar en la pantalla de carga.
        """
        self.mensaje = mensaje
        self.fuente = pygame.font.Font(None, TAMANO_FUENTE_MEDIANA)
        self.texto = self.fuente.render(self.mensaje, True, BLANCO)
        self.rect = self.texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
        
        # Información de versión y creador
        self.version = "Versión: 0.2 - Abril 2025"
        self.creador = "Creador: github.com/686f6c61"
        self.fuente_info = pygame.font.Font(None, TAMANO_FUENTE_PEQUENA)
        self.texto_version = self.fuente_info.render(self.version, True, GRIS)
        self.texto_creador = self.fuente_info.render(self.creador, True, GRIS)
        self.rect_version = self.texto_version.get_rect(bottomleft=(10, ALTO_VENTANA - 30))
        self.rect_creador = self.texto_creador.get_rect(bottomleft=(10, ALTO_VENTANA - 10))
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja la pantalla de carga.
        
        Args:
            superficie: Superficie de pygame donde dibujar la pantalla.
        """
        # Fondo
        superficie.fill(NEGRO)
        
        # Texto de carga
        superficie.blit(self.texto, self.rect)
        
        # Información de versión y creador
        superficie.blit(self.texto_version, self.rect_version)
        superficie.blit(self.texto_creador, self.rect_creador)


class PantallaJuego:
    """
    Pantalla principal del juego donde se muestra el laberinto.
    """
    
    def __init__(self, laberinto, jugador):
        """
        Inicializa la pantalla de juego.
        
        Args:
            laberinto: Instancia del laberinto a mostrar.
            jugador: Instancia del jugador.
        """
        self.laberinto = laberinto
        self.jugador = jugador
        
        # Temporizador
        self.temporizador = Temporizador()
        
        # Superficie para dibujar el laberinto (puede ser más grande que la ventana)
        self.superficie_laberinto = pygame.Surface((
            laberinto.columnas * TAMANO_CELDA,
            laberinto.filas * TAMANO_CELDA
        ))
        
        # Desplazamiento de la cámara
        self.camara_x = 0
        self.camara_y = 0
        
        # Estado del juego
        self.juego_terminado = False
        self.victoria = False
        
        # Botones
        centro_x = ANCHO_VENTANA // 2
        self.boton_reiniciar = Boton(centro_x - 100, ALTO_VENTANA - 50, 
                                    180, 40, "Reiniciar", AZUL)
        self.boton_menu = Boton(centro_x + 100, ALTO_VENTANA - 50, 
                               180, 40, "Menú principal", GRIS)
        
        # Botón para volver al menú durante el juego (en la esquina inferior izquierda)
        self.boton_volver_menu = Boton(70, ALTO_VENTANA - 20, 
                                      100, 30, "Menú", ROJO)
        
        # Información de versión y creador
        self.version = "Versión: 0.2 - Abril 2025"
        self.creador = "Creador: github.com/686f6c61"
        self.fuente_info = pygame.font.Font(None, TAMANO_FUENTE_PEQUENA)
        self.texto_version = self.fuente_info.render(self.version, True, GRIS)
        self.texto_creador = self.fuente_info.render(self.creador, True, GRIS)
        self.rect_version = self.texto_version.get_rect(bottomleft=(10, ALTO_VENTANA - 30))
        self.rect_creador = self.texto_creador.get_rect(bottomleft=(10, ALTO_VENTANA - 10))
    
    def reiniciar(self, tiempo_limite: Optional[int] = None) -> None:
        """
        Reinicia el juego.
        
        Args:
            tiempo_limite: Nuevo tiempo límite en segundos.
        """
        self.jugador.reiniciar()
        self.temporizador.reiniciar(tiempo_limite)
        self.juego_terminado = False
        self.victoria = False
    
    def manejar_evento(self, evento: pygame.event.Event) -> Optional[str]:
        """
        Maneja los eventos de la pantalla de juego.
        
        Args:
            evento: Evento de pygame a manejar.
            
        Returns:
            Acción a realizar o None si no hay acción.
        """
        # Manejar clic en el botón de volver al menú
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Clic izquierdo
            pos_mouse = pygame.mouse.get_pos()
            if self.boton_volver_menu.actualizar(pos_mouse):
                return "menu_principal"
        
        # Si el juego no ha terminado, pasar eventos al jugador
        if not self.juego_terminado:
            self.jugador.manejar_evento(evento)
        
        return None
    
    def actualizar(self) -> Optional[str]:
        """
        Actualiza el estado de la pantalla de juego.
        
        Returns:
            Acción a realizar o None si no hay acción.
        """
        pos_mouse = pygame.mouse.get_pos()
        
        # Actualizar estado del botón de volver al menú
        self.boton_volver_menu.actualizar(pos_mouse)
        
        # Si el juego ha terminado, verificar clicks en botones
        if self.juego_terminado:
            if self.boton_reiniciar.actualizar(pos_mouse) and pygame.mouse.get_pressed()[0]:
                self.reiniciar()
                return None
            elif self.boton_menu.actualizar(pos_mouse) and pygame.mouse.get_pressed()[0]:
                return "menu_principal"
        else:
            # Actualizar jugador
            self.jugador.actualizar()
            
            # Verificar victoria
            if self.jugador.ha_llegado_meta():
                self.juego_terminado = True
                self.victoria = True
            
            # Verificar tiempo agotado
            if self.temporizador.ha_terminado():
                self.juego_terminado = True
                self.victoria = False
            
            # Actualizar posición de la cámara para seguir al jugador
            self._actualizar_camara()
        
        return None
    
    def _actualizar_camara(self) -> None:
        """
        Actualiza la posición de la cámara para seguir al jugador.
        """
        # Obtener posición del jugador
        x, y = self.jugador.posicion
        
        # Calcular posición deseada de la cámara (centrada en el jugador)
        camara_deseada_x = x - ANCHO_VENTANA // 2
        camara_deseada_y = y - ALTO_VENTANA // 2
        
        # Limitar la cámara a los bordes del laberinto
        max_camara_x = max(0, self.superficie_laberinto.get_width() - ANCHO_VENTANA)
        max_camara_y = max(0, self.superficie_laberinto.get_height() - ALTO_VENTANA)
        
        # Suavizar el movimiento de la cámara (interpolación lineal)
        factor_suavizado = 0.1
        self.camara_x += (max(0, min(camara_deseada_x, max_camara_x)) - self.camara_x) * factor_suavizado
        self.camara_y += (max(0, min(camara_deseada_y, max_camara_y)) - self.camara_y) * factor_suavizado
        
        # Asegurar que los valores sean enteros para evitar problemas de renderizado
        self.camara_x = int(self.camara_x)
        self.camara_y = int(self.camara_y)
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja la pantalla de juego en la superficie proporcionada.
        
        Args:
            superficie: Superficie de pygame donde dibujar la pantalla.
        """
        # Limpiar superficie
        superficie.fill(BLANCO)
        
        # Dibujar laberinto en la superficie del laberinto
        self.superficie_laberinto.fill(BLANCO)
        self.laberinto.dibujar(self.superficie_laberinto)
        self.jugador.dibujar(self.superficie_laberinto)
        
        # Dibujar parte visible del laberinto en la superficie principal
        superficie.blit(self.superficie_laberinto, (0, 0), 
                       (self.camara_x, self.camara_y, ANCHO_VENTANA, ALTO_VENTANA))
        
        # Dibujar indicador de dirección hacia la meta si no está visible
        self._dibujar_indicador_meta(superficie)
        
        # Dibujar interfaz
        self._dibujar_interfaz(superficie)
        
        # Si el juego ha terminado, mostrar mensaje
        if self.juego_terminado:
            self._dibujar_fin_juego(superficie)
    
    def _dibujar_interfaz(self, superficie: pygame.Surface) -> None:
        """
        Dibuja la interfaz del juego (tiempo, botones, etc.).
        
        Args:
            superficie: Superficie de pygame donde dibujar la interfaz.
        """
        # Dibujar panel superior con tiempo
        pygame.draw.rect(superficie, GRIS, (0, 0, ANCHO_VENTANA, 40))
        
        # Dibujar tiempo transcurrido
        tiempo_transcurrido = self.temporizador.obtener_tiempo_transcurrido()
        texto_tiempo = f"Tiempo: {formatear_tiempo(tiempo_transcurrido)}"
        dibujar_texto(superficie, texto_tiempo, TAMANO_FUENTE_PEQUENA, 
                     ANCHO_VENTANA // 4, 20, BLANCO)
        
        # Dibujar tiempo restante si hay límite
        tiempo_restante = self.temporizador.obtener_tiempo_restante()
        if tiempo_restante is not None:
            texto_restante = f"Restante: {formatear_tiempo(tiempo_restante)}"
            color = VERDE if tiempo_restante > 30 else AMARILLO if tiempo_restante > 10 else ROJO
            dibujar_texto(superficie, texto_restante, TAMANO_FUENTE_PEQUENA, 
                         3 * ANCHO_VENTANA // 4, 20, color)
        
        # Dibujar información sobre la meta
        meta_x, meta_y = calcular_centro_celda(*self.laberinto.meta, TAMANO_CELDA)
        jugador_x, jugador_y = self.jugador.posicion
        distancia = int(((meta_x - jugador_x) ** 2 + (meta_y - jugador_y) ** 2) ** 0.5 / TAMANO_CELDA)
        
        texto_distancia = f"Distancia a meta: {distancia} celdas"
        # Usar un fondo negro para el texto para que se vea mejor
        pygame.draw.rect(superficie, NEGRO, (ANCHO_VENTANA // 2 - 120, 35, 240, 20))
        dibujar_texto(superficie, texto_distancia, TAMANO_FUENTE_PEQUENA, 
                     ANCHO_VENTANA // 2, 45, AMARILLO)
        
        # Dibujar panel inferior para botones
        pygame.draw.rect(superficie, GRIS, (0, ALTO_VENTANA - 40, ANCHO_VENTANA, 40))
        
        # Dibujar botón para volver al menú principal
        self.boton_volver_menu.dibujar(superficie)
        
        # Dibujar información de versión y creador
        superficie.blit(self.texto_version, self.rect_version)
        superficie.blit(self.texto_creador, self.rect_creador)
    
    def _dibujar_indicador_meta(self, superficie: pygame.Surface) -> None:
        """
        Dibuja un indicador de dirección hacia la meta cuando no está visible en la pantalla.
        
        Args:
            superficie: Superficie de pygame donde dibujar el indicador.
        """
        # Obtener posición de la meta en coordenadas del mundo
        meta_x, meta_y = calcular_centro_celda(*self.laberinto.meta, TAMANO_CELDA)
        
        # Convertir a coordenadas de pantalla
        meta_pantalla_x = meta_x - self.camara_x
        meta_pantalla_y = meta_y - self.camara_y
        
        # Verificar si la meta está fuera de la pantalla
        fuera_pantalla = (
            meta_pantalla_x < 0 or 
            meta_pantalla_x > ANCHO_VENTANA or 
            meta_pantalla_y < 40 or  # Considerar el panel superior
            meta_pantalla_y > ALTO_VENTANA
        )
        
        if fuera_pantalla:
            # Obtener posición del jugador en coordenadas de pantalla
            jugador_x, jugador_y = self.jugador.posicion
            jugador_pantalla_x = jugador_x - self.camara_x
            jugador_pantalla_y = jugador_y - self.camara_y
            
            # Calcular vector dirección hacia la meta
            dx = meta_x - jugador_x
            dy = meta_y - jugador_y
            
            # Normalizar el vector (convertirlo en un vector unitario)
            longitud = (dx**2 + dy**2)**0.5
            if longitud > 0:
                dx /= longitud
                dy /= longitud
            
            # Calcular posición del indicador (en el borde de la pantalla)
            # Margen para no dibujar exactamente en el borde
            margen = 30
            
            # Posición inicial del indicador (centro de la pantalla)
            indicador_x = ANCHO_VENTANA // 2
            indicador_y = ALTO_VENTANA // 2
            
            # Ajustar posición según la dirección
            if abs(dx) > abs(dy):  # Más horizontal que vertical
                if dx > 0:  # Meta a la derecha
                    indicador_x = ANCHO_VENTANA - margen
                else:  # Meta a la izquierda
                    indicador_x = margen
                # Ajustar y proporcionalmente
                indicador_y = ALTO_VENTANA // 2 + int((dy / dx) * (indicador_x - ANCHO_VENTANA // 2))
            else:  # Más vertical que horizontal
                if dy > 0:  # Meta abajo
                    indicador_y = ALTO_VENTANA - margen
                else:  # Meta arriba
                    indicador_y = 40 + margen  # Considerar panel superior
                # Ajustar x proporcionalmente
                if dy != 0:  # Evitar división por cero
                    indicador_x = ANCHO_VENTANA // 2 + int((dx / dy) * (indicador_y - ALTO_VENTANA // 2))
            
            # Limitar a los bordes de la pantalla
            indicador_x = max(margen, min(indicador_x, ANCHO_VENTANA - margen))
            indicador_y = max(40 + margen, min(indicador_y, ALTO_VENTANA - margen))
            
            # Dibujar flecha
            tamano_flecha = 15
            color_flecha = VERDE
            
            # Calcular puntos de la flecha
            # Punta de la flecha apuntando en la dirección correcta
            punta_x = indicador_x + int(dx * tamano_flecha)
            punta_y = indicador_y + int(dy * tamano_flecha)
            
            # Calcular puntos de la base de la flecha (perpendiculares a la dirección)
            perpendicular_x = -dy
            perpendicular_y = dx
            
            base1_x = indicador_x - int(perpendicular_x * tamano_flecha * 0.5)
            base1_y = indicador_y - int(perpendicular_y * tamano_flecha * 0.5)
            
            base2_x = indicador_x + int(perpendicular_x * tamano_flecha * 0.5)
            base2_y = indicador_y + int(perpendicular_y * tamano_flecha * 0.5)
            
            # Dibujar triángulo de la flecha
            pygame.draw.polygon(superficie, color_flecha, [
                (punta_x, punta_y),
                (base1_x, base1_y),
                (base2_x, base2_y)
            ])
            
            # Dibujar círculo en la base de la flecha
            pygame.draw.circle(superficie, color_flecha, (indicador_x, indicador_y), tamano_flecha // 2)
    
    def _dibujar_fin_juego(self, superficie: pygame.Surface) -> None:
        """
        Dibuja la pantalla de fin de juego.
        
        Args:
            superficie: Superficie de pygame donde dibujar la pantalla.
        """
        # Dibujar panel semitransparente
        panel = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 128))  # Negro semitransparente
        superficie.blit(panel, (0, 0))
        
        # Dibujar mensaje según resultado
        if self.victoria:
            mensaje = "¡Victoria!"
            color = VERDE
        else:
            mensaje = "¡Tiempo agotado!"
            color = ROJO
        
        dibujar_texto(superficie, mensaje, TAMANO_FUENTE_GRANDE, 
                     ANCHO_VENTANA // 2, ALTO_VENTANA // 3, color)
        
        # Dibujar tiempo total
        tiempo_total = self.temporizador.obtener_tiempo_transcurrido()
        texto_tiempo = f"Tiempo: {formatear_tiempo(tiempo_total)}"
        dibujar_texto(superficie, texto_tiempo, TAMANO_FUENTE_MEDIANA, 
                     ANCHO_VENTANA // 2, ALTO_VENTANA // 2, BLANCO)
        
        # Dibujar botones
        self.boton_reiniciar.dibujar(superficie)
        self.boton_menu.dibujar(superficie)
