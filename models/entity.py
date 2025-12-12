import pygame
from utils.settings import TILE_SIZE

class Entity:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.color = color

class Player(Entity):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.history = [] 
        
        # --- DÜZELTME BURADA ---
        # Eskiden 0.8 idi, şimdi 0.65 yaptık.
        # Bu sayede kapılardan geçerken sağa sola takılma payı oluştu.
        size = int(TILE_SIZE * 0.65) 
        
        offset = (TILE_SIZE - size) // 2
        self.rect = pygame.Rect(x + offset, y + offset, size, size)

    def record_position(self):
        self.history.append(self.rect.topleft)

class Ghost(Entity):
    def __init__(self, history, color):
        super().__init__(0, 0, color)
        self.history = history
        # Hayalet de oyuncuyla aynı boyutta olsun
        size = int(TILE_SIZE * 0.65)
        self.rect = pygame.Rect(0, 0, size, size)
        if history: self.rect.topleft = history[0]

    def update_position_from_history(self, frame):
        if frame < len(self.history):
            self.rect.topleft = self.history[frame]
        else:
            if self.history: self.rect.topleft = self.history[-1]

class Wall(Entity): pass

class Box(Entity):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        pad = 2
        self.rect = pygame.Rect(x+pad, y+pad, TILE_SIZE-pad*2, TILE_SIZE-pad*2)

class Exit(Entity):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        size = int(TILE_SIZE * 0.5)
        offset = (TILE_SIZE - size) // 2
        self.rect = pygame.Rect(x + offset, y + offset, size, size)

class Button(Entity):
    def __init__(self, x, y, color, link_id):
        super().__init__(x, y, color)
        self.link_id = link_id
        self.is_pressed = False
        self.was_occupied = False 
        size = int(TILE_SIZE * 0.6)
        offset = (TILE_SIZE - size) // 2
        self.rect = pygame.Rect(x + offset, y + offset, size, size)

class Door(Entity):
    def __init__(self, x, y, color, link_id):
        super().__init__(x, y, color)
        self.link_id = link_id
        self.is_open = False
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

class Laser(Entity):
    def __init__(self, x, y, color, axis):
        super().__init__(x, y, color)
        self.axis = axis 
        self.active = True
        thickness = int(TILE_SIZE * 0.25)
        center = (TILE_SIZE - thickness) // 2
        if self.axis == 'V': 
            self.rect = pygame.Rect(x + center, y, thickness, TILE_SIZE)
        else: 
            self.rect = pygame.Rect(x, y + center, TILE_SIZE, thickness)