import pygame
import os
from utils.settings import *

class GameView:
    def __init__(self):
        pygame.init()
        
        # Ekran bilgileri
        self.display_info = pygame.display.Info()
        self.desktop_w = self.display_info.current_w
        self.desktop_h = self.display_info.current_h
        
        # 1. Başlangıç: Pencere Modu
        self.screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Time-Loop Co-op: Kronos Protocol") # Oyun Başlığı
        
        # 2. Sanal Tuval
        self.canvas = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        self.fullscreen = False
        
        # --- 3. FONT TANIMLAMASI ---
        # Kod 'assets/font.ttf' dosyasını arar. Bulamazsa Arial kullanır.
        # MUTLAK YOL (Absolute Path) kullanıyoruz
        current_script_path = os.path.abspath(__file__)
        views_folder = os.path.dirname(current_script_path)
        self.project_root = os.path.dirname(views_folder)
        font_path = os.path.join(self.project_root, "assets", "font.ttf")
        
        # Varsayılan Fontlar
        self.ui_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.story_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 60, bold=True)

        try:
            if os.path.exists(font_path):
                self.ui_font = pygame.font.Font(font_path, 40) 
                self.story_font = pygame.font.Font(font_path, 30)
                self.big_font = pygame.font.Font(font_path, 60)
            else:
                print("WARNING: font.ttf not found, using Arial.")
        except Exception as e:
            print(f"CRITICAL FONT ERROR: {e}")

        # 4. Görselleri Yükle
        self.assets = {}
        self._load_assets()
        
        # 5. Işıklandırma Katmanı
        self.darkness = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)

    def _load_assets(self):
        """Resimleri assets/images klasöründen yükler."""
        img_dir = os.path.join(self.project_root, "assets", "images")
        
        files = {
            "wall": "wall.png", 
            "floor": "floor.png",
            "player": "player.png",
            "exit": "exit.png",
            "button": "button.png",
            "clock_icon": "clock_icon.png",
            "level_icon": "level_icon.png"
        }
        
        print("--- LOADING ASSETS ---")
        for key, filename in files.items():
            path = os.path.join(img_dir, filename)
            try:
                img = pygame.image.load(path).convert_alpha()
                
                if key == "player":
                    char_size = int(TILE_SIZE * 0.6) 
                    img = pygame.transform.scale(img, (char_size, char_size))
                elif key in ["clock_icon", "level_icon"]:
                    img = pygame.transform.scale(img, (40, 40))
                elif key in ["button", "exit"]:
                    size = int(TILE_SIZE * 0.7)
                    img = pygame.transform.scale(img, (size, size))
                else:
                    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                
                self.assets[key] = img
                print(f"[OK] {filename}")
            except FileNotFoundError:
                if key not in ["clock_icon", "level_icon"]:
                    print(f"[ERROR] {filename} not found!")
                self.assets[key] = None

    def toggle_fullscreen_mode(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.desktop_w, self.desktop_h), pygame.NOFRAME)
        else:
            self.screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)

    def render(self, data):
        self._draw_on_canvas(data)
        self._draw_scaled_output()
        pygame.display.flip()

    def _draw_on_canvas(self, data):
        """Tüm çizimleri sanal tuvale yapar."""
        state = data["state"]
        
        if state == "BRIEFING":
            self.canvas.fill((5, 5, 10)); self._draw_briefing(data); return
        elif state == "GAME_FINISHED":
            self.canvas.fill((0, 0, 0)); 
            # İNGİLİZCE MESAJLAR
            self._draw_centered_text("DATA UPLOAD COMPLETE...", (0, 255, 0), -80); 
            self._draw_centered_text("SUBJECT 404: SUCCESSFUL.", (0, 255, 0), -30); 
            
            text = self.big_font.render("TO BE CONTINUED...", True, (255, 255, 255))
            text_rect = text.get_rect(center=(VIRTUAL_WIDTH/2, VIRTUAL_HEIGHT/2 + 60))
            self.canvas.blit(text, text_rect)
            return
        
        # --- OYUN ÇİZİMİ (AYNI KALIYOR) ---
        if self.assets.get("floor"):
            for row in range(VIRTUAL_HEIGHT // TILE_SIZE + 1):
                for col in range(VIRTUAL_WIDTH // TILE_SIZE + 1):
                    self.canvas.blit(self.assets["floor"], (col * TILE_SIZE, row * TILE_SIZE))
        else: self.canvas.fill(COLOR_BG)

        for button in data["buttons"]:
            linked_door = next((d for d in data["doors"] if d.link_id == button.link_id), None)
            if linked_door:
                wire_color = button.color
                start_pos = button.rect.center
                end_pos = linked_door.rect.center
                thickness = 6 if button.is_pressed else 2
                pygame.draw.line(self.canvas, wire_color, start_pos, end_pos, thickness)
                pygame.draw.circle(self.canvas, wire_color, start_pos, 6)
                pygame.draw.circle(self.canvas, wire_color, end_pos, 6)

        for wall in data["walls"]: 
            if self.assets.get("wall"): self.canvas.blit(self.assets["wall"], wall.rect)
            else: pygame.draw.rect(self.canvas, wall.color, wall.rect)

        if data["exit"]: 
            if self.assets.get("exit"):
                self.canvas.blit(self.assets["exit"], data["exit"].rect)
            else: pygame.draw.rect(self.canvas, data["exit"].color, data["exit"].rect)
        
        for button in data["buttons"]: 
            if self.assets.get("button"):
                btn_img = self.assets["button"].copy()
                btn_img.fill(button.color, special_flags=pygame.BLEND_MULT)
                self.canvas.blit(btn_img, button.rect)
            else: pygame.draw.rect(self.canvas, button.color, button.rect)

        for door in data["doors"]:
            if door.is_open: pygame.draw.rect(self.canvas, COLOR_DOOR_OPEN, door.rect, 4) 
            else: pygame.draw.rect(self.canvas, door.color, door.rect) 
        
        for ghost in data["ghosts"]:
            if self.assets.get("player"):
                ghost_img = self.assets["player"].copy()
                ghost_img.set_alpha(100) 
                ghost_img.fill((200, 200, 200), special_flags=pygame.BLEND_MULT)
                img_rect = ghost_img.get_rect(center=ghost.rect.center)
                self.canvas.blit(ghost_img, img_rect)
            else:
                s = pygame.Surface((ghost.rect.width, ghost.rect.height), pygame.SRCALPHA)
                s.set_alpha(120); s.fill(ghost.color)
                self.canvas.blit(s, ghost.rect)
            
        if data["player"]:
            if self.assets.get("player"):
                img_rect = self.assets["player"].get_rect(center=data["player"].rect.center)
                self.canvas.blit(self.assets["player"], img_rect)
            else: pygame.draw.rect(self.canvas, data["player"].color, data["player"].rect)

        # Işıklandırma
        self._apply_lighting(data)

        # --- UI (İNGİLİZCE GÜNCELLEME) ---
        
        # Zaman -> TIME
        time_text = self.ui_font.render(f"TIME: {data['time_left']}", True, COLOR_TEXT)
        time_x = 20
        if self.assets.get("clock_icon"):
            self.canvas.blit(self.assets["clock_icon"], (20, 20))
            time_x = 70
        self.canvas.blit(time_text, (time_x, 25))
        
        # Bölüm -> LEVEL
        level_text = self.ui_font.render(f"LEVEL: {data['level_index']}", True, (255, 255, 0))
        text_w = level_text.get_width()
        level_x = VIRTUAL_WIDTH - text_w - 30
        if self.assets.get("level_icon"):
            icon_x = VIRTUAL_WIDTH - 60
            self.canvas.blit(self.assets["level_icon"], (icon_x, 20))
            level_x -= 50
        self.canvas.blit(level_text, (level_x, 25))
        
        # Alt Bilgi -> Fullscreen / Exit
        fs_text = self.story_font.render("'F': Fullscreen / 'ESC': Quit", True, (100, 100, 100))
        self.canvas.blit(fs_text, (20, VIRTUAL_HEIGHT - 40))

        # Oyun Sonu Mesajları
        if state == "WON":
            self._draw_centered_text("LEVEL COMPLETE!", (100, 255, 100), -40)
            self._draw_centered_text("Press 'SPACE' to Continue", (255, 255, 255), 40)
        elif state == "GAME_OVER":
            self._draw_centered_text("PARADOX!", (255, 50, 50), -40)
            self._draw_centered_text("Press 'R' to Retry", (255, 255, 255), 40)

    def _apply_lighting(self, data):
        self.darkness.fill((0, 0, 0, 255)) 
        if data["player"]:
            pygame.draw.circle(self.darkness, (0, 0, 0, 0), data["player"].rect.center, 150)
        for ghost in data["ghosts"]:
            pygame.draw.circle(self.darkness, (0, 0, 0, 0), ghost.rect.center, 80)
        self.canvas.blit(self.darkness, (0,0))

    def _draw_briefing(self, data):
        level_idx = data["level_index"]
        story_lines = STORY_TEXTS.get(level_idx, ["Ready?", "Press SPACE."])
        total_height = len(story_lines) * 40
        start_y = (VIRTUAL_HEIGHT - total_height) / 2
        for i, line in enumerate(story_lines):
            text_surface = self.story_font.render(line, True, (180, 200, 255))
            text_rect = text_surface.get_rect(center=(VIRTUAL_WIDTH / 2, start_y + i * 40))
            self.canvas.blit(text_surface, text_rect)

    def _draw_scaled_output(self):
        target_screen = pygame.display.get_surface()
        screen_w, screen_h = target_screen.get_size()
        scale = min(screen_w / VIRTUAL_WIDTH, screen_h / VIRTUAL_HEIGHT)
        new_w = int(VIRTUAL_WIDTH * scale)
        new_h = int(VIRTUAL_HEIGHT * scale)
        start_x = (screen_w - new_w) // 2
        start_y = (screen_h - new_h) // 2
        try: scaled_canvas = pygame.transform.smoothscale(self.canvas, (new_w, new_h))
        except: scaled_canvas = pygame.transform.scale(self.canvas, (new_w, new_h))
        target_screen.fill((0, 0, 0))
        target_screen.blit(scaled_canvas, (start_x, start_y))

    def _draw_centered_text(self, text, color, y_offset):
        msg = self.big_font.render(text, True, color)
        outline = self.big_font.render(text, True, (0,0,0))
        center_pos = (VIRTUAL_WIDTH / 2, VIRTUAL_HEIGHT / 2 + y_offset)
        outline_rect = outline.get_rect(center=(center_pos[0]+3, center_pos[1]+3))
        text_rect = msg.get_rect(center=center_pos)
        self.canvas.blit(outline, outline_rect)
        self.canvas.blit(msg, text_rect)