import pygame
from pygame.locals import *
import numpy as np


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)

class Board_teste():
    PLAYING = 0
    PLAYER1_WON = 1
    PLAYER2_WON = 2

    ROW = 10
    COL = 10
    player = 0
    cplayer = 0
    cpc = 0

    # cria o tabuleiro
    def Board(self, screen,player,c1,c2):
        self.screen = screen
        self.player = player
        self.cplayer = c1
        self.cpc = c2
        self.board = np.zeros( (self.ROW, self.COL) )
        self.initBoard()

    # inicializa as posições das peças
    def initBoard(self):
        for row in range(self.ROW):
            for col in range(self.COL):
                if row == 0 or row == 2:
                    if col%2!=0:
                        self.board[row][col] = 2
                if row == 1 or row == 3:
                    if col%2==0:
                        self.board[row][col] = 2
                if row == 6 or row == 8:
                    if col%2!=0:
                        self.board[row][col] = 1
                if row == 7 or row == 9:
                    if col%2==0:
                        self.board[row][col] = 1


	# verifica as peças disponiveis para movimento
    def check_move(self,current_player):
        self.player = current_player

        moves=[]
        movesEat=[]
        for i in range(self.ROW):
            for j in range(self.COL):
                if self.board[i][j] == current_player or self.board[i][j] == current_player*10:
                    plist,posR,eat = self.show_sugestion(current_player,(i,j))
                    if len(plist) != 0:
                        if eat == True:
                            movesEat.append( [i,j] )
                        else:
                            moves.append( [i,j] )
        if len(movesEat) != 0:
            return movesEat
        else:
            return moves

    # verifica se a peça foi clicada
    def check_player(self,current_player,x,y,oldpos,checked,plist,posR):

        self.player = current_player

        if y < 10 and x < 10:
            pos = [x,y] 
            if not checked:
                if self.board[x][y] == current_player or self.board[x][y] == current_player*10:
                    self.drawCell(pos,checked)
                    plist,posR,et = self.show_sugestion(current_player,pos)
                    for z in plist:
                        self.drawCell( z,checked )
                    return True,pos,current_player,plist,posR
                else:
                    return False,pos,current_player,plist,posR
            else:
                if pos in plist:
    
                    eat = False
                    move = False
                    if len(posR) != 0:
                        for m in posR:
                         
                            if pos[0] - oldpos[0] > 0:          #inferior
                                if pos[1] - oldpos[1] < 0:          #esquerda
                                    if m[0] - pos[0] < 0:               #atras novo
                                        if m[1] - oldpos[1] < 0:        #frente old
                                            self.board[m[0]][m[1]] = 0
                                            self.drawCell(m,True)
                                            eat = True
                                            self.update_game(current_player)
                                else:                               #direita
                                    if m[0] - pos[0] < 0:               #atras novo
                                        if m[1] - oldpos[1] > 0:        #frente old
                                            self.board[m[0]][m[1]] = 0
                                            self.drawCell(m,True)
                                            eat = True
                                            self.update_game(current_player)
                            else:  
                                if pos[1] - oldpos[1] < 0:          #esquerda
                                    if m[0] - pos[0] > 0:               #atras novo
                                        if m[1] - oldpos[1] < 0:        #frente old
                                            self.board[m[0]][m[1]] = 0
                                            self.drawCell(m,True)
                                            eat = True
                                            self.update_game(current_player)
                                else:                               #direita
                                    if m[0] - pos[0] > 0:               #atras novo
                                        if m[1] - oldpos[1] > 0:        #frente old
                                            self.board[m[0]][m[1]] = 0
                                            self.drawCell(m,True)
                                            eat = True
                                            self.update_game(current_player)
                        if eat:
                            move = True
                    else:           
                        move = True
                        
                    if move:
                        for clean in plist:
                            self.drawCell(clean,True)

                        self.board[pos[0]][pos[1]] = self.board[oldpos[0]][oldpos[1]]
                        self.board[oldpos[0]][oldpos[1]] = 0
                        self.drawCell(pos,True)
                        self.drawCell(oldpos,True)

                        if pos[0] == 0 or pos[0] == 9:
                            self.board[pos[0]][pos[1]] = current_player*10
                            self.drawCell(pos,True)
                        
                        current_player = 2 if(current_player == 1) else 1
                        self.show_status(current_player,self.cplayer,self.cpc)
                        return False,pos,current_player,[],[]
                    else:
                        return True,oldpos,current_player,[],[]

                elif oldpos[0] == pos[0] and oldpos[1] == pos[1]:
                    self.drawCell(pos,checked)
                    for clean in plist:
                        self.drawCell(clean,checked)
                    return False,pos,current_player,[],[]
            
                else:
                    return True,oldpos,current_player,[],[]
    
    # atualiza o estado do jogo  		
    def update_game(self, player):
        if self.player == 1:
            self.cplayer+=1
        else:
            self.cpc+=1

    # verifica e retorna o vencedor da partida
    def has_won(self):
        if self.cplayer == 20:
            return self.PLAYER1_WON
        elif self.cpc == 20:
            return self.PLAYER2_WON
        else:
            return self.PLAYING
            
	# mostra sugestoes de espaços disponeis para mover a peça 
    def show_sugestion(self,current_player,pos):
  
        cimax = pos[0]
        baixox = self.ROW - pos[0] -1
        direitay = self.ROW - pos[1] -1
        esquerday = pos[1]

        if pos[0] - pos[1] > 0:
            x=cimax-esquerday
            y=0
        else:
            x=0
            y=abs(cimax-esquerday)
        if pos[0] + pos[1] < 10:
            x2=0
            y2=abs(cimax+esquerday)
        else:
            x2=abs(baixox-esquerday)
            y2=self.ROW-1

        if self.board[pos[0],pos[1]] == 1:
            dist = -2
        elif self.board[pos[0],pos[1]] == 2:
            dist = 2
        elif self.board[pos[0],pos[1]] == 20:
            dist = 20
        elif self.board[pos[0],pos[1]] == 10:
            dist = 10

        plist = []
        plist2 = []

        pos0 = []
        pos0x = []
        cont = 0
        contx = 0
        cont2 = 0
        cont2x = 0
        pass_current = 0
        pass_current_x2 = 0
        posR = []
        posRx = []

        for ax in range(self.ROW):
            for ay in range(self.ROW):
                if ax == x and ay == y:
                    a = x - pos[0]

                    if abs(a) <= abs(dist):
                        if self.board[x][y] != current_player and self.board[x][y] != current_player*10:

                            if self.board[x][y] == 0:
 
                                if abs(dist) == 2:

                                    if dist == -2:
                                        if a < 0:
                                            if len(plist) != 0:
                                                plist = [] 
                                                plist.append( [x,y] )
                                            else:
                                                plist.append( [x,y] )
                                    else:     
                                        if a > 0:
                                            if len(plist) == 0:
                                                if len(posR) != 0:
                                                    plist.append( [x,y] )
                                                elif a == 1:
                                                    plist.append( [x,y] )

                                else:
                                    if a < 0: 
                                        plist.append( [x,y] )
                                    else:
                                        if cont < 2:
                                            if pass_current == 0:
                                                plist.append( [x,y] )
                                cont=0

                            else:
                                cont+=1
                                if abs(dist) == 2: 
                                    if dist == -2:
                                        if a == -1 :
                                            posR.append( [x,y] )
                                    else:
                                        if a == 1:
                                            posR.append( [x,y] )
                                else:
                                    if cont % 2 == 0 and a < 0:
                                        posR = []
                                        plist = []
                                        cont2 = 0
                                        cont = 0
                                    elif cont % 2 != 0 and a < 0:
                                        if len(plist) != 0:
                                            if cont2 == 1:
                                                pl = []
                                                for l in plist:
                                                    lr = posR[0]
                                                    if l[0] - (lr[0]) > 0:
                                                        pl.append(l)
                                                plist=pl        

                                                posR=[]
                                                posR.append( [x,y] )
                                                cont=1
                                            else:
                                                posR.append( [x,y] )
                                                cont2 += 1
                                    elif cont % 2 != 0 and a > 0:
                                        if pass_current == 0 and cont2 == 0:
                                            posR.append( [x,y] )
                                            cont2 += 1
                                        else:
                                            pass_current = 1
                                    elif cont % 2 == 0 and a > 0:
                                        if cont2 == 1:
                                            pass_current = 1
                                            cont=0
                        else:
                            if a > 0:
                                pass_current = 1
                            if a < 0:
                                plist = []
                                posR=[]
                            if a == 0:
                                cont = 0
                                cont2 = 0
                    x+=1
                    y+=1
                if ax == x2 and ay == y2:

                    a = x2 - pos[0]

                    if abs(a) <= abs(dist):
                        if self.board[x2][y2] != current_player and self.board[x2][y2] != current_player*10:

                            if self.board[x2][y2] == 0:
 
                                if abs(dist) == 2:

                                    if dist == -2:
                                        if a < 0:
                                            if len(plist2) != 0:
                                                plist2 = [] 
                                                plist2.append( [x2,y2] )
                                            else:
                                                plist2.append( [x2,y2] )
                                    else:     
                                        if a > 0:
                                            if len(plist2) == 0:
                                                if len(posRx) != 0:
                                                    plist2.append( [x2,y2] )
                                                elif a == 1:
                                                    plist2.append( [x2,y2] )
                                else:
                                    if a < 0: 
                                        plist2.append( [x2,y2] )
                                    else:
                                        if contx < 2:
                                            if pass_current_x2 == 0:
                                                plist2.append( [x2,y2] )
                                contx=0
                            else:
                                contx+=1
                                if abs(dist) == 2: 
                                    if dist == -2:
                                        if a == -1 :
                                            posRx.append( [x2,y2] )
                                    else:
                                        if a == 1:
                                            posRx.append( [x2,y2] )
                                else:
                                    if contx % 2 == 0 and a < 0:
                                        posRx = []
                                        plist2 = []
                                        cont2x = 0
                                        contx = 0
                                    elif contx % 2 != 0 and a < 0:
                                        if len(plist2) != 0:
                                            if cont2x == 1:
                                                pl = []
                                                for l in plist2:
                                                    lr = posRx[0]
                                                    if l[0] - (lr[0]) > 0:
                                                        pl.append(l)
                                                plist2=pl    
                                                posRx=[]
                                                posRx.append( [x2,y2] )
                                                contx=1
                                            else:
                                                posRx.append( [x2,y2] )
                                                cont2x += 1
                                    elif contx % 2 != 0 and a > 0:
                                        if pass_current_x2 == 0 and cont2x == 0:
                                            posRx.append( [x2,y2] )
                                            cont2x += 1
                                        else:
                                            pass_current_x2 = 1
                                    elif contx % 2 == 0 and a > 0:
                                        if cont2x == 1:
                                            pass_current_x2 = 1
                                            contx=0
                        else:
                            if a > 0:
                                pass_current_x2 = 1
                            if a < 0:
                                plist2 = []
                                posRx = [] 
                    x2+=1
                    y2-=1

        eat = False
        if len(posR) != 0:
            plist,posR,eat = self.check_eat(plist,posR, pos, current_player,False)
            plist2,posRx,eat = self.check_eat(plist2,posRx, pos, current_player,eat)
        elif len(posRx) != 0:
            plist2,posRx,eat = self.check_eat(plist2,posRx, pos, current_player,False)
            plist,posR,eat = self.check_eat(plist,posR, pos, current_player,eat)

        posR+=posRx

        plist+=plist2
        return plist,posR,eat

    
	# funcao que verifica se houve captura de peça    
    def check_eat(self, plist, posR, oldpos,current_player,eat):
        r = []
        p = []
        for pos in plist:
            if len(posR) != 0:
                for m in posR:
                
                    if pos[0] - oldpos[0] > 0:          #inferior
                        if pos[1] - oldpos[1] < 0:          #esquerda
                            if m[0] - pos[0] < 0:               #atras novo
                                if m[1] - oldpos[1] < 0:        #frente old
                                    eat = True
                                    p.append(pos)
                        else:                               #direita
                            if m[0] - pos[0] < 0:               #atras novo
                                if m[1] - oldpos[1] > 0:        #frente old
                                    eat = True
                                    p.append(pos)
                    else:  
                        if pos[1] - oldpos[1] < 0:          #esquerda
                            if m[0] - pos[0] > 0:               #atras novo
                                if m[1] - oldpos[1] < 0:        #frente old
                                    eat = True
                                    p.append(pos)
                        else:                               #direita
                            if m[0] - pos[0] > 0:               #atras novo
                                if m[1] - oldpos[1] > 0:        #frente old
                                    eat = True
                                    p.append(pos)
                if eat == True:
                    if len(r)==0:
                        r.append(m)
                        if m not in r:
                            r.append(m)
            else:
                if eat == False:
                    p.append(pos)                  
        return p,r,eat

    # atualiza o desenho da peça
    def drawCell(self,pos,checked):
        blockSize = 50
        rect = pygame.Rect(pos[1]*blockSize+1, pos[0]*blockSize+1,
        blockSize, blockSize)
        if not checked:
            pygame.draw.rect(self.screen, GREEN, rect, 0)
        else:
            pygame.draw.rect(self.screen, BLACK, rect, 0)

        if self.board[pos[0]][pos[1]] == 2:
            pygame.draw.circle(self.screen, RED, ((pos[1]*blockSize)+25,(pos[0]*blockSize)+25), 20)
        if self.board[pos[0]][pos[1]] == 1:
            pygame.draw.circle(self.screen, BLUE, ((pos[1]*blockSize)+25,(pos[0]*blockSize)+25), 20)
        if self.board[pos[0]][pos[1]] == 10:
            pygame.draw.circle(self.screen, BLUE, ((pos[1]*blockSize)+25,(pos[0]*blockSize)+25), 20)
            pygame.draw.circle(self.screen, BLACK, ((pos[1]*blockSize)+25,(pos[0]*blockSize)+25), 5)
        if self.board[pos[0]][pos[1]] == 20:
            pygame.draw.circle(self.screen, RED, ((pos[1]*blockSize)+25,(pos[0]*blockSize)+25), 20)
            pygame.draw.circle(self.screen, BLACK, ((pos[1]*blockSize)+25,(pos[0]*blockSize)+25), 5)

    # desenha o tabuleiro
    def drawGrid(self):
        blockSize = 50
        r = pygame.Rect(0, 0,502, 502)
        pygame.draw.rect(self.screen, GREEN, r,2)
        for x in range(self.ROW):
            for y in range(self.COL):
                rect = pygame.Rect(x*blockSize+1, y*blockSize+1,
                                blockSize, blockSize)
                if y % 2 == 0:
                    if x % 2 != 0:       
                        pygame.draw.rect(self.screen, BLACK, rect, 0)
                    else:
                        pygame.draw.rect(self.screen, WHITE, rect, 0)
                else:
                    if x % 2 == 0:       
                        pygame.draw.rect(self.screen, BLACK, rect, 0)
                    else:
                        pygame.draw.rect(self.screen, WHITE, rect, 0)
                if self.board[y][x] == 2:
                    pygame.draw.circle(self.screen, RED, ((x*blockSize)+25,(y*blockSize)+25), 20)
                if self.board[y][x] == 1:
                    pygame.draw.circle(self.screen, BLUE, ((x*blockSize)+25,(y*blockSize)+25), 20)
                self.show_status(self.player,self.cplayer,self.cpc)

    # mostra o status do jogo
    def show_status(self,player,cplayer,cpc): 

        self.screen.fill(WHITE, (502, 0, 700, 500))
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = self.text_objects("Jogador 2", smallText,-1)
        textRect.center = ( (600), (100) )
        self.screen.blit(textSurf, textRect)
        textSurf, textRect = self.text_objects("Pontuação: "+str(cpc), smallText,-1)
        textRect.center = ( (600), (150) )
        self.screen.blit(textSurf, textRect)
        textSurf, textRect = self.text_objects("Vez do jogador "+str(player), smallText,player)
        textRect.center = ( (600), (250) )
        self.screen.blit(textSurf, textRect)  
        textSurf, textRect = self.text_objects("Jogador 1", smallText,-1)
        textRect.center = ( (600), (400) )
        self.screen.blit(textSurf, textRect) 
        textSurf, textRect = self.text_objects("Pontuação: "+str(cplayer), smallText,-1)
        textRect.center = ( (600), (450) )
        self.screen.blit(textSurf, textRect)
    
    # printa texto
    def text_objects(self,text, font,player):
        color = BLACK
        if player == 1:
            color = BLUE
        elif player == 2:
            color = RED
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()