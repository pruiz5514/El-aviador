import pygame
from draw_text import draw_text
from scores import show_scores

white = (255, 255, 255)
yellow = (255, 255, 0)



def menu(screen_width, screen, clock, fps, bg):
    font = pygame.font.SysFont('Bauhaus 93', 60)
    small_font = pygame.font.SysFont('Bauhaus 93', 40)
    menu = True
    while menu:
        screen.blit(bg, (0, 0))

        title_rect = draw_text(screen, "El Aviador", font, white, screen_width // 2 - 150, 100)
        play_rect = draw_text(screen,"Jugar", small_font, yellow, screen_width // 2 - 70, 300)
        scores_rect = draw_text(screen, "Ver puntajes altos", small_font, yellow, screen_width // 2 - 170, 400)
        exit_rect = draw_text(screen,"Salir", small_font, yellow, screen_width // 2 - 60, 500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    menu = False  
                elif scores_rect.collidepoint(mouse_pos):
                    show_scores(screen, font) 
                elif exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

        pygame.display.update()
        clock.tick(fps)