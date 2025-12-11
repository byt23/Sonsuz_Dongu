import pygame
import os
from models.entity import Entity, Player, Ghost, Wall, Button, Door, Exit
from utils.settings import *
from utils.save_manager import SaveManager

class GameViewModel:
    def __init__(self):
        self.ghosts = [] 
        self.walls = []
        self.buttons = []
        self.doors = []
        self.exit_point = None
        self.start_pos = (100, 100)
        self.current_level_index = 1
        self.current_level_max_time = DEFAULT_DURATION
        self.state = "MENU" 
        self.save_data = SaveManager.load_data()
        self.unlocked_levels = self.save_data.get("unlocked_levels", 1)

    def process_click(self, action):
        if action == "START_GAME":
            self.current_level_index = self.unlocked_levels
            if self.current_level_index > 7: self.current_level_index = 1
            self.start_level_sequence()
        elif action == "OPEN_LEVELS":
            self.state = "LEVEL_SELECT"
        elif action == "QUIT_GAME":
            return "QUIT"
        elif action == "BACK_TO_MENU":
            self.state = "MENU"
        elif action == "RESUME_GAME":
            self.state = "PLAYING"
        elif action == "PAUSE_TO_LEVELS":
            self.state = "LEVEL_SELECT"
        elif action == "PAUSE_TO_MENU":
            self.state = "MENU" # ANA MENÜYE DÖN
        elif action.startswith("LEVEL_"):
            lvl = int(action.split("_")[1])
            if lvl <= self.unlocked_levels:
                self.current_level_index = lvl
                self.start_level_sequence()

    def toggle_pause(self):
        if self.state == "PLAYING": self.state = "PAUSED"
        elif self.state == "PAUSED": self.state = "PLAYING"

    def start_level_sequence(self):
        if self.current_level_index in STORY_TEXTS: self.state = "BRIEFING"
        else: self.start_level_gameplay()

    def start_level_gameplay(self):
        self.state = "PLAYING"
        self._init_level(self.current_level_index)
        self.reset_game_state()

    def next_level(self):
        SaveManager.save_progress(self.current_level_index)
        self.unlocked_levels = SaveManager.load_data()["unlocked_levels"]
        self.current_level_index += 1
        if self.current_level_index in STORY_TEXTS and self.current_level_index <= 7: self.state = "BRIEFING" 
        elif self.current_level_index > 7: self.state = "GAME_FINISHED" 
        else: self.start_level_gameplay()

    def _init_level(self, level_num):
        self.current_level_max_time = LEVEL_DURATIONS.get(level_num, DEFAULT_DURATION)
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
                    elif char == '1': self.buttons.append(Button(x, y, COLOR_BUTTON_1, 1))
                    elif char == 'a': self.doors.append(Door(x, y, COLOR_DOOR_1, 1))
                    elif char == '2': self.buttons.append(Button(x, y, COLOR_BUTTON_2, 2))
                    elif char == 'b': self.doors.append(Door(x, y, COLOR_DOOR_2, 2))
                    elif char == '3': self.buttons.append(Button(x, y, COLOR_BUTTON_3, 3))
                    elif char == 'c': self.doors.append(Door(x, y, COLOR_DOOR_3, 3))
        except FileNotFoundError:
            self.state = "MENU"

    def reset_game_state(self):
        start_x, start_y = self.start_pos
        self.player = Player(start_x, start_y, COLOR_PLAYER)
        self.current_frame = 0
        self.is_loop_ended = False

    def full_restart(self):
        self.ghosts = [] 
        self.state = "PLAYING"
        for btn in self.buttons: 
            btn.is_pressed = False
            btn.was_occupied = False 
        for door in self.doors: door.is_open = False
        self.reset_game_state()

    def handle_input(self, dx, dy):
        if self.state != "PLAYING": return
        if self.is_loop_ended: return
        next_rect = self.player.rect.copy()
        next_rect.x += dx * 5
        next_rect.y += dy * 5
        if self._can_move_to(next_rect): self.player.rect = next_rect

    def _can_move_to(self, rect):
        if rect.left < 0 or rect.right > VIRTUAL_WIDTH or rect.top < 0 or rect.bottom > VIRTUAL_HEIGHT: return False
        for wall in self.walls:
            if rect.colliderect(wall.rect): return False
        for door in self.doors:
            if not door.is_open and rect.colliderect(door.rect): return False
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
        for button in self.buttons:
            occupied = self.player.rect.colliderect(button.rect) or any(g.rect.colliderect(button.rect) for g in self.ghosts)
            if occupied and not button.was_occupied: button.is_pressed = not button.is_pressed
            button.was_occupied = occupied
            if button.is_pressed: button.color = COLOR_BUTTON_PRESSED
            else:
                if button.link_id == 1: button.color = COLOR_BUTTON_1
                elif button.link_id == 2: button.color = COLOR_BUTTON_2
                elif button.link_id == 3: button.color = COLOR_BUTTON_3
        for door in self.doors:
            btn = next((b for b in self.buttons if b.link_id == door.link_id), None)
            if btn and btn.is_pressed: door.is_open = True
            else: door.is_open = False
            if door.link_id == 1: door.color = COLOR_DOOR_1
            elif door.link_id == 2: door.color = COLOR_DOOR_2
            elif door.link_id == 3: door.color = COLOR_DOOR_3

    def _check_game_status(self):
        if self.exit_point and self.player.rect.colliderect(self.exit_point.rect): self.state = "WON"
        for ghost in self.ghosts:
            if self.player.rect.colliderect(ghost.rect): self.state = "GAME_OVER"

    def create_time_loop(self):
        self.ghosts.append(Ghost(self.player.history, COLOR_GHOST))
        self.reset_game_state()

    def get_render_data(self):
        return {
            "player": getattr(self, 'player', None),
            "ghosts": self.ghosts,
            "walls": self.walls,
            "buttons": self.buttons,
            "doors": self.doors,
            "exit": self.exit_point,
            "time_left": self.current_level_max_time - self.current_frame if hasattr(self, 'current_frame') else 0,
            "state": self.state,
            "level_index": self.current_level_index,
            "unlocked_levels": self.unlocked_levels
        }