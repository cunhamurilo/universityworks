import pygame
from pygame.locals import *
import numpy as np
from board import *
from minimax import *

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)

pygame.init()
screen = pygame.display.set_mode((700,502))
pygame.display.set_caption('Jogo de Damas')

class Jogo():
    PLAYING = 0
    PLAYER1_WON = 1
    PLAYER2_WON = 2
    pc = 0
       
    # inicia o jogo
    def play_game(self,current_player):
        self.board = Board_teste()
        self.board.Board(screen,current_player,0,0)
        self.board.drawGrid()

        self.pc = 2 if current_player == 1 else 1
        self.computer = Minimax(self.board,self.pc)

        checked = False
        plist = []
        posR = []
        moves = []
        self.game_state = self.PLAYING
        self.pc = 2 if current_player == 1 else 1

        while self.game_state == self.PLAYING:
            if self.pc != current_player:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()

                    click = pygame.mouse.get_pressed()
                    if click[0] == 1:
                        print('Jogador real: ')
                        moves = self.board.check_move(current_player)
                        pos = pygame.mouse.get_pos()
                        x = pos[1]//50
                        y = pos[0]//50
                        gt = [x,y]
                        if x < 10 and y < 10:
                            if not checked:
                                if gt in moves:
                                    checked,oldpos,current_player,plist,posR = self.board.check_player(current_player,x,y,(x,y),checked,plist,posR)
                            else:  
                                checked,oldpos,current_player,plist,posR = self.board.check_player(current_player,x,y,oldpos,checked,plist,posR)
                            
            elif self.pc == current_player:
                print('Jogador O(PC): ',current_player)
                move = self.computer.move()
                o = move[1]
                p = move[2]
                r = move[3]

                checked,oldpos,current_player,plist,posR = self.board.check_player(current_player,p[0],p[1],o,True,[p],r)
                current_player = 1
                checked = False

            self.game_state = self.board.has_won()
            if self.game_state != self.PLAYING:
                self.show_winner()

            pygame.display.update()
		
    # mostra vencedor
    def show_winner(self):

        print('aquuiii show')
        while True:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            screen.fill(WHITE)
            largeText = pygame.font.Font('freesansbold.ttf',40)
            TextSurf, TextRect = self.text_objects("Vencedor", largeText)
            TextRect.center = ((700/2),(200))
            screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = self.text_objects('Jogador '+str(self.game_state), largeText)
            TextRect.center = ((700/2),(250))
            screen.blit(TextSurf, TextRect)


            pygame.display.update()

    # printa texto
    def text_objects(self,text, font):
        textSurface = font.render(text, True, BLACK)
        return textSurface, textSurface.get_rect()

    # introdução do jogo
    def game_intro(self):
        intro = True

        while intro:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            
            screen.fill(WHITE)
            largeText = pygame.font.Font('freesansbold.ttf',90)
            TextSurf, TextRect = self.text_objects("Jogo de Damas", largeText)
            TextRect.center = ((700/2),(500/2))
            screen.blit(TextSurf, TextRect)

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            
            x = 350
            y = 200

            if y+100 > mouse[0] > y and x+50 > mouse[1] > x:
                pygame.draw.rect(screen, GREEN,(y,x,100,50))
                if click[0] == 1:
                    print('jogador 1')
                    screen.fill(WHITE)
                    intro =False
                    self.play_game(1)
                    
            else:
                pygame.draw.rect(screen, BLUE,(y,x,100,50))

            smallText = pygame.font.Font("freesansbold.ttf",20)
            textSurf, textRect = self.text_objects("Jogador 1", smallText)
            textRect.center = ( (y+(100/2)), (x+(50/2)) )
            screen.blit(textSurf, textRect) 
                
            if y*2+100 > mouse[0] > y*2 and x+50 > mouse[1] > x:
                pygame.draw.rect(screen, GREEN,(y*2,x,100,50))
                if click[0] == 1:
                    print('jogador 2')
                    screen.fill(WHITE)
                    self.play_game(2)
            else:
                pygame.draw.rect(screen, RED,(y*2,x,100,50))

            textSurf, textRect = self.text_objects("Jogador 2", smallText)
            textRect.center = ( (y*2+(100/2)), (x+(50/2)) )
            screen.blit(textSurf, textRect) 

            pygame.display.flip()

j = Jogo()
j.game_intro()