import pygame
import sys
from utils.settings import FPS
from viewmodels.game_viewmodel import GameViewModel
from views.game_view import GameView

def main():
    try:
        print("Oyun Başlatılıyor...")
        view_model = GameViewModel()
        view = GameView()
        clock = pygame.time.Clock()
        
        running = True
        while running:
            dx, dy = 0, 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # --- TUŞ KONTROLLERİ ---
                if event.type == pygame.KEYDOWN:
                    
                    # 'F' -> Tam Ekran Aç/Kapa
                    if event.key == pygame.K_f:
                        view.toggle_fullscreen_mode()

                    # 'ESC' -> Tam Ekran Kontrolü ve Çıkış
                    if event.key == pygame.K_ESCAPE:
                        # Eğer Tam Ekrandaysa -> Pencereye Dön
                        if view.fullscreen:
                             view.toggle_fullscreen_mode()
                        # Eğer Zaten Penceredeyse -> Oyunu Kapat
                        else:
                            running = False
                        
                    # 'R' -> Restart
                    data = view_model.get_render_data()
                    current_state = data["state"]
                    if event.key == pygame.K_r and current_state in ["PLAYING", "GAME_OVER"]:
                        view_model.full_restart()
                    
                    # 'SPACE' -> Geçiş
                    if event.key == pygame.K_SPACE:
                        if current_state == "WON":
                            view_model.next_level()
                        elif current_state == "BRIEFING":
                            view_model.start_level()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:  dx = -1
            if keys[pygame.K_RIGHT]: dx = 1
            if keys[pygame.K_UP]:    dy = -1
            if keys[pygame.K_DOWN]:  dy = 1

            view_model.handle_input(dx, dy)
            view_model.update()
            
            render_data = view_model.get_render_data()
            view.render(render_data)

            clock.tick(FPS)

        pygame.quit()
        sys.exit()

    except Exception as e:
        print("KRİTİK HATA:", e)
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()