# Programmed with <3 by fluffy

import pygame

class Mouse:
    def get_pos(self) -> tuple:
        return pygame.mouse.get_pos()

    def set_pos(self, x:int, y:int) -> None:
        pygame.mouse.set_pos((x, y))

    def show(self) -> None:
        pygame.mouse.set_visible(1)

    def hide(self) -> None:
        pygame.mouse.set_visible(0)