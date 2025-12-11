import pygame
from utils.settings import TILE_SIZE

class Entity:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.color = color
        self.history = []

    def record_position(self):
        self.history.append((self.rect.x, self.rect.y))

class Player(Entity):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        # Hitbox ayarı
        hitbox_size = 50 
        offset = (TILE_SIZE - hitbox_size) // 2
        self.rect = pygame.Rect(x + offset, y + offset, hitbox_size, hitbox_size)

class Ghost(Entity):
    def __init__(self, history, color):
        start_x, start_y = history[0]
        super().__init__(start_x, start_y, color)
        hitbox_size = 50
        self.rect = pygame.Rect(start_x, start_y, hitbox_size, hitbox_size)
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
        
        self.is_pressed = False   # Butonun AÇIK/KAPALI durumu (Işık gibi)
        self.was_occupied = False # YENİ: Bir önceki karede üzerinde biri var mıydı?
        
        shrink = 20 
        self.rect = self.rect.inflate(-shrink*2, -shrink*2)

class Door(Entity):
    def __init__(self, x, y, color, link_id):
        super().__init__(x, y, color)
        self.link_id = link_id
        self.is_open = False

class Exit(Entity):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        shrink = 20
        self.rect = self.rect.inflate(-shrink*2, -shrink*2)