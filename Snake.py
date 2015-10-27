import pygame
from collections import deque

class Snake(object):
    def __init__(self,board):
        self.board=board                                            # BOARD OBJECT
        self.point=(0, 0, board.rand_color())
        self.color=None
        self.tailmax = 10                                           # LENGTH OF SNAKE
        self.direction = board.DIRECTIONS.Right
        self.deque = deque()                                        # SNAKE COORDINATE
        self.deque.append(self.point)
        self.nextDir = deque()                                      # QUEUE OF NEXT DIRECTION

    def get_color(self):
        if self.color is None:
            return self.board.rand_color()
        else:
            return self.color

    def populate_nextDir(self, events, identifier):
        if (identifier == "arrows"):
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.nextDir.appendleft(self.board.DIRECTIONS.Up)
                    elif event.key == pygame.K_DOWN:
                        self.nextDir.appendleft(self.board.DIRECTIONS.Down)
                    elif event.key == pygame.K_RIGHT:
                        self.nextDir.appendleft(self.board.DIRECTIONS.Right)
                    elif event.key == pygame.K_LEFT:
                        self.nextDir.appendleft(self.board.DIRECTIONS.Left)

    def get_head(self,next_head):                                       # MOVE SNAKE HEAD TO NEXT COORDINATE
        head=list(next_head)
        if(next_head[0]<0):
            head[0]=self.board.BOARD_LENGTH-1
        elif(next_head[0]>=self.board.BOARD_LENGTH):
            head[0]=0

        if(next_head[1]<0):
            head[1]=self.board.BOARD_LENGTH-1
        elif(next_head[1]>=self.board.BOARD_LENGTH):
            head[1]=0

        return head


    def move(self):                                                     # MOVING SNAKE
        if len(self.nextDir) != 0:
            next_dir = self.nextDir.pop()
        else:
            next_dir = self.direction

        head = self.deque.pop()
        self.deque.append(head)

        if (next_dir == self.board.DIRECTIONS.Up):
            if self.direction != self.board.DIRECTIONS.Down:
                next_move =  (head[0] - 1, head[1], self.get_color())
                self.direction = next_dir
            else:
                next_move =  (head[0] + 1, head[1], self.get_color())

        elif (next_dir == self.board.DIRECTIONS.Down):
            if self.direction != self.board.DIRECTIONS.Up:
                next_move =  (head[0] + 1, head[1], self.get_color())
                self.direction = next_dir
            else:
                next_move =  (head[0] - 1, head[1], self.get_color())

        elif (next_dir == self.board.DIRECTIONS.Left):
            if self.direction != self.board.DIRECTIONS.Right:
                next_move =  (head[0], head[1] - 1, self.get_color())
                self.direction = next_dir
            else:
                next_move =  (head[0], head[1] + 1, self.get_color())

        elif (next_dir == self.board.DIRECTIONS.Right):
            if self.direction != self.board.DIRECTIONS.Left:
                next_move =  (head[0], head[1] + 1, self.get_color())
                self.direction = next_dir
            else:
                next_move =  (head[0], head[1] - 1, self.get_color())

        return next_move
