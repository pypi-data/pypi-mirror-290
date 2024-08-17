# Programmed with <3 by fluffy

import pygame
from . import Rect
from . import Surface
from .color import Color
from .font import Font

class RenderContext:
    def __init__(self, surface:Surface) -> None:
        self.__surface:pygame.Surface = surface

    def fill(self, color:Color) -> None:
        self.__surface.fill(color.pack())

    def line(self, color:Color, x_start:int, y_start:int, x_end:int, y_end:int, width:int=1) -> None:
        pygame.draw.line(self.__surface, color.pack(), (x_start, y_start), (x_end, y_end), width)

    def rect(self, color:Color, x:int, y:int, w:int, h:int, width:int=1) -> None:
        pygame.draw.rect(self.__surface, color.pack(), (x, y, w, h), width)

    def register_font(self, font_name:str, font_size:int, bold:bool=0, italic:bool=0) -> Font:
        return Font(font_name, font_size, pygame.font.SysFont(font_name, font_size, bold, italic), bold, italic)

    def blit(self, surface:Surface, x:int=0, y:int=0, area:Rect=None) -> None:
        self.__surface.blit(surface, (x, y), area)