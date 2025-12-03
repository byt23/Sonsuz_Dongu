import pygame
import os
from models.entity import Entity, Player, Ghost, Wall, Button, Door, Exit
from utils.settings import *

class GameViewModel:
    def __init__(self):
        self.ghosts = [] 
        self.walls = []
        self.buttons = []
        self.doors = []
        self.exit_point = None
        self.start_pos = (100, 100)
        self.current_level_index = 1
        self.state = "BRIEFING" 
        
    def start_level(self):
        if self.state == "BRIEFING":
            print(f"--- LEVEL {self.current_level_index} BAŞLATILIYOR ---")
            self.state = "PLAYING"
            self._init_level(self.current_level_index)
            self.reset_game_state()

    def next_level(self):
        self.current_level_index += 1
        if self.current_level_index in STORY_TEXTS and self.current_level_index <= 7:
             self.state = "BRIEFING" 
        else:
             self.state = "GAME_FINISHED"

    def _init_level(self, level_num):
        print(f"--- HARİTA YÜKLENİYOR... ---")
        self.walls = []
        self.buttons = []
        self.doors = []
        self.ghosts = [] 
        self.exit_point = None

        try:
            file_path = os.path.join("levels", f"level{level_num}.txt")
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
            for row_index, line in enumerate(lines):
                for col_index, char in enumerate(line):
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    
                    if char == 'W': self.walls.append(Wall(x, y, COLOR_WALL))
                    elif char == 'P': self.start_pos = (x, y)
                    elif char == 'E': self.exit_point = Exit(x, y, COLOR_EXIT)
                    elif char == '1': self.buttons.append(Button(x, y, COLOR_BUTTON_1, link_id=1))
                    elif char == 'a': self.doors.append(Door(x, y, COLOR_DOOR_1, link_id=1))
                    elif char == '2': self.buttons.append(Button(x, y, COLOR_BUTTON_2, link_id=2))
                    elif char == 'b': self.doors.append(Door(x, y, COLOR_DOOR_2, link_id=2))

            print("--- HARİTA BAŞARIYLA OKUNDU ---")
        except FileNotFoundError:
            print("Level dosyası bulunamadı!")
            self.state = "GAME_FINISHED"
            self.walls = []

    def reset_game_state(self):
        if self.state == "PLAYING":
            start_x, start_y = self.start_pos
            self.player = Player(start_x, start_y, COLOR_PLAYER)
            self.current_frame = 0
            self.is_loop_ended = False

    def full_restart(self):
        self.ghosts = [] 
        self.state = "PLAYING"
        for btn in self.buttons: 
            btn.is_pressed = False
            btn.was_occupied = False # Restart atınca hafızayı sil
        for door in self.doors: door.is_open = False
        self.reset_game_state()
        print(f"LEVEL {self.current_level_index} RESETLENDİ")

    def handle_input(self, dx, dy):
        if self.state != "PLAYING": return
        if self.is_loop_ended: return

        next_rect = self.player.rect.copy()
        next_rect.x += dx * 5
        next_rect.y += dy * 5

        if self._can_move_to(next_rect):
            self.player.rect = next_rect

    def _can_move_to(self, rect):
        if rect.left < 0 or rect.right > VIRTUAL_WIDTH or rect.top < 0 or rect.bottom > VIRTUAL_HEIGHT:
            return False

        for wall in self.walls:
            if rect.colliderect(wall.rect): return False
        
        for door in self.doors:
            if not door.is_open and rect.colliderect(door.rect): return False
        
        return True

    def update(self):
        if self.state != "PLAYING": return

        if self.current_frame >= LOOP_DURATION:
            self.create_time_loop()
            return

        self.player.record_position()

        for ghost in self.ghosts:
            ghost.update_position_from_history(self.current_frame)

        self._update_mechanics()
        self._check_game_status()

        self.current_frame += 1

    def _update_mechanics(self):
        """AÇ/KAPA (TOGGLE) MANTIĞI"""
        
        for button in self.buttons:
            # 1. Şu an üzerinde biri var mı kontrol et
            is_currently_occupied = False
            
            if self.player.rect.colliderect(button.rect):
                is_currently_occupied = True
            
            for ghost in self.ghosts:
                if ghost.rect.colliderect(button.rect):
                    is_currently_occupied = True
            
            # 2. TOGGLE MANTIĞI:
            # Eğer şu an biri üzerindeyse VE bir önceki karede kimse yoksa
            # Bu "Yeni Basıldı" demektir -> Durumu değiştir.
            if is_currently_occupied and not button.was_occupied:
                button.is_pressed = not button.is_pressed # True ise False, False ise True yap
            
            # 3. Şimdiki durumu kaydet (Bir sonraki kare için 'geçmiş' olacak)
            button.was_occupied = is_currently_occupied
            
            # Renk Ayarı (Görsel için)
            button.color = COLOR_BUTTON_PRESSED if button.is_pressed else (COLOR_BUTTON_1 if button.link_id == 1 else COLOR_BUTTON_2)

        # Kapıları güncelle
        for door in self.doors:
            linked_btn = next((b for b in self.buttons if b.link_id == door.link_id), None)
            if linked_btn and linked_btn.is_pressed:
                door.is_open = True
                door.color = COLOR_DOOR_OPEN
            else:
                door.is_open = False
                door.color = COLOR_DOOR_1 if door.link_id == 1 else COLOR_DOOR_2

    def _check_game_status(self):
        if self.exit_point and self.player.rect.colliderect(self.exit_point.rect):
            self.state = "WON"
        
        for ghost in self.ghosts:
            if self.player.rect.colliderect(ghost.rect):
                self.state = "GAME_OVER"

    def create_time_loop(self):
        new_ghost = Ghost(self.player.history, COLOR_GHOST)
        self.ghosts.append(new_ghost)
        self.reset_game_state()

    def get_render_data(self):
        return {
            "player": getattr(self, 'player', None),
            "ghosts": self.ghosts,
            "walls": self.walls,
            "buttons": self.buttons,
            "doors": self.doors,
            "exit": self.exit_point,
            "time_left": LOOP_DURATION - self.current_frame if hasattr(self, 'current_frame') else 0,
            "state": self.state,
            "level_index": self.current_level_index
        }