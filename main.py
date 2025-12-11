import pygame
import sys
from viewmodels.game_viewmodel import GameViewModel
from views.game_view import GameView
from utils.settings import FPS

def main():
    view_model = GameViewModel()
    view = GameView()
    clock = pygame.time.Clock()
    running = True
    
    last_q_press_time = 0 

    while running:
        dx, dy = 0, 0
        
        # --- INPUT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                # --- ÇİFT 'Q' İLE ÇIKIŞ ---
                if event.key == pygame.K_q:
                    current_time = pygame.time.get_ticks()
                    if current_time - last_q_press_time < 1000:
                        running = False
                    else:
                        last_q_press_time = current_time
                        print("Çıkmak için tekrar Q'ya basın!")

                # --- ESC TUŞU ---
                elif event.key == pygame.K_ESCAPE:
                    if view_model.state == "PLAYING":
                        view_model.toggle_pause()
                    elif view_model.state == "PAUSED":
                        view_model.toggle_pause()
                    elif view_model.state == "LEVEL_SELECT":
                        view_model.state = "MENU"

                # --- F TUŞU (TAM EKRAN) ---
                elif event.key == pygame.K_f:
                    view.toggle_fullscreen_mode()

                # --- R TUŞU (RESTART) - DÜZELTİLDİ ---
                elif event.key == pygame.K_r:
                    # Artık sadece oynarken değil;
                    # Oyun bittiyse (GAME_OVER), Kazandıysan (WON) veya Durdurduysan (PAUSED)
                    # R tuşu çalışacak ve bölümü baştan başlatacak.
                    if view_model.state in ["PLAYING", "GAME_OVER", "WON", "PAUSED"]:
                        view_model.full_restart()
                
                # --- SPACE TUŞU (GEÇİŞ) ---
                elif event.key == pygame.K_SPACE:
                    if view_model.state == "WON":
                        view_model.next_level()
                    elif view_model.state == "BRIEFING":
                        view_model.start_level_gameplay()

            # --- FARE TIKLAMASI ---
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Sol Tık
                    action = view.get_click_action(pygame.mouse.get_pos(), view_model.state)
                    if action:
                        response = view_model.process_click(action)
                        if response == "QUIT":
                            running = False

        # --- HAREKET ---
        keys = pygame.key.get_pressed()
        # Sadece oyun oynanırken hareket et
        if view_model.state == "PLAYING":
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = 1
            if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = 1

        view_model.handle_input(dx, dy)
        view_model.update()
        
        # ÇİZİM
        data = view_model.get_render_data()
        view.render(data)
        
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()