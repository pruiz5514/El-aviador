import pygame

def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    rect = img.get_rect()
    rect.topleft = (x, y)
    screen.blit(img, rect)
    return rect
