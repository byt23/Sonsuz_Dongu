import pygame
import os
from models.entity import Player, Ghost, Wall, Button, Door, Exit, Box, Laser
from utils.settings import *
from utils.save_manager import SaveManager
from utils.localization import TEXTS 

class GameViewModel:
    def __init__(self, model=None):
        self.state = "INTRO"
        
        self.ghosts = []; self.walls = []; self.buttons = []
        self.doors = []; self.boxes = []; self.lasers = []
        self.exit_point = None
        
        self.player = Player(100, 100, COLOR_PLAYER)
        self.start_pos = (100, 100)
        
        self.current_level_index = 1
        self.current_level_max_time = DEFAULT_DURATION
        self.current_frame = 0 
        self.is_loop_ended = False
        self.sound_queue = []
        
        self.languages = ["TR", "EN", "DE", "FR", "ES"]
        self.lang_index = 0
        self.texts = TEXTS["TR"]
        
        self.save_data = SaveManager.load_data()
        self.unlocked_levels = self.save_data.get("unlocked_levels", 1)

    def cycle_language(self):
        self.lang_index = (self.lang_index + 1) % len(self.languages)
        lang_code = self.languages[self.lang_index]
        self.texts = TEXTS[lang_code]

    def process_click(self, action):
        if not action: return
        
        if self.state == "INTRO": self.state = "MENU"
        elif action == "START_GAME":
            self.current_level_index = self.unlocked_levels
            if self.current_level_index > 15: self.current_level_index = 1
            self.start_level_sequence()
        elif action == "OPEN_LEVELS": self.state = "LEVEL_SELECT"
        elif action == "QUIT_GAME": return "QUIT"
        elif action == "CHANGE_LANGUAGE": self.cycle_language()
        elif action == "RESUME_GAME": self.state = "PLAYING"
        elif action == "PAUSE_TO_LEVELS": self.state = "LEVEL_SELECT"
        elif action == "PAUSE_TO_MENU": self.state = "MENU"
        elif action == "BACK_TO_MENU": self.state = "MENU"
        elif action.startswith("LEVEL_"):
            try:
                lvl = int(action.split("_")[1])
                if lvl <= self.unlocked_levels:
                    self.current_level_index = lvl
                    self.start_level_sequence()
            except: pass

    # --- HAREKET MANTIĞI (DÜZELTİLDİ: Kaygan Hareket) ---
    def handle_input(self, dx, dy):
        if self.state != "PLAYING" or self.is_loop_ended: return
        if dx == 0 and dy == 0: return

        speed = 6 # Hızı biraz artırdım, daha akıcı olsun diye
        
        # 1. Önce X Ekseninde Hareket Dene
        if dx != 0:
            next_rect_x = self.player.rect.copy()
            next_rect_x.x += dx * speed
            
            # Kutu İtme (X Ekseni)
            can_move_x = True
            for box in self.boxes:
                if next_rect_x.colliderect(box.rect):
                    box_next = box.rect.copy()
                    box_next.x += dx * speed
                    if self._check_collision(box_next, is_box=True):
                        box.rect = box_next
                        self.sound_queue.append("push")
                    else:
                        can_move_x = False
            
            if can_move_x and self._check_collision(next_rect_x):
                self.player.rect = next_rect_x

        # 2. Sonra Y Ekseninde Hareket Dene
        if dy != 0:
            next_rect_y = self.player.rect.copy()
            next_rect_y.y += dy * speed
            
            # Kutu İtme (Y Ekseni)
            can_move_y = True
            for box in self.boxes:
                if next_rect_y.colliderect(box.rect):
                    box_next = box.rect.copy()
                    box_next.y += dy * speed
                    if self._check_collision(box_next, is_box=True):
                        box.rect = box_next
                        if "push" not in self.sound_queue: # Ses tekrarını önle
                            self.sound_queue.append("push")
                    else:
                        can_move_y = False
            
            if can_move_y and self._check_collision(next_rect_y):
                self.player.rect = next_rect_y

    def _check_collision(self, rect, is_box=False):
        if rect.left < 0 or rect.right > VIRTUAL_WIDTH or rect.top < 0 or rect.bottom > VIRTUAL_HEIGHT: return False
        for wall in self.walls:
            if rect.colliderect(wall.rect): return False
        for door in self.doors:
            if not door.is_open and rect.colliderect(door.rect): return False
        if is_box:
            for other in self.boxes:
                if rect.colliderect(other.rect) and rect != other.rect: return False
        return True

    def update(self):
        if self.state != "PLAYING": return
        if self.current_frame >= self.current_level_max_time:
            self.create_time_loop()
            return
        
        self.player.record_position()
        for ghost in self.ghosts: ghost.update_position_from_history(self.current_frame)
        self._update_mechanics()
        self._check_game_status()
        self.current_frame += 1

    def _update_mechanics(self):
        cycle = 180
        laser_active = (self.current_frame % cycle) < (cycle // 2)
        for laser in self.lasers: laser.active = laser_active

        for button in self.buttons:
            collides = self.player.rect.colliderect(button.rect)
            for g in self.ghosts:
                if g.rect.colliderect(button.rect): collides = True
            for b in self.boxes:
                if b.rect.colliderect(button.rect): collides = True
            
            if collides and not button.was_occupied:
                button.is_pressed = not button.is_pressed
                self.sound_queue.append("click")
            button.was_occupied = collides
            button.color = COLOR_BUTTON_PRESSED if button.is_pressed else (200,200,200)

        for door in self.doors:
            btn = next((b for b in self.buttons if b.link_id == door.link_id), None)
            if btn and btn.is_pressed: door.is_open = True
            else: door.is_open = False

    def _check_game_status(self):
        if self.exit_point and self.player.rect.colliderect(self.exit_point.rect):
            self.state = "WON"
            self.sound_queue.append("win")
            return
        for ghost in self.ghosts:
            if self.player.rect.colliderect(ghost.rect):
                self.state = "GAME_OVER"
                self.sound_queue.append("glitch")
                return
        for laser in self.lasers:
            if laser.active and self.player.rect.colliderect(laser.rect):
                self.state = "GAME_OVER"
                self.sound_queue.append("glitch")
                return

    def create_time_loop(self):
        self.ghosts.append(Ghost(self.player.history, COLOR_GHOST))
        self.reset_game_state()

    def start_level_sequence(self):
        key = f"S{self.current_level_index}"
        if key in self.texts: self.state = "BRIEFING"
        else: self.start_level_gameplay()

    def start_level_gameplay(self):
        self.state = "PLAYING"
        self._init_level(self.current_level_index)
        self.reset_game_state()
        self.ghosts = []

    def reset_game_state(self):
        temp_ghosts = self.ghosts[:]
        self._init_level(self.current_level_index)
        self.ghosts = temp_ghosts
        self.player = Player(self.start_pos[0], self.start_pos[1], COLOR_PLAYER)
        self.current_frame = 0

    def _init_level(self, lvl):
        self.walls, self.boxes, self.buttons, self.doors, self.lasers = [], [], [], [], []
        self.current_level_max_time = LEVEL_DURATIONS.get(lvl, DEFAULT_DURATION)
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_path, "levels", f"level{lvl}.txt")
            with open(file_path, "r") as f:
                lines = f.readlines()
                for r, line in enumerate(lines):
                    for c, char in enumerate(line):
                        x, y = c * TILE_SIZE, r * TILE_SIZE
                        if char == 'W': self.walls.append(Wall(x, y, COLOR_WALL))
                        elif char == 'P': self.start_pos = (x, y)
                        elif char == 'E': self.exit_point = Exit(x, y, COLOR_EXIT)
                        elif char == 'B': self.boxes.append(Box(x, y, COLOR_BOX))
                        elif char == 'L': self.lasers.append(Laser(x, y, COLOR_LASER, 'V'))
                        elif char == 'H': self.lasers.append(Laser(x, y, COLOR_LASER, 'H'))
                        elif char in ['1','2','3','4','5']: 
                            self.buttons.append(Button(x, y, (255,255,255), int(char)))
                        elif char in ['a','b','c','d','e']: 
                            mapping = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5}
                            self.doors.append(Door(x, y, (255,255,255), mapping[char]))
        except: self.state = "MENU"

    def skip_intro(self): self.state = "MENU"
    def toggle_pause(self): self.state = "PAUSED" if self.state == "PLAYING" else "PLAYING"
    def full_restart(self): self.start_level_sequence()
    def next_level(self): 
        SaveManager.save_progress(self.current_level_index)
        self.save_data = SaveManager.load_data()
        self.unlocked_levels = self.save_data.get("unlocked_levels", 1)
        self.current_level_index += 1
        self.start_level_sequence()

    def get_render_data(self):
        data = {
            "state": self.state,
            "texts": self.texts,
            "current_frame": self.current_frame,
            "max_time": self.current_level_max_time,
            "level_index": self.current_level_index,
            "unlocked_levels": self.unlocked_levels,
            "time_left": (self.current_level_max_time - self.current_frame) // 60 
        }
        if self.state in ["PLAYING", "PAUSED", "GAME_OVER", "WON"]:
            data.update({
                "player": self.player, "walls": self.walls, "ghosts": self.ghosts,
                "boxes": self.boxes, "buttons": self.buttons, "doors": self.doors,
                "lasers": self.lasers, "exit": self.exit_point 
            })
        return data