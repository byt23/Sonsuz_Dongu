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
        pygame.display.set_caption("Time-Loop Co-op Project")
        
        # 2. Sanal Tuval
        self.canvas = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        self.fullscreen = False
        
        # --- 3. FONT TANIMLAMASI ---
        font_path = os.path.join("assets", "font.ttf") 
        self.ui_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.story_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 60, bold=True)

        try:
            if os.path.exists(font_path):
                self.ui_font = pygame.font.Font(font_path, 40) 
                self.story_font = pygame.font.Font(font_path, 30)
                self.big_font = pygame.font.Font(font_path, 60)
            else:
                print("UYARI: font.ttf bulunamadı, Arial kullanılıyor.")
        except Exception as e:
            print(f"KRİTİK FONT HATASI: {e}")

        # 4. Görselleri Yükle
        self.assets = {}
        self._load_assets()
        
        # 5. Işıklandırma Katmanı
        self.darkness = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)

    def _load_assets(self):
        """Resimleri assets/images klasöründen yükler."""
        img_dir = os.path.join("assets", "images")
        
        files = {
            "wall": "wall.png", 
            "floor": "floor.png",
            "player": "player.png",
            "exit": "exit.png",
            "button": "button.png" # <-- YENİ: Buton eklendi
        }
        
        print("--- GÖRSELLER YÜKLENİYOR ---")
        for key, filename in files.items():
            path = os.path.join(img_dir, filename)
            try:
                img = pygame.image.load(path).convert_alpha()
                
                # --- KARAKTER BOYUT AYARI ---
                if key == "player":
                    # Karakter küçük kalsın (%60)
                    char_size = int(TILE_SIZE * 0.6) 
                    img = pygame.transform.scale(img, (char_size, char_size))
                else:
                    # Diğerleri tam boy (80px)
                    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                
                self.assets[key] = img
                print(f"[OK] {filename} yüklendi.")
            except FileNotFoundError:
                print(f"[HATA] {filename} bulunamadı! Kare çizilecek.")
                self.assets[key] = None

    def toggle_fullscreen_mode(self):
        """Tam Ekran / Pencere modu geçişi"""
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
        state = data["state"]
        
        if state == "BRIEFING":
            self.canvas.fill((5, 5, 10)); self._draw_briefing(data); return
        elif state == "GAME_FINISHED":
            self.canvas.fill((0, 0, 0)); self._draw_centered_text("TEBRİKLER! OYUN BİTTİ.", (0, 255, 255), 0); return
        
        # --- 1. ZEMİN ---
        if self.assets.get("floor"):
            for row in range(VIRTUAL_HEIGHT // TILE_SIZE + 1):
                for col in range(VIRTUAL_WIDTH // TILE_SIZE + 1):
                    self.canvas.blit(self.assets["floor"], (col * TILE_SIZE, row * TILE_SIZE))
        else: self.canvas.fill(COLOR_BG)
        
        # --- 2. DUVARLAR ---
        for wall in data["walls"]: 
            if self.assets.get("wall"): self.canvas.blit(self.assets["wall"], wall.rect)
            else: pygame.draw.rect(self.canvas, wall.color, wall.rect)

        # --- 3. ÇIKIŞ ---
        if data["exit"]: 
            if self.assets.get("exit"):
                self.canvas.blit(self.assets["exit"], data["exit"].rect)
            else:
                pygame.draw.rect(self.canvas, data["exit"].color, data["exit"].rect)
        
        # --- 4. BUTONLAR (GÜNCELLENDİ) ---
        for button in data["buttons"]: 
            if self.assets.get("button"):
                # Resmi kopyala
                btn_img = self.assets["button"].copy()
                # Butonun o anki rengini (Kırmızı/Mavi/Yeşil) resmin üzerine uygula
                btn_img.fill(button.color, special_flags=pygame.BLEND_MULT)
                self.canvas.blit(btn_img, button.rect)
            else:
                pygame.draw.rect(self.canvas, button.color, button.rect)

        # --- 5. KAPILAR (SADE KARE) ---
        for door in data["doors"]:
            if door.is_open: pygame.draw.rect(self.canvas, COLOR_DOOR_OPEN, door.rect, 2)
            else: pygame.draw.rect(self.canvas, door.color, door.rect)
        
        # --- 6. KARAKTER VE HAYALETLER ---
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
            else:
                pygame.draw.rect(self.canvas, data["player"].color, data["player"].rect)

        # --- 7. IŞIKLANDIRMA (ZİFİRİ KARANLIK) ---
        self._apply_lighting(data)

        # --- 8. UI ---
        time_text = self.ui_font.render(f"Zaman: {data['time_left']}", True, COLOR_TEXT)
        self.canvas.blit(time_text, (20, 20))
        
        level_text = self.ui_font.render(f"Bölüm: {data['level_index']}", True, (255, 255, 0))
        self.canvas.blit(level_text, (VIRTUAL_WIDTH - 200, 20))
        
        fs_text = self.story_font.render("'F' -> Tam Ekran / 'ESC' -> Çık", True, (100, 100, 100))
        self.canvas.blit(fs_text, (20, VIRTUAL_HEIGHT - 40))

        if state == "WON":
            self._draw_centered_text("BOLUM TAMAMLANDI!", (100, 255, 100), -40)
            self._draw_centered_text("'SPACE' ile Devam Et", (255, 255, 255), 40)
        elif state == "GAME_OVER":
            self._draw_centered_text("PARADOKS!", (255, 50, 50), -40)
            self._draw_centered_text("'R' ile Tekrar Dene", (255, 255, 255), 40)

    def _apply_lighting(self, data):
        self.darkness.fill((0, 0, 0, 255)) 
        if data["player"]:
            pygame.draw.circle(self.darkness, (0, 0, 0, 0), data["player"].rect.center, 150)
        for ghost in data["ghosts"]:
            pygame.draw.circle(self.darkness, (0, 0, 0, 0), ghost.rect.center, 80)
        self.canvas.blit(self.darkness, (0,0))

    def _draw_briefing(self, data):
        level_idx = data["level_index"]
        story_lines = STORY_TEXTS.get(level_idx, ["Hazır?", "SPACE bas."])
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
        try:
            scaled_canvas = pygame.transform.smoothscale(self.canvas, (new_w, new_h))
        except:
            scaled_canvas = pygame.transform.scale(self.canvas, (new_w, new_h))
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