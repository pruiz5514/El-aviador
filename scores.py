import json
import pygame
from draw_text import draw_text

def save_score(score):
    try:
        with open("scores.json", "r") as file:
            scores = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        scores = []

    scores.append(score)
    scores.sort(reverse=True) 

    scores = scores[:3]

    with open("scores.json", "w") as file:
        json.dump(scores, file)

def show_scores(screen, font):
    try:
        with open("scores.json", "r") as file:
            scores = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        scores = []

    screen.fill((0, 0, 0)) 

    draw_text(screen, " Mejores Puntajes ", font, (255, 255, 255), 100, 100)

    for idx, puntaje in enumerate(scores):
        draw_text(screen, f"{idx + 1}. {puntaje}", font, (255, 255, 255), 100, 180 + idx * 60)

    draw_text(screen, "Presiona cualquier tecla para volver", pygame.font.SysFont('Bauhaus 93', 30), (200, 200, 200), 100, 400)
    pygame.display.update()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                esperando = False