import pygame,sys
from gameController import Game
from colors import Colors

pygame.init()

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

game = Game()

GAME_UPDATE = pygame.USEREVENT  # для ускорения падения блоков
pygame.time.set_timer(GAME_UPDATE, 200)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu(game):
    g = game
    while True:

        screen.fill(Colors.bg_color)
        draw_text('Главное меню', title_font, (255, 255, 255), screen, 155, 100)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(150, 200, 200, 50)
        draw_text('Играть', title_font, (255, 255, 255), screen, 150, 200)

        button_2 = pygame.Rect(150, 300, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                g = Game()
                game(g)
        if button_2.collidepoint((mx, my)):
            if click:
                scoreboard()
        pygame.draw.rect(screen, Colors.cyan, button_1, border_radius=4)
        pygame.draw.rect(screen, Colors.cyan, button_2, border_radius=4)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        CLOCK.tick(60)

def scoreboard():
    while True:
        screen.fill(Colors.bg_color)

        draw_text('Предыдущие результаты', title_font, (255, 255, 255), screen, 80, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        CLOCK.tick(60)

def game(gam):
    game = gam
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
            run = False


        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx,
            centery = score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        game.draw(screen)

        pygame.display.update()
        CLOCK.tick(FPS)

main_menu(game)