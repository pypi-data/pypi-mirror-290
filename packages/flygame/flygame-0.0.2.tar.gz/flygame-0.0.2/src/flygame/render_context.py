# Programmed with <3 by fluffy

import pygame

from .color import Color

class RenderContext:
    def __init__(self, surface:pygame.Surface) -> None:
        self.__surface = surface

    def fill(self, color:Color) -> None:
        self.__surface.fill(color.pack())

    def line(self, color:Color, x_start:int, y_start:int, x_end:int, y_end:int, width:int=1) -> None:
        pygame.draw.line(self.__surface, color.pack(), (x_start, y_start), (x_end, y_end), width)

    def rect(self, color:Color, x:int, y:int, w:int, h:int, width:int=1) -> None:
        pygame.draw.rect(self.__surface, color.pack(), (x, y, w, h), width)