import pygame, sys
from gameController import Game
from colors import Colors
import sqlite3 as sq
from player import Player

pygame.init()

connection = sq.connect('scoreboard.db')
cursor = connection.cursor()

title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Счёт", True, Colors.white)
next_surface = title_font.render("След.", True, Colors.white)
game_over_surface = title_font.render("Проигрыш", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Tetris")

CLOCK = pygame.time.Clock()
FPS = 60

game_control = Game()
player_data = Player()

GAME_UPDATE = pygame.USEREVENT  # для ускорения падения блоков
pygame.time.set_timer(GAME_UPDATE, 200)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu(game_contr, player):
    p = player
    g = game_contr
    username = ''
    click = False
    while True:
        screen.fill(Colors.bg_color)
        draw_text('Главное меню', title_font, (255, 255, 255), screen, 155, 100)

        mx, my = pygame.mouse.get_pos()

        button_play = pygame.Rect(150, 200, 200, 50)
        button_lb = pygame.Rect(150, 300, 200, 50)

        if button_play.collidepoint((mx, my)):
            if click:
                p.name = username
                game(g, p)
        if button_lb.collidepoint((mx, my)):
            if click:
                scoreboard()
        pygame.draw.rect(screen, Colors.cyan, button_play, border_radius=4)  # кнопка
        draw_text('Играть', title_font, Colors.white, screen, 200, 215)  # "Играть"

        pygame.draw.rect(screen, Colors.cyan, button_lb, border_radius=4)  # кнопка
        draw_text('Лидеры', title_font, Colors.white, screen, 190, 315)  # "лидеры"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                connection.commit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                username += event.unicode
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.K_BACKSPACE:
                username = username[:-1]

        enter_name_surface = title_font.render('Введите свой логин: ', True, Colors.white)
        screen.blit(enter_name_surface, (110, 400))

        name_input_surface = title_font.render(username, True, Colors.white)
        screen.blit(name_input_surface, (200, 450))

        pygame.display.update()
        CLOCK.tick(60)


def scoreboard():
    leaders = fetch_leaders()
    run = True

    while run:
        screen.fill(Colors.bg_color)

        draw_text('Таблица лидеров', title_font, (255, 255, 255), screen, 125, 50)
        for i in range(len(leaders)):
            draw_text(leaders[i][0], title_font, Colors.white, screen, 125, 100 + i * 50)
            draw_text(str(leaders[i][1]), title_font, Colors.white, screen, 300, 100 + i * 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                connection.commit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    # pygame.quit()
                    # sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        CLOCK.tick(60)


def game(g, player_data):
    game = g
    p = player_data
    run = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                p.score = game.score
                insert_db(p.return_data())
                connection.commit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game.game_over == True:
                    game.game_over = False
                    game.reset()
                if event.key == pygame.K_LEFT and game.game_over == False:
                    game.move_left()
                if event.key == pygame.K_RIGHT and game.game_over == False:
                    game.move_right()
                if event.key == pygame.K_DOWN and game.game_over == False:
                    game.move_down()
                    game.update_score(0, 1)
                if event.key == pygame.K_UP and game.game_over == False:
                    game.rotate()
            if event.type == GAME_UPDATE and game.game_over == False:
                game.move_down()

        score_value_surface = title_font.render(str(game.score), True, Colors.white)

        screen.fill(Colors.bg_color)
        screen.blit(score_surface, (365, 20, 50, 50))
        screen.blit(next_surface, (375, 180, 50, 50))

        if game.game_over == True:
            screen.blit(game_over_surface, (320, 450, 50, 50))

        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,
                                                                      centery=score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        game.draw(screen)

        pygame.display.update()
        CLOCK.tick(FPS)


def insert_db(data):
    cursor.execute('INSERT INTO sb (name, score) VALUES(?, ?)', data)


def fetch_leaders():
    cursor.execute('SELECT * FROM sb ORDER BY score DESC LIMIT 10')
    top = cursor.fetchall()
    return top


main_menu(game_control, player_data)
