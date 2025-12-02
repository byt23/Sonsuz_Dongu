# models/entity.py
import pygame

class Entity:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = color
        self.history = []

    def record_position(self):
        """Mevcut pozisyonu kaydeder."""
        self.history.append((self.rect.x, self.rect.y))

class Ghost(Entity):
    def __init__(self, history, color):
        start_x, start_y = history[0]
        super().__init__(start_x, start_y, color)
        self.full_history = history
    
    def update_position_from_history(self, frame_index):
        if frame_index < len(self.full_history):
            self.rect.x, self.rect.y = self.full_history[frame_index]

class Wall(Entity):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

class Button(Entity):
    def __init__(self, x, y, color, link_id):
        super().__init__(x, y, color)
        self.link_id = link_id
        self.is_pressed = False

class Door(Entity):
    def __init__(self, x, y, color, link_id):
        super().__init__(x, y, color)
        self.link_id = link_id
        self.is_open = False

class Exit(Entity):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)