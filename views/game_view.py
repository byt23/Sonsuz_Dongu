import pygame, os
from utils.settings import *

class GameView:
    def __init__(self):
        pygame.init()
        self.width, self.height = VIRTUAL_WIDTH, VIRTUAL_HEIGHT
        current_script_path = os.path.abspath(__file__)
        self.project_root = os.path.dirname(os.path.dirname(current_script_path))
        self.screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Time-Loop Co-op: Kronos Protocol")
        self.canvas = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        self.fullscreen = False
        self.display_info = pygame.display.Info()
        self.desktop_w, self.desktop_h = self.display_info.current_w, self.display_info.current_h
        self._load_fonts(); self.assets = {}; self._load_assets()
        self.darkness = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        self.menu_buttons = {}; self.level_buttons = {}; self.pause_buttons = {}

    def _load_fonts(self):
        font_path = os.path.join(self.project_root, "assets", "font.ttf")
        try:
            if os.path.exists(font_path):
                self.ui_font = pygame.font.Font(font_path, 36)
                self.story_font = pygame.font.Font(font_path, 24)
                self.big_font = pygame.font.Font(font_path, 80)
            else: raise FileNotFoundError
        except:
            self.ui_font = pygame.font.SysFont("Arial", 36, bold=True)
            self.story_font = pygame.font.SysFont("Arial", 24, bold=True)
            self.big_font = pygame.font.SysFont("Arial", 80, bold=True)

    def _load_assets(self):
        img_dir = os.path.join(self.project_root, "assets", "images")
        files = {"wall":"wall.png", "floor":"floor.png", "player":"player.png", "exit":"exit.png", "button":"button.png", "clock_icon":"clock_icon.png", "level_icon":"level_icon.png", "intro_bg":"intro.png"}
        for key, filename in files.items():
            path = os.path.join(img_dir, filename)
            try:
                img = pygame.image.load(path).convert_alpha()
                if key == "player": img = pygame.transform.scale(img, (int(TILE_SIZE * 0.6), int(TILE_SIZE * 0.6)))
                elif key in ["clock_icon", "level_icon"]: img = pygame.transform.scale(img, (40, 40))
                elif key in ["button", "exit"]: img = pygame.transform.scale(img, (int(TILE_SIZE * 0.7), int(TILE_SIZE * 0.7)))
                elif key == "intro_bg": img = pygame.transform.scale(img, (400, 200))
                else: img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                self.assets[key] = img
            except: self.assets[key] = None

    def toggle_fullscreen_mode(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen: self.screen = pygame.display.set_mode((self.desktop_w, self.desktop_h), pygame.FULLSCREEN)
        else: self.screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)

    def render(self, data):
        state = data["state"]; texts = data.get("texts", {})
        if state == "INTRO": self._draw_intro(texts)
        elif state == "MENU": self._draw_menu(texts)
        elif state == "LEVEL_SELECT": self._draw_level_select(data["unlocked_levels"], texts)
        elif state == "BRIEFING":
            self.canvas.fill((5, 5, 10)); self._draw_briefing(data, texts)
        elif state in ["PLAYING", "WON", "GAME_OVER"]: self._draw_game(data, texts)
        elif state == "PAUSED": self._draw_game(data, texts); self._draw_pause_menu(texts)
        elif state == "GAME_FINISHED":
            self.canvas.fill((0, 0, 0)); self._draw_centered_text(texts.get("SIMULATION_COMPLETE", "END"), (0, 255, 0), 0)
        self._draw_scaled_output(); pygame.display.flip()

    def _draw_intro(self, texts):
        self.canvas.fill((0, 0, 0))
        self._draw_centered_text(texts.get("INTRO_TITLE", "KRONOS"), (0, 255, 0), -250)
        intro_img = self.assets.get("intro_bg")
        img_rect = pygame.Rect(0, 0, 400, 200); img_rect.center = (VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2 - 50)
        if intro_img: self.canvas.blit(intro_img, img_rect); pygame.draw.rect(self.canvas, (0, 255, 0), img_rect, 2)
        else: pygame.draw.rect(self.canvas, (50, 50, 50), img_rect, 2)
        story = texts.get("INTRO_STORY", "").split("\n"); start_y = VIRTUAL_HEIGHT // 2 + 80
        for i, line in enumerate(story):
            l = self.story_font.render(line, True, (200, 200, 200))
            self.canvas.blit(l, l.get_rect(center=(VIRTUAL_WIDTH // 2, start_y + i * 30)))
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            e = self.ui_font.render(texts.get("PRESS_ENTER", "ENTER"), True, (0, 255, 255))
            self.canvas.blit(e, e.get_rect(center=(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT - 80)))
        l = self.story_font.render(texts.get("CHANGE_LANG", "L: Language"), True, (150, 150, 150))
        self.canvas.blit(l, l.get_rect(center=(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT - 40)))

    def _draw_game(self, data, texts):
        if self.assets.get("floor"):
             for r in range(VIRTUAL_HEIGHT//TILE_SIZE+1):
                for c in range(VIRTUAL_WIDTH//TILE_SIZE+1): self.canvas.blit(self.assets["floor"], (c*TILE_SIZE, r*TILE_SIZE))
        else: self.canvas.fill(COLOR_BG)
        for b in data["buttons"]:
            lnk = next((d for d in data["doors"] if d.link_id == b.link_id), None)
            if lnk: pygame.draw.line(self.canvas, b.color, b.rect.center, lnk.rect.center, 6 if b.is_pressed else 2)
        for w in data["walls"]: 
            if self.assets.get("wall"): self.canvas.blit(self.assets["wall"], w.rect)
            else: pygame.draw.rect(self.canvas, w.color, w.rect)
        if data["exit"]:
            if self.assets.get("exit"): self.canvas.blit(self.assets["exit"], self.assets["exit"].get_rect(center=data["exit"].rect.center))
            else: pygame.draw.rect(self.canvas, data["exit"].color, data["exit"].rect)
        for b in data.get("boxes", []): pygame.draw.rect(self.canvas, b.color, b.rect)
        for l in data.get("lasers", []): 
            if l.active: pygame.draw.rect(self.canvas, l.color, l.rect)
        for b in data["buttons"]:
            if self.assets.get("button"):
                i = self.assets["button"].copy(); i.fill(b.color, special_flags=pygame.BLEND_MULT)
                self.canvas.blit(i, i.get_rect(center=b.rect.center))
            else: pygame.draw.rect(self.canvas, b.color, b.rect)
        for d in data["doors"]:
            if d.is_open: pygame.draw.rect(self.canvas, d.color, d.rect, 6)
            else: pygame.draw.rect(self.canvas, d.color, d.rect)
        for g in data["ghosts"]:
            if self.assets.get("player"):
                i = self.assets["player"].copy(); i.set_alpha(100); i.fill((200, 200, 200), special_flags=pygame.BLEND_MULT)
                self.canvas.blit(i, i.get_rect(center=g.rect.center))
            else: s=pygame.Surface((g.rect.w, g.rect.h), pygame.SRCALPHA); s.fill((*g.color, 150)); self.canvas.blit(s, g.rect)
        if data["player"]:
            if self.assets.get("player"): self.canvas.blit(self.assets["player"], self.assets["player"].get_rect(center=data["player"].rect.center))
            else: pygame.draw.rect(self.canvas, data["player"].color, data["player"].rect)
        self._apply_lighting(data)
        t = self.ui_font.render(f"{texts.get('TIME')}: {data['time_left']}", True, (255,255,255))
        self.canvas.blit(t, (70 if self.assets.get("clock_icon") else 20, 25))
        if self.assets.get("clock_icon"): self.canvas.blit(self.assets["clock_icon"], (20, 20))
        l = self.ui_font.render(f"{texts.get('LEVEL')}: {data['level_index']}", True, (255, 255, 0))
        lx = VIRTUAL_WIDTH - l.get_width() - 30
        if self.assets.get("level_icon"): self.canvas.blit(self.assets["level_icon"], (VIRTUAL_WIDTH-60, 20)); lx-=50
        self.canvas.blit(l, (lx, 25))
        f = self.story_font.render(texts.get("FULLSCREEN_TIP"), True, (100, 100, 100))
        self.canvas.blit(f, (20, VIRTUAL_HEIGHT-40))
        if data["state"] == "WON": self._draw_centered_text(texts.get("LEVEL_COMPLETE"), (100, 255, 100), -40); self._draw_centered_text(texts.get("PRESS_SPACE"), (255, 255, 255), 40)
        elif data["state"] == "GAME_OVER": self._draw_centered_text(texts.get("PARADOX"), (255, 50, 50), -40); self._draw_centered_text(texts.get("PRESS_R"), (255, 255, 255), 40)

    def _draw_briefing(self, data, texts):
        key = f"S{data['level_index']}"; lines = texts.get(key, ["Ready?", "Press SPACE."])
        start_y = (VIRTUAL_HEIGHT - len(lines)*40) / 2
        for i, l in enumerate(lines): t = self.story_font.render(l, True, (180, 200, 255)); self.canvas.blit(t, t.get_rect(center=(VIRTUAL_WIDTH/2, start_y + i*40)))

    def _apply_lighting(self, data):
        self.darkness.fill((0, 0, 0, 255))
        if data["player"]: pygame.draw.circle(self.darkness, (0,0,0,0), data["player"].rect.center, 150)
        for g in data["ghosts"]: pygame.draw.circle(self.darkness, (0,0,0,0), g.rect.center, 80)
        self.canvas.blit(self.darkness, (0,0))

    def _draw_menu(self, texts):
        self.canvas.fill(COLOR_BG)
        self._draw_centered_text(texts.get("GAME_TITLE"), (0, 255, 255), -150)
        bw, bh = 500, 60; bx = VIRTUAL_WIDTH//2 - bw//2
        btn_start = pygame.Rect(bx, 350, bw, bh); btn_levels = pygame.Rect(bx, 430, bw, bh)
        btn_lang = pygame.Rect(bx, 510, bw, bh); btn_quit = pygame.Rect(bx, 590, bw, bh)
        self._draw_button(btn_start, texts.get("START_GAME"), (0, 200, 0))
        self._draw_button(btn_levels, texts.get("LEVELS"), (200, 200, 0))
        self._draw_button(btn_lang, texts.get("LANGUAGE"), (50, 150, 200))
        self._draw_button(btn_quit, texts.get("QUIT"), (200, 50, 50))
        self.menu_buttons = {"START_GAME": btn_start, "OPEN_LEVELS": btn_levels, "CHANGE_LANGUAGE": btn_lang, "QUIT_GAME": btn_quit}

    def _draw_pause_menu(self, texts):
        s = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA); s.fill((0, 0, 0, 150)); self.canvas.blit(s, (0,0))
        self._draw_centered_text(texts.get("PAUSED"), (255, 255, 255), -150)
        bw, bh = 500, 60; bx = VIRTUAL_WIDTH//2 - bw//2
        btn_r = pygame.Rect(bx, 300, bw, bh); btn_l = pygame.Rect(bx, 380, bw, bh); btn_m = pygame.Rect(bx, 460, bw, bh)
        self._draw_button(btn_r, texts.get("RESUME"), (0, 200, 0))
        self._draw_button(btn_l, texts.get("LEVEL_SELECT"), (200, 200, 0))
        self._draw_button(btn_m, texts.get("MAIN_MENU"), (200, 50, 50))
        self.pause_buttons = {"RESUME_GAME": btn_r, "PAUSE_TO_LEVELS": btn_l, "PAUSE_TO_MENU": btn_m}

    def _draw_level_select(self, unlocked, texts):
        self.canvas.fill(COLOR_BG); self._draw_centered_text(texts.get("SELECT_LEVEL"), (255, 255, 255), -250)
        b = pygame.Rect(50, 50, 200, 50); self._draw_button(b, texts.get("BACK"), (100, 100, 100))
        self.level_buttons = {"BACK_TO_MENU": b}
        sx, sy, p, s = 240, 200, 20, 80
        for i in range(1, 16):
            r, c = (i-1)//5, (i-1)%5; rect = pygame.Rect(sx+c*(s+p), sy+r*(s+p), s, s)
            lock = i > unlocked; col = (50, 50, 50) if lock else (0, 255, 255)
            pygame.draw.rect(self.canvas, col, rect, border_radius=10); pygame.draw.rect(self.canvas, (255,255,255), rect, 3, border_radius=10)
            l = self.ui_font.render(str(i), True, (100,100,100) if lock else (0,0,0))
            self.canvas.blit(l, l.get_rect(center=rect.center))
            if not lock: self.level_buttons[f"LEVEL_{i}"] = rect

    def _draw_button(self, r, t, c):
        pygame.draw.rect(self.canvas, c, r, border_radius=5); pygame.draw.rect(self.canvas, (255,255,255), r, 2, border_radius=5)
        l = self.ui_font.render(t, True, (255,255,255)); self.canvas.blit(l, l.get_rect(center=r.center))

    def _draw_centered_text(self, t, c, o):
        l = self.big_font.render(t, True, c); self.canvas.blit(l, l.get_rect(center=(VIRTUAL_WIDTH//2, VIRTUAL_HEIGHT//2 + o)))

    def _draw_scaled_output(self):
        ts = pygame.display.get_surface(); sw, sh = ts.get_size()
        scale = min(sw/VIRTUAL_WIDTH, sh/VIRTUAL_HEIGHT)
        nw, nh = int(VIRTUAL_WIDTH*scale), int(VIRTUAL_HEIGHT*scale)
        try: sc = pygame.transform.smoothscale(self.canvas, (nw, nh))
        except: sc = pygame.transform.scale(self.canvas, (nw, nh))
        ts.fill((0,0,0)); ts.blit(sc, ((sw-nw)//2, (sh-nh)//2))

    def get_click_action(self, pos, state):
        sw, sh = self.screen.get_size(); scale = min(sw/VIRTUAL_WIDTH, sh/VIRTUAL_HEIGHT)
        nw, nh = int(VIRTUAL_WIDTH*scale), int(VIRTUAL_HEIGHT*scale)
        sx, sy = (sw-nw)//2, (sh-nh)//2; vx, vy = (pos[0]-sx)/scale, (pos[1]-sy)/scale
        if state == "MENU": return next((n for n, r in self.menu_buttons.items() if r.collidepoint(vx, vy)), None)
        elif state == "LEVEL_SELECT": return next((n for n, r in self.level_buttons.items() if r.collidepoint(vx, vy)), None)
        elif state == "PAUSED": return next((n for n, r in self.pause_buttons.items() if r.collidepoint(vx, vy)), None)
        return None