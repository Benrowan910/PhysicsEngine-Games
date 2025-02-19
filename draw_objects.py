import math
import pygame

# Slider class to control particle size
class Slider:
    def __init__(self, x, y, width, height, min_value, max_value):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value
        self.handle_rect = pygame.Rect(x, y - 5, 10, height + 10)
        self.is_dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.handle_rect)

    def update(self, mouse_pos, mouse_pressed):
        if self.handle_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            self.is_dragging = True
        if self.is_dragging:
            self.handle_rect.x = max(min(mouse_pos[0], self.rect.right - 10), self.rect.left)
            self.value = self.min_value + (self.handle_rect.x - self.rect.left) / (self.rect.width - 10) * (self.max_value - self.min_value)
        if not mouse_pressed[0]:
            self.is_dragging = False