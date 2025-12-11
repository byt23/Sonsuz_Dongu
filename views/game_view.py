import pygame
import os
from utils.settings import *

class GameView:
    def __init__(self):
        pygame.init()
        # DOSYA YOLLARI (Absolute Path)
        current_script_path = os.path.abspath(__file__)
        views_folder = os.path.dirname(current_script_path)
        self.project_root = os.path.dirname(views_folder)
        
        self.display_info = pygame.display.Info()
        self.desktop_w = self.display_info.current_w
        self.desktop_h = self.display_info.current_h
        
        # Başlangıç: Pencere Modu
        self.screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Time-Loop Co-op: Kronos Protocol")
        
        self.canvas = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        self.fullscreen = False
        
        self._load_fonts()
        self.assets = {}
        self._load_assets()
        self.darkness = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        
        self.menu_buttons = {} 
        self.level_buttons = {}
        self.pause_buttons = {}

    def _load_fonts(self):
        font_path = os.path.join(self.project_root, "assets", "font.ttf")
        try:
            if os.path.exists(font_path):
                self.ui_font = pygame.font.Font(font_path, 36) 
                self.story_font = pygame.font.Font(font_path, 28)
                self.big_font = pygame.font.Font(font_path, 80)
            else:
                raise FileNotFoundError
        except:
            self.ui_font = pygame.font.SysFont("Arial", 36, bold=True)
            self.story_font = pygame.font.SysFont("Arial", 28, bold=True)
            self.big_font = pygame.font.SysFont("Arial", 80, bold=True)

    def _load_assets(self):
        img_dir = os.path.join(self.project_root, "assets", "images")
        files = {
            "wall": "wall.png", "floor": "floor.png", "player": "player.png",
            "exit": "exit.png", "button": "button.png", "clock_icon": "clock_icon.png", "level_icon": "level_icon.png"
        }
        for key, filename in files.items():
            path = os.path.join(img_dir, filename)
            try:
                img = pygame.image.load(path).convert_alpha()
                if key == "player": img = pygame.transform.scale(img, (int(TILE_SIZE * 0.6), int(TILE_SIZE * 0.6)))
                elif key in ["clock_icon", "level_icon"]: img = pygame.transform.scale(img, (40, 40))
                elif key in ["button", "exit"]: img = pygame.transform.scale(img, (int(TILE_SIZE * 0.7), int(TILE_SIZE * 0.7)))
                else: img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                self.assets[key] = img
            except: self.assets[key] = None

    # --- TAM EKRAN DÜZELTMESİ ---
    def toggle_fullscreen_mode(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            # NOFRAME yerine FULLSCREEN kullanıyoruz (Daha kararlı)
            self.screen = pygame.display.set_mode((self.desktop_w, self.desktop_h), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)

    def render(self, data):
        state = data["state"]
        
        if state == "MENU": self._draw_menu()
        elif state == "LEVEL_SELECT": self._draw_level_select(data["unlocked_levels"])
        elif state == "BRIEFING":
            self.canvas.fill((5, 5, 10))
            self._draw_briefing(data)
        elif state == "PLAYING" or state == "WON" or state == "GAME_OVER": self._draw_game(data)
        elif state == "PAUSED":
            self._draw_game(data)
            self._draw_pause_menu()
        elif state == "GAME_FINISHED":
            self.canvas.fill((0, 0, 0))
            self._draw_centered_text("SIMULATION COMPLETE", (0, 255, 0), 0)

        self._draw_scaled_output()
        pygame.display.flip()

    def get_click_action(self, mouse_pos, state):
        screen_w, screen_h = self.screen.get_size()
        scale = min(screen_w / VIRTUAL_WIDTH, screen_h / VIRTUAL_HEIGHT)
        new_w, new_h = int(VIRTUAL_WIDTH * scale), int(VIRTUAL_HEIGHT * scale)
        start_x, start_y = (screen_w - new_w) // 2, (screen_h - new_h) // 2
        
        virtual_x = (mouse_pos[0] - start_x) / scale
        virtual_y = (mouse_pos[1] - start_y) / scale
        
        if state == "MENU":
            for name, rect in self.menu_buttons.items():
                if rect.collidepoint(virtual_x, virtual_y): return name
        elif state == "LEVEL_SELECT":
            for name, rect in self.level_buttons.items():
                if rect.collidepoint(virtual_x, virtual_y): return name
        elif state == "PAUSED":
            for name, rect in self.pause_buttons.items():
                if rect.collidepoint(virtual_x, virtual_y): return name
        return None

    def _draw_pause_menu(self):
        s = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        self.canvas.blit(s, (0,0))
        self._draw_centered_text("PAUSED", (255, 255, 255), -150)
        
        btn_width = 400
        btn_x_offset = btn_width // 2
        btn_resume = pygame.Rect(VIRTUAL_WIDTH//2 - btn_x_offset, 300, btn_width, 60)
        btn_levels = pygame.Rect(VIRTUAL_WIDTH//2 - btn_x_offset, 380, btn_width, 60)
        btn_menu = pygame.Rect(VIRTUAL_WIDTH//2 - btn_x_offset, 460, btn_width, 60)
        
        self._draw_button(btn_resume, "RESUME", (0, 200, 0))
        self._draw_button(btn_levels, "LEVEL SELECT", (200, 200, 0))
        self._draw_button(btn_menu, "MAIN MENU", (200, 50, 50))
        
        self.pause_buttons = {"RESUME_GAME": btn_resume, "PAUSE_TO_LEVELS": btn_levels, "PAUSE_TO_MENU": btn_menu}

    def _draw_menu(self):
        self.canvas.fill(COLOR_BG)
        self._draw_centered_text("KRONOS PROTOCOL", (0, 255, 255), -150)
        self._draw_centered_text("Time-Loop Initiative", (100, 100, 100), -80)
        
        btn_width = 400
        btn_x_offset = btn_width // 2
        btn_start = pygame.Rect(VIRTUAL_WIDTH//2 - btn_x_offset, 350, btn_width, 60)
        btn_levels = pygame.Rect(VIRTUAL_WIDTH//2 - btn_x_offset, 430, btn_width, 60)
        btn_quit = pygame.Rect(VIRTUAL_WIDTH//2 - btn_x_offset, 510, btn_width, 60)
        
        self._draw_button(btn_start, "START GAME", (0, 200, 0))
        self._draw_button(btn_levels, "LEVELS", (200, 200, 0))
        self._draw_button(btn_quit, "QUIT", (200, 50, 50))
        self.menu_buttons = {"START_GAME": btn_start, "OPEN_LEVELS": btn_levels, "QUIT_GAME": btn_quit}

    def _draw_level_select(self, unlocked):
        self.canvas.fill(COLOR_BG)
        self._draw_centered_text("SELECT LEVEL", (255, 255, 255), -250)
        
        btn_back = pygame.Rect(50, 50, 200, 50)
        self._draw_button(btn_back, "< BACK", (100, 100, 100))
        self.level_buttons = {"BACK_TO_MENU": btn_back}
        
        start_x, start_y = 300, 200
        padding, size = 20, 100
        for i in range(1, 8):
            row, col = (i-1) // 4, (i-1) % 4
            rect = pygame.Rect(start_x + col*(size+padding), start_y + row*(size+padding), size, size)
            is_locked = i > unlocked
            color = (50, 50, 50) if is_locked else (0, 255, 255)
            pygame.draw.rect(self.canvas, color, rect, border_radius=10)
            pygame.draw.rect(self.canvas, (255,255,255), rect, 3, border_radius=10)
            lbl = self.ui_font.render(str(i), True, (100,100,100) if is_locked else (0,0,0))
            self.canvas.blit(lbl, lbl.get_rect(center=rect.center))
            if not is_locked: self.level_buttons[f"LEVEL_{i}"] = rect

    def _draw_button(self, rect, text, color):
        pygame.draw.rect(self.canvas, color, rect, border_radius=5)
        pygame.draw.rect(self.canvas, (255, 255, 255), rect, 2, border_radius=5)
        lbl = self.ui_font.render(text, True, (255, 255, 255))
        self.canvas.blit(lbl, lbl.get_rect(center=rect.center))

    def _draw_game(self, data):
        if self.assets.get("floor"):
             for row in range(VIRTUAL_HEIGHT // TILE_SIZE + 1):
                for col in range(VIRTUAL_WIDTH // TILE_SIZE + 1):
                    self.canvas.blit(self.assets["floor"], (col * TILE_SIZE, row * TILE_SIZE))
        else: self.canvas.fill(COLOR_BG)
        
        for button in data["buttons"]:
            linked = next((d for d in data["doors"] if d.link_id == button.link_id), None)
            if linked:
                col = button.color
                pygame.draw.line(self.canvas, col, button.rect.center, linked.rect.center, 6 if button.is_pressed else 2)
                pygame.draw.circle(self.canvas, col, button.rect.center, 6)
                pygame.draw.circle(self.canvas, col, linked.rect.center, 6)

        for wall in data["walls"]: 
            if self.assets.get("wall"): self.canvas.blit(self.assets["wall"], wall.rect)
            else: pygame.draw.rect(self.canvas, wall.color, wall.rect)
        
        if data["exit"]:
            if self.assets.get("exit"): self.canvas.blit(self.assets["exit"], self.assets["exit"].get_rect(center=data["exit"].rect.center))
            else: pygame.draw.rect(self.canvas, data["exit"].color, data["exit"].rect)
            
        for btn in data["buttons"]:
            if self.assets.get("button"):
                img = self.assets["button"].copy()
                img.fill(btn.color, special_flags=pygame.BLEND_MULT)
                self.canvas.blit(img, img.get_rect(center=btn.rect.center))
            else: pygame.draw.rect(self.canvas, btn.color, btn.rect)
            
        for door in data["doors"]:
            # --- RENK SEÇİMİ ---
            if door.link_id == 1: col = COLOR_DOOR_1
            elif door.link_id == 2: col = COLOR_DOOR_2
            elif door.link_id == 3: col = COLOR_DOOR_3
            elif door.link_id == 4: col = COLOR_DOOR_4
            elif door.link_id == 5: col = COLOR_DOOR_5
            else: col = (200, 200, 200)

            if door.is_open:
                pygame.draw.rect(self.canvas, col, door.rect, 6)
                for c in [door.rect.topleft, door.rect.topright, door.rect.bottomleft, door.rect.bottomright]: pygame.draw.circle(self.canvas, col, c, 4)
            else:
                pygame.draw.rect(self.canvas, col, door.rect)
                pygame.draw.line(self.canvas, (0,0,0), door.rect.topleft, door.rect.bottomright, 3)

        for ghost in data["ghosts"]:
            if self.assets.get("player"):
                img = self.assets["player"].copy()
                img.set_alpha(100)
                img.fill((200, 200, 200), special_flags=pygame.BLEND_MULT)
                self.canvas.blit(img, img.get_rect(center=ghost.rect.center))
            else:
                 s = pygame.Surface((ghost.rect.width, ghost.rect.height), pygame.SRCALPHA)
                 s.set_alpha(120); s.fill(ghost.color); self.canvas.blit(s, ghost.rect)

        if data["player"]:
            if self.assets.get("player"): self.canvas.blit(self.assets["player"], self.assets["player"].get_rect(center=data["player"].rect.center))
            else: pygame.draw.rect(self.canvas, data["player"].color, data["player"].rect)
            
        self._apply_lighting(data)
        
        time_text = self.ui_font.render(f"{data['time_left']}", True, COLOR_TEXT)
        self.canvas.blit(time_text, (70 if self.assets.get("clock_icon") else 20, 25))
        if self.assets.get("clock_icon"): self.canvas.blit(self.assets["clock_icon"], (20, 20))
        
        lvl_text = self.ui_font.render(f"LEVEL: {data['level_index']}", True, (255, 255, 0))
        lx = VIRTUAL_WIDTH - lvl_text.get_width() - 30
        if self.assets.get("level_icon"): 
            self.canvas.blit(self.assets["level_icon"], (VIRTUAL_WIDTH - 60, 20))
            lx -= 50
        self.canvas.blit(lvl_text, (lx, 25))
        
        if data["state"] == "WON":
             self._draw_centered_text("LEVEL COMPLETE!", (100, 255, 100), -40)
             self._draw_centered_text("Press 'SPACE' to Continue", (255, 255, 255), 40)
        elif data["state"] == "GAME_OVER":
             self._draw_centered_text("PARADOX!", (255, 50, 50), -40)
             self._draw_centered_text("Press 'R' to Retry", (255, 255, 255), 40)

    def _apply_lighting(self, data):
        self.darkness.fill((0, 0, 0, 255))
        if data["player"]: pygame.draw.circle(self.darkness, (0,0,0,0), data["player"].rect.center, 150)
        for g in data["ghosts"]: pygame.draw.circle(self.darkness, (0,0,0,0), g.rect.center, 80)
        self.canvas.blit(self.darkness, (0,0))

    def _draw_briefing(self, data):
        lines = STORY_TEXTS.get(data["level_index"], ["Ready?", "Press SPACE."])
        start_y = (VIRTUAL_HEIGHT - len(lines)*40) / 2
        for i, line in enumerate(lines):
            t = self.story_font.render(line, True, (180, 200, 255))
            self.canvas.blit(t, t.get_rect(center=(VIRTUAL_WIDTH/2, start_y + i*40)))

    def _draw_centered_text(self, text, color, y_offset):
        t = self.big_font.render(text, True, color)
        self.canvas.blit(t, t.get_rect(center=(VIRTUAL_WIDTH/2, VIRTUAL_HEIGHT/2 + y_offset)))
    
    def _draw_scaled_output(self):
        ts = pygame.display.get_surface()
        sw, sh = ts.get_size()
        scale = min(sw/VIRTUAL_WIDTH, sh/VIRTUAL_HEIGHT)
        nw, nh = int(VIRTUAL_WIDTH*scale), int(VIRTUAL_HEIGHT*scale)
        try: sc = pygame.transform.smoothscale(self.canvas, (nw, nh))
        except: sc = pygame.transform.scale(self.canvas, (nw, nh))
        ts.fill((0,0,0)); ts.blit(sc, ((sw-nw)//2, (sh-nh)//2))