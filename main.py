"""
    Date of completion: 27-10-2015
                                            Advance Snake Game
    Developed a Snake Game with MOVING FOOD PARTICLE,with an idea of enhancing the players's response time.
    Implemented in python using Pygame library,used Threading to control both object separately and mutex lock for
    shared attributes.

"""

import pygame
from Board import Board


def menu(screen,board):                               # TO SHOW MENU FOR THE GAME
    font = pygame.font.Font(None, 30)
    menu_message1 = font.render("Press enter to start the GAME", True, board.WHITE)
    screen.fill(board.BLACK)
    screen.blit(menu_message1, (32, 32))
    pygame.display.update()

    while True:
       Board.done = False
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             Board.done = True
          elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_RETURN:
                return 1
    pygame.display.update()
    return 1


def game_over(screen, eaten,board):                   # GAME OVER MENU OF THE GAME
    message1 = "You ate %d foods" % eaten
    message2 = "Press enter to play again, esc to quit."
    game_over_message1 = pygame.font.Font(None, 30).render(message1, True, board.BLACK)
    game_over_message2 = pygame.font.Font(None, 30).render(message2, True, board.BLACK)

    overlay = pygame.Surface((board.BOARD_LENGTH * board.OFFSET, board.BOARD_LENGTH * board.OFFSET))
    overlay.fill((84, 84, 84))
    overlay.set_alpha(150)
    screen.blit(overlay, (0,0))

    screen.blit(game_over_message1, (35, 35))
    screen.blit(game_over_message2, (65, 65))
    game_over_message1 = pygame.font.Font(None, 30).render(message1, True, board.WHITE)
    game_over_message2 = pygame.font.Font(None, 30).render(message2, True, board.WHITE)
    screen.blit(game_over_message1, (32, 32))
    screen.blit(game_over_message2, (62, 62))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_RETURN:
                    return True


def main():                                                         # MAIN MENU OF THE GAME
    pygame.init()                                                   # INITIALISATION OF PYGAME LIBRARY
    board=Board()                                                   # INITIALISATION OF BOARD CLASS
    screen = pygame.display.set_mode([board.BOARD_LENGTH * board.OFFSET,board.BOARD_LENGTH * board.OFFSET])
    pygame.display.set_caption("Snake")
    pygame.draw.rect(screen,pygame.Color(255,255,255,255),pygame.Rect(50,50,10,10))
    playing = True

    pick = menu(screen,board)

    while playing:
        now = board.game(screen)                                     # STARTING GAME BY CALLING GAME
        if now == False:
            break
        elif pick == 1 or pick == 2:
            eaten = now / 4 - 2
            playing = game_over(screen, eaten,board)                 # DISPLAYING RESULT OF GAME

    pygame.quit()

if __name__ == "__main__":
    main()

