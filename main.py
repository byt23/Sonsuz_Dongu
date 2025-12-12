import pygame, sys, traceback
try:
    from models.game_model import GameModel
    from viewmodels.game_viewmodel import GameViewModel
    from views.game_view import GameView
    from utils.settings import FPS
    from utils.sound_manager import SoundManager

    def main():
        pygame.init(); clock = pygame.time.Clock()
        gm = GameModel(); vm = GameViewModel(gm); v = GameView(); sm = SoundManager()
        run = True; last_q = 0
        while run:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: run = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        if pygame.time.get_ticks() - last_q < 1000: run = False
                        else: last_q = pygame.time.get_ticks()
                    elif e.key == pygame.K_l:
                        if vm.state in ["INTRO", "MENU"]: vm.cycle_language()
                    elif e.key == pygame.K_RETURN:
                        if vm.state == "INTRO": vm.skip_intro()
                    elif e.key == pygame.K_ESCAPE:
                        if vm.state in ["PLAYING", "PAUSED"]: vm.toggle_pause()
                        elif vm.state == "LEVEL_SELECT": vm.state = "MENU"
                    elif e.key == pygame.K_f: v.toggle_fullscreen_mode()
                    elif e.key == pygame.K_r:
                        if vm.state in ["PLAYING", "GAME_OVER", "WON", "PAUSED"]: vm.full_restart()
                    elif e.key == pygame.K_SPACE:
                        if vm.state == "WON": vm.next_level()
                        elif vm.state == "BRIEFING": vm.start_level_gameplay()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        act = v.get_click_action(pygame.mouse.get_pos(), vm.state)
                        if act: 
                            if vm.process_click(act) == "QUIT": run = False
            
            dx, dy = 0, 0
            if vm.state == "PLAYING":
                k = pygame.key.get_pressed()
                if k[pygame.K_LEFT] or k[pygame.K_a]: dx = -1
                if k[pygame.K_RIGHT] or k[pygame.K_d]: dx = 1
                if k[pygame.K_UP] or k[pygame.K_w]: dy = -1
                if k[pygame.K_DOWN] or k[pygame.K_s]: dy = 1
            
            vm.handle_input(dx, dy); vm.update()
            for s in vm.sound_queue: sm.play(s)
            vm.sound_queue.clear()
            v.render(vm.get_render_data())
            clock.tick(FPS)
        pygame.quit(); sys.exit()

    if __name__ == "__main__": main()
except Exception as e:
    print(f"\nCRASH: {e}\n"); traceback.print_exc(); pygame.quit(); input("Press ENTER...")