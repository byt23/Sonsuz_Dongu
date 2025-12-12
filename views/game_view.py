import pygame
import os
from utils.settings import *

class GameView:
    def __init__(self):
        pygame.init()
        
        # --- EKRAN AYARLARI ---
        # Hata almaman için self.width ve self.height'i burada tanımlıyoruz
        self.width = VIRTUAL_WIDTH
        self.height = VIRTUAL_HEIGHT
        
        # Proje yolu bulma
        current_script_path = os.path.abspath(__file__)
        views_folder = os.path.dirname(current_script_path)
        self.project_root = os.path.dirname(views_folder)
        
        # Ekran Bilgileri
        self.display_info = pygame.display.Info()
        self.desktop_w = self.display_info.current_w
        self.desktop_h = self.display_info.current_h
        
        # Pencere ve Tuval (Canvas)
        self.screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Time-Loop Co-op: Kronos Protocol")
        
        # Tüm çizimleri önce bu 'canvas'a yapıyoruz, sonra ekrana scale ediyoruz
        self.canvas = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        self.fullscreen = False
        
        # Yüklemeler
        self._load_fonts()
        self.assets = {}
        self._load_assets()
        
        # Arayüz Elemanları
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
            else: raise FileNotFoundError
        except:
            self.ui_font = pygame.font.SysFont("Arial", 36, bold=True)
            self.story_font = pygame.font.SysFont("Arial", 28, bold=True)
            self.big_font = pygame.font.SysFont("Arial", 80, bold=True)

    def _load_assets(self):
        img_dir = os.path.join(self.project_root, "assets", "images")
        files = {"wall":"wall.png", "floor":"floor.png", "player":"player.png", "exit":"exit.png", "button":"button.png", "clock_icon":"clock_icon.png", "level_icon":"level_icon.png"}
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

    def toggle_fullscreen_mode(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen: self.screen = pygame.display.set_mode((self.desktop_w, self.desktop_h), pygame.FULLSCREEN)
        else: self.screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)

    def render(self, data):
        state = data["state"]
        texts = data.get("texts", {})
        if not texts: texts = {"GAME_TITLE":"ERROR", "INTRO_TITLE":"BOOT...", "INTRO_TEXT":["Loading..."]}

        # Hangi ekranın çizileceği
        if state == "INTRO": self._draw_intro(texts)
        elif state == "MENU": self._draw_menu(texts)
        elif state == "LEVEL_SELECT": self._draw_level_select(data["unlocked_levels"], texts)
        elif state == "BRIEFING":
            self.canvas.fill((5, 5, 10))
            self._draw_briefing(data, texts)
        elif state == "PLAYING" or state == "WON" or state == "GAME_OVER": 
            self._draw_game(data, texts)
        elif state == "PAUSED":
            self._draw_game(data, texts)
            self._draw_pause_menu(texts)
        elif state == "GAME_FINISHED":
            self.canvas.fill((0, 0, 0))
            self._draw_centered_text(texts.get("SIMULATION_COMPLETE", "THE END"), (0, 255, 0), 0)
        
        # Canvas'ı ekrana ölçekle ve çiz
        self._draw_scaled_output()
        pygame.display.flip()

    def get_click_action(self, mouse_pos, state):
        # Mouse koordinatlarını ölçeklendirilmiş ekrana göre ayarla
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

    # --- ÇİZİM FONKSİYONLARI ---

    def _draw_intro(self, texts):
        """Giriş ekranını çizer (Düzeltilmiş)."""
        # Canvas kullanıyoruz ki pencere büyüyünce bozulmasın
        self.canvas.fill((0, 0, 0)) 
        
        title_text = texts.get("INTRO_TITLE", "KRONOS PROTOCOL") 
        msg_text = texts.get("PRESS_ENTER", "PRESS ENTER")
        
        # Başlık
        title_surf = self.big_font.render(title_text, True, (0, 255, 0))
        # self.width yerine VIRTUAL_WIDTH da kullanılabilir ama __init__'te tanımladık
        title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 3))
        self.canvas.blit(title_surf, title_rect)
        
        # Alt mesaj
        msg_surf = self.ui_font.render(msg_text, True, (255, 255, 255))
        msg_rect = msg_surf.get_rect(center=(self.width // 2, self.height // 2))
        self.canvas.blit(msg_surf, msg_rect)

    def _draw_menu(self, texts):
        self.canvas.fill(COLOR_BG)
        self._draw_centered_text(texts.get("GAME_TITLE", "GAME"), (0, 255, 255), -150)
        self._draw_centered_text(texts.get("GAME_SUBTITLE", ""), (100, 100, 100), -80)
        
        btn_width = 500
        btn_x_offset = btn_width // 2
        
        btn_start = pygame.Rect(VIRTUAL_WIDTH//2 - btn_x_offset, 350, btn_width, 60)
        btn_levels = pygame.Rect(VIRTUAL_WIDTH//2 - btn_x_offset, 430, btn_width, 60)
        btn_lang = pygame.Rect(VIRTUAL_WIDTH//2 - btn_x_offset, 510, btn_width, 60)
        btn_quit = pygame.Rect(VIRTUAL_WIDTH//2 - btn_x_offset, 590, btn_width, 60)
        
        self._draw_button(btn_start, texts.get("START_GAME", "Start"), (0, 200, 0))
        self._draw_button(btn_levels, texts.get("LEVELS", "Levels"), (200, 200, 0))
        self._draw_button(btn_lang, texts.get("LANGUAGE", "Lang"), (50, 150, 200))
        self._draw_button(btn_quit, texts.get("QUIT", "Quit"), (200, 50, 50))
        
        self.menu_buttons = {"START_GAME": btn_start, "OPEN_LEVELS": btn_levels, "CHANGE_LANGUAGE": btn_lang, "QUIT_GAME": btn_quit}

    def _draw_level_select(self, unlocked, texts):
        self.canvas.fill(COLOR_BG)
        self._draw_centered_text(texts.get("SELECT_LEVEL", "Select Level"), (255, 255, 255), -250)
        
        btn_back = pygame.Rect(50, 50, 200, 50)
        self._draw_button(btn_back, texts.get("BACK", "Back"), (100, 100, 100))
        self.level_buttons = {"BACK_TO_MENU": btn_back}
        
        start_x = 240; start_y = 200; padding = 20; size = 80
        for i in range(1, 16):
            row = (i-1) // 5; col = (i-1) % 5
            rect = pygame.Rect(start_x + col*(size+padding), start_y + row*(size+padding), size, size)
            
            is_locked = i > unlocked
            col = (50, 50, 50) if is_locked else (0, 255, 255)
            
            pygame.draw.rect(self.canvas, col, rect, border_radius=10)
            pygame.draw.rect(self.canvas, (255,255,255), rect, 3, border_radius=10)
            
            lbl = self.ui_font.render(str(i), True, (100,100,100) if is_locked else (0,0,0))
            self.canvas.blit(lbl, lbl.get_rect(center=rect.center))
            
            if not is_locked: self.level_buttons[f"LEVEL_{i}"] = rect

    def _draw_pause_menu(self, texts):
        s = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        self.canvas.blit(s, (0,0))
        
        self._draw_centered_text(texts.get("PAUSED", "Paused"), (255, 255, 255), -150)
        
        btn_width = 500
        btn_x_offset = btn_width // 2
        btn_resume = pygame.Rect(VIRTUAL_WIDTH//2 - btn_x_offset, 300, btn_width, 60)
        btn_levels = pygame.Rect(VIRTUAL_WIDTH//2 - btn_x_offset, 380, btn_width, 60)
        btn_menu = pygame.Rect(VIRTUAL_WIDTH//2 - btn_x_offset, 460, btn_width, 60)
        
        self._draw_button(btn_resume, texts.get("RESUME", "Resume"), (0, 200, 0))
        self._draw_button(btn_levels, texts.get("LEVEL_SELECT", "Levels"), (200, 200, 0))
        self._draw_button(btn_menu, texts.get("MAIN_MENU", "Menu"), (200, 50, 50))
        
        self.pause_buttons = {"RESUME_GAME": btn_resume, "PAUSE_TO_LEVELS": btn_levels, "PAUSE_TO_MENU": btn_menu}

    def _draw_game(self, data, texts):
        # Zemin
        if self.assets.get("floor"):
             for row in range(VIRTUAL_HEIGHT // TILE_SIZE + 1):
                for col in range(VIRTUAL_WIDTH // TILE_SIZE + 1):
                    self.canvas.blit(self.assets["floor"], (col * TILE_SIZE, row * TILE_SIZE))
        else: self.canvas.fill(COLOR_BG)
        
        # Bağlantı Çizgileri
        for button in data["buttons"]:
            linked = next((d for d in data["doors"] if d.link_id == button.link_id), None)
            if linked:
                col = button.color
                pygame.draw.line(self.canvas, col, button.rect.center, linked.rect.center, 6 if button.is_pressed else 2)
                pygame.draw.circle(self.canvas, col, button.rect.center, 6)
                pygame.draw.circle(self.canvas, col, linked.rect.center, 6)

        # Duvarlar
        for wall in data["walls"]: 
            if self.assets.get("wall"): self.canvas.blit(self.assets["wall"], wall.rect)
            else: pygame.draw.rect(self.canvas, wall.color, wall.rect)
        
        # Çıkış
        if data["exit"]:
            if self.assets.get("exit"): self.canvas.blit(self.assets["exit"], self.assets["exit"].get_rect(center=data["exit"].rect.center))
            else: pygame.draw.rect(self.canvas, data["exit"].color, data["exit"].rect)
            
        # Kutular
        for box in data.get("boxes", []):
            if self.assets.get("wall"): # Kutu texture yoksa duvar gibi ama renkli çiz
                pygame.draw.rect(self.canvas, (139, 69, 19), box.rect)
                pygame.draw.rect(self.canvas, (205, 133, 63), box.rect, 4)
                pygame.draw.line(self.canvas, (100, 50, 0), box.rect.topleft, box.rect.bottomright, 3)
            else: pygame.draw.rect(self.canvas, box.color, box.rect)

        # Lazerler
        for laser in data.get("lasers", []):
            if laser.active:
                pygame.draw.rect(self.canvas, (255, 0, 0), laser.rect)
                c = laser.rect.copy()
                if laser.axis == 'V': c.inflate_ip(-6, 0)
                else: c.inflate_ip(0, -6)
                pygame.draw.rect(self.canvas, (255, 200, 200), c)
            else: pygame.draw.rect(self.canvas, (50, 50, 50), laser.rect, 1)

        # Butonlar
        for btn in data["buttons"]:
            if self.assets.get("button"):
                img = self.assets["button"].copy()
                img.fill(btn.color, special_flags=pygame.BLEND_MULT)
                self.canvas.blit(img, img.get_rect(center=btn.rect.center))
            else: pygame.draw.rect(self.canvas, btn.color, btn.rect)
            
        # Kapılar
        for door in data["doors"]:
            # Basit renk eşleşmesi (Yedek)
            col = (200, 200, 200)
            if door.link_id == 1: col = COLOR_DOOR_1
            elif door.link_id == 2: col = COLOR_DOOR_2
            elif door.link_id == 3: col = COLOR_DOOR_3
            elif door.link_id == 4: col = COLOR_DOOR_4
            elif door.link_id == 5: col = COLOR_DOOR_5
            
            if door.is_open:
                pygame.draw.rect(self.canvas, col, door.rect, 6)
            else:
                pygame.draw.rect(self.canvas, col, door.rect)
                pygame.draw.line(self.canvas, (0,0,0), door.rect.topleft, door.rect.bottomright, 3)

        # Hayaletler
        for ghost in data["ghosts"]:
            if self.assets.get("player"):
                img = self.assets["player"].copy()
                img.set_alpha(100)
                img.fill((200, 200, 200), special_flags=pygame.BLEND_MULT)
                self.canvas.blit(img, img.get_rect(center=ghost.rect.center))
            else:
                 s = pygame.Surface((ghost.rect.width, ghost.rect.height), pygame.SRCALPHA)
                 s.set_alpha(120); s.fill(ghost.color); self.canvas.blit(s, ghost.rect)

        # Oyuncu
        if data["player"]:
            if self.assets.get("player"): self.canvas.blit(self.assets["player"], self.assets["player"].get_rect(center=data["player"].rect.center))
            else: pygame.draw.rect(self.canvas, data["player"].color, data["player"].rect)
            
        # Işıklandırma ve UI
        self._apply_lighting(data)
        
        # UI Metinleri
        time_text = self.ui_font.render(f"{texts.get('TIME', 'Time')}: {data['time_left']}", True, (255,255,255))
        self.canvas.blit(time_text, (70 if self.assets.get("clock_icon") else 20, 25))
        if self.assets.get("clock_icon"): self.canvas.blit(self.assets["clock_icon"], (20, 20))
        
        lvl_text = self.ui_font.render(f"{texts.get('LEVEL', 'Level')}: {data['level_index']}", True, (255, 255, 0))
        lx = VIRTUAL_WIDTH - lvl_text.get_width() - 30
        if self.assets.get("level_icon"): 
            self.canvas.blit(self.assets["level_icon"], (VIRTUAL_WIDTH - 60, 20))
            lx -= 50
        self.canvas.blit(lvl_text, (lx, 25))
        
        fs_text = self.story_font.render(texts.get("FULLSCREEN_TIP", "F: Fullscreen"), True, (100, 100, 100))
        self.canvas.blit(fs_text, (20, VIRTUAL_HEIGHT - 40))

        if data["state"] == "WON":
             self._draw_centered_text(texts.get("LEVEL_COMPLETE", "Done!"), (100, 255, 100), -40)
             self._draw_centered_text(texts.get("PRESS_SPACE", "Space"), (255, 255, 255), 40)
        elif data["state"] == "GAME_OVER":
             self._draw_centered_text(texts.get("PARADOX", "Fail!"), (255, 50, 50), -40)
             self._draw_centered_text(texts.get("PRESS_R", "R"), (255, 255, 255), 40)

    # --- YARDIMCI METODLAR ---

    def _apply_lighting(self, data):
        self.darkness.fill((0, 0, 0, 255))
        if data["player"]: pygame.draw.circle(self.darkness, (0,0,0,0), data["player"].rect.center, 150)
        for g in data["ghosts"]: pygame.draw.circle(self.darkness, (0,0,0,0), g.rect.center, 80)
        self.canvas.blit(self.darkness, (0,0))

    def _draw_briefing(self, data, texts):
        key = f"S{data['level_index']}"
        lines = texts.get(key, ["Ready?", "Press SPACE."])
        start_y = (VIRTUAL_HEIGHT - len(lines)*40) / 2
        for i, line in enumerate(lines):
            t = self.story_font.render(line, True, (180, 200, 255))
            self.canvas.blit(t, t.get_rect(center=(VIRTUAL_WIDTH/2, start_y + i*40)))

    def _draw_button(self, rect, text, color):
        pygame.draw.rect(self.canvas, color, rect, border_radius=5)
        pygame.draw.rect(self.canvas, (255, 255, 255), rect, 2, border_radius=5)
        lbl = self.ui_font.render(text, True, (255, 255, 255))
        self.canvas.blit(lbl, lbl.get_rect(center=rect.center))

    def _draw_centered_text(self, text, color, y_offset):
        t = self.big_font.render(text, True, color)
        self.canvas.blit(t, t.get_rect(center=(VIRTUAL_WIDTH/2, VIRTUAL_HEIGHT/2 + y_offset)))
    
    def _draw_scaled_output(self):
        # Canvas'ı ekrana sığacak şekilde büyüt/küçült
        ts = pygame.display.get_surface()
        sw, sh = ts.get_size()
        scale = min(sw/VIRTUAL_WIDTH, sh/VIRTUAL_HEIGHT)
        nw, nh = int(VIRTUAL_WIDTH*scale), int(VIRTUAL_HEIGHT*scale)
        
        try: sc = pygame.transform.smoothscale(self.canvas, (nw, nh))
        except: sc = pygame.transform.scale(self.canvas, (nw, nh))
        
        ts.fill((0,0,0))
        ts.blit(sc, ((sw-nw)//2, (sh-nh)//2))