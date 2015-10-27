import pygame
import random

class Food(object):                                                 # FOOD CLASS

    def __init__(self,board):
        self.btimer=40;                                             # TIMER FOR DELAY
        self.board=board                                            # BOARD OBJECT
        self.pos=15,15                                              # FOOD PARTICLE

    def valid(self,snake,coord):                                    # CHECK VALID POINT FOR FOOD PARTICLE
        if (coord[0] < 0 or coord[0] >= self.board.BOARD_LENGTH or coord[1] < 0 or coord[1] >= self.board.BOARD_LENGTH):
            return False
        for i in list(snake.deque):
            if((coord[0],coord[1]) ==(i[0],i[1])):
                return False
        return True


    def move_food(self,snake):                                      # MOVE FOOD PARTICLE

        last=0;
        clock=pygame.time.Clock()
        while self.board.Signal:
            
            if(self.btimer>8):
                self.btimer-=1
            else:
                self.btimer=6;

            delay=(self.btimer/5)

            clock.tick(delay)
            x=random.randrange(12)                                     # MOVING IN SAME DIRECTION MOST OF THE TIME
            if(x>3):
                x=last
            if(x==1):
                last=x
                if(self.valid(snake,(self.pos[0],self.pos[1]+1))):
                    with self.board.lock:
                        self.pos=list(self.pos)
                        self.pos[1]=self.pos[1]+1
            elif(x==0):
                last=x
                if(self.valid(snake,(self.pos[0]+1,self.pos[1]))):
                    with self.board.lock:
                        self.pos=list(self.pos)
                        self.pos[0]=self.pos[0]+1

            elif(x==2):
                last=x
                if(self.valid(snake,(self.pos[0]-1,self.pos[1]))):
                    with self.board.lock:
                        self.pos=list(self.pos)
                        self.pos[0]=self.pos[0]-1

            elif(x==3):
                last=x
                if(self.valid(snake,(self.pos[0],self.pos[1]-1))):
                    with self.board.lock:
                        self.pos=list(self.pos)
                        self.pos[1]=self.pos[1]-1


