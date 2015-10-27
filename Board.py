from collections import  namedtuple
import thread
import random
import pygame
from Snake import Snake
from Food import Food
import threading

class Board(object):
    DIRECTIONS = namedtuple('DIRECTIONS',['Up', 'Down', 'Left', 'Right'])(0, 1, 2, 3)


    def __init__(self):
        self.lock=threading.RLock()                                 # MUTEX LOCK FOR SHARED FOOD PARTICLE POSITION
        self.Signal=True                                            # SIGNAL TO KEEP MOVING FOOD PARTICLE
        self.BOARD_LENGTH=40                                        # NO. OF PIXEL IN BOARD
        self.OFFSET = 15                                            # SIZE OF ONE PIXEL
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.food=Food(self)                                        # FOOD CLASS OBJECT
        self.start=pygame.time.get_ticks();                         # KEEPING TRACK OF TIME
        self.end=pygame.time.get_ticks();


    def make_board(self):                                           # INITIALISATION OF BOARD
        spots = [[] for i in range(self.BOARD_LENGTH)]
        for row in spots:
            for i in range(self.BOARD_LENGTH):
                row.append(0)
        return spots


    def find_food(self,spots):                                      # GENERATE NEW VALID POSITION OF FOOD PARTICLE
        while True:
            with self.lock:
                self.food.pos = random.randrange(self.BOARD_LENGTH), random.randrange(self.BOARD_LENGTH)
            if not (spots[self.food.pos[0]][self.food.pos[1]] == 1 or spots[self.food.pos[0]][self.food.pos[1]] == 2):
                break
        return self.food.pos


    def rand_color(self):                                           # RETURN A RANDOM COLOR
        return (random.randrange(254)|64, random.randrange(254)|64, random.randrange(254)|64)


    def is_food(self,board, point):                                 # CHECK GIVEN POINT CONTAIN FOOD OR NOT
        return board[point[0]][point[1]] == 2


    def update_board(self,screen, snake):                           # CREATE BOARD
        rect = pygame.Rect(0, 0,self.OFFSET, self.OFFSET)
        spots = [[] for i in range(self.BOARD_LENGTH)]
        num1 = 0
        num2 = 0
        for row in spots:
            for i in range(self.BOARD_LENGTH):
                row.append(0)
                temprect = rect.move(num1 * self.OFFSET, num2 * self.OFFSET)
                pygame.draw.rect(screen, self.BLACK, temprect)
                num2 += 1
            num1 += 1

        spots[self.food.pos[0]][self.food.pos[1]] = 2
        temprect = rect.move(self.food.pos[1] * self.OFFSET, self.food.pos[0] * self.OFFSET)
        pygame.draw.rect(screen, self.rand_color(), temprect)

        for coord in snake.deque:
                spots[coord[0]][coord[1]] = 1
                temprect = rect.move(coord[1] * self.OFFSET, coord[0] * self.OFFSET)
                pygame.draw.rect(screen, coord[2], temprect)

        return spots


    def end_condition(self,board, coord):                           # CHECK SNAKE IS STRIKING ITSELF OR NOT
        if board[coord[0]][coord[1]] == 1:
            return True
        return False


    def game(self,screen):                                           # MAIN FUNCTION TO START THE GAME
        clock = pygame.time.Clock()
        spots = self.make_board()
        snake = Snake(self)
        spots[0][0] = 1

        with self.lock:
            self.food.pos = self.find_food(spots)

        thread.start_new_thread(self.food.move_food,(snake,))       # THREAD FOR MOVING FOOD PARTICLE

        self.Signal=True

        while True:
            clock.tick(15)
            # Event processing
            self.done = False
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    print("Quit given")
                    self.done = True
                    self.Signal=False
                    break
            if self.done:
                return False

            snake.populate_nextDir(events, "arrows")

            # Game logic
            next_head = snake.move()                                # MOVING SNAKE TO NEXT COORDINATE
            next_head=snake.get_head(next_head)

            if (self.end_condition(spots, next_head)):
                self.Signal=False
                return snake.tailmax

            if self.is_food(spots, next_head):
                snake.tailmax += 4
                self.end=pygame.time.get_ticks();
                count=snake.tailmax/4-2;
                self.food.btimer=float(self.food.btimer*((count+2))/(count+1))+50-float(self.end-self.start)/((count+1)*300);

                print self.food.btimer;

                self.start=pygame.time.get_ticks();
                with self.lock:
                    self.food.pos = self.find_food(spots)

            snake.deque.append(next_head)

            if len(snake.deque) > snake.tailmax:
                snake.deque.popleft()

            # Draw code
            screen.fill(self.BLACK)  # makes screen black
            spots = self.update_board(screen, snake)
            pygame.display.update()
