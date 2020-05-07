import sys
from board import *

class Minimax:
	ROW = 10
	COL = 10

	def __init__(self, boar, player):
		self.board = boar
		self.current_player = player

	def move(self):
		return self.max_value(self.board,self.current_player)


	# minimiza a jogada do oponente	
	def min_value(self,board,player):
		if self.terminal_test(board):
			return [self.utility(board), None, None, None]
		
		v = [float("inf"), None, None,None]
	
		moves = self.check_move(board.board,player)
		for move in moves:
			if board.board[move[0]][move[1]] != 0:
				plist,posR,eat = self.show_sugestion(board.board,player,move)
				if len(plist) != 0:
					for new_pos in plist: 
						if board.board[move[0]][move[1]] != 0:
							self.make_move(new_pos,move,board.board)
							r = self.eat(board,posR,new_pos,move,player)
							oldcont = board.cplayer
							other_player = 1 if player == 2 else 2
							m = self.max_value(board,other_player)
							self.make_move(move,new_pos,board.board)
							if len(r[0]) != 0:
								self.back_eat(r[0],r[1],board.board)
							board.cplayer = oldcont
							
							if m[0] < v[0]:
								v[0] = m[0]
								v[1] = move	
								v[2] = new_pos
								v[3] = posR	
						
							return v
			return v	
					

	# maximiza a jogada do PC	
	def max_value(self,board,player):

		if self.terminal_test(board):
			return [self.utility(board), None, None, None]
		
		v = [float("-inf"), None, None, None]

		moves = self.check_move(board.board,player)
		for move in moves:
			if board.board[move[0]][move[1]] != 0:
				plist,posR,eat = self.show_sugestion(board.board,player,move)
				if len(plist) != 0:
					for new_pos in plist: 
						if board.board[move[0]][move[1]] != 0:
							self.make_move(new_pos,move,board.board)
							r = self.eat(board,posR,new_pos,move,player)
							oldcont = board.cpc
							other_player = 1 if player == 2 else 2
							m = self.min_value(board,other_player)
							self.make_move(move,new_pos,board.board)
							if len(r[0]) != 0:
								self.back_eat(r[0],r[1],board.board)
							board.cpc = oldcont
							
							if m[0] > v[0]:
								v[0] = m[0]
								v[1] = move
								v[2] = new_pos
								v[3] = posR	
							return v
			return v	

	# verifica as peças disponiveis para movimento
	def check_move(self,board,current_player):
		moves=[]
		movesEat=[]
		for i in range(self.ROW):
			for j in range(self.COL):
				if board[i][j] == current_player or board[i][j] == current_player*10:
					plist,posR,eat = self.show_sugestion(board,current_player,(i,j))
					if len(plist) != 0:
						if eat == True:
							movesEat.append( [i,j] )
						else:
							moves.append( [i,j] )
		if len(movesEat) != 0:
			return movesEat
		else:
			return moves


	# executa o movimento  
	def make_move(self, move, oldmove, board): 
		board[move[0]][move[1]] = board[oldmove[0]][oldmove[1]]
		board[oldmove[0]][oldmove[1]] = 0
	
	# restaura a captura da peça
	def back_eat(self,move,player,board):
		board[move[0]][move[1]] = player

	# atualiza o tabuleiro se houve captura de peça
	def eat(self,board,posR,pos,oldpos,player):
		r = [[],0]
		if len(posR) != 0:
			#print('player eat', player)
			for m in posR:
				if pos[0] - oldpos[0] > 0:			#inferior
					if pos[1] - oldpos[1] < 0:          #esquerda
						if m[0] - pos[0] < 0:               #atras novo
							if m[1] - oldpos[1] < 0:        #frente old
								r = [m,board.board[m[0]][m[1]]]
								board.board[m[0]][m[1]] = 0
								self.update_game(board,player)
					else:								#direita
						if m[0] - pos[0] < 0:				#atras novo
							if m[1] - oldpos[1] > 0:		#frente old
								r = [m,board.board[m[0]][m[1]]]
								board.board[m[0]][m[1]] = 0
								self.update_game(board,player)
				else:
					if pos[1] - oldpos[1] < 0:          #esquerda
						if m[0] - pos[0] > 0:               #atras novo
							if m[1] - oldpos[1] < 0:        #frente old
								r = [m,board.board[m[0]][m[1]]]
								board.board[m[0]][m[1]] = 0
								self.update_game(board,player)
					else:                               #direita
						if m[0] - pos[0] > 0:               #atras novo
							if m[1] - oldpos[1] > 0:        #frente old
								r = [m,board.board[m[0]][m[1]]]
								board.board[m[0]][m[1]] = 0
								self.update_game(board,player)
		return r


	# atualiza o estado do jogo  		
	def update_game(self, board,player):
		if player == 1:
			board.cplayer+=1
		else:
			board.cpc+=1

	# mostra sugestoes de espaços disponeis para mover a peça
	def show_sugestion(self,board,current_player,pos):

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

	    if board[pos[0],pos[1]] == 1:
	        dist = -2
	    elif board[pos[0],pos[1]] == 2:
	        dist = 2
	    elif board[pos[0],pos[1]] == 20:
	        dist = 20
	    elif board[pos[0],pos[1]] == 10:
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
	                    if board[x][y] != current_player and board[x][y] != current_player*10:	
	                        if board[x][y] == 0:
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
	                    if board[x2][y2] != current_player and board[x2][y2] != current_player*10:	
	                        if board[x2][y2] == 0:
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
	
    # Retorna um valor para computador 1 para vencer e -1 para perder   
	def utility(self,board):
		if board.has_won() == 1:
			return -1
		elif board.has_won() == 2:
			return 1
    
	# Retorna verdadeiro caso tenha terminado o jogo 
	def terminal_test(self,board):
		return board.has_won()
