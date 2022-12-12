from Algorithm import *
import pygame
import time


BLOCKNUMB = 10
BLACK = (0,0,0)
WHITE = (255, 255, 255) 
GRAY = (128, 128, 128) 
YELLOW = (249, 217, 35)
BLUE = (24, 116, 152)
GREEN = (0, 255, 171)
bot = 3
player_1 = 1
player_2 = 2
draw = 0
empty = 0
nothing = -1


class Visualization:
    def __init__(self, Map, condition, numberPlayers, typeAlg):
        self.numberPlayers = numberPlayers
        self.map = Map
        self.size = len(Map)
        self.BLOCKSIZE = 100 
        self.player1Turn = True
        self.winCondition = condition
        self.isEnd = False
        self.typeAlg = typeAlg

        pygame.init()
        self.WidthScreen = self.BLOCKSIZE*self.size
        self.HeightScreen = self.BLOCKSIZE*self.size
        self.screen = pygame.display.set_mode((self.WidthScreen, self.HeightScreen))
        self.screen.fill(GRAY) 
        self.drawX = pygame.image.load("source/X.png").convert_alpha()
        self.drawO = pygame.image.load("source/O.png").convert_alpha()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def fillFullMap(self, minX, maxX, minY, maxY):
        for x in range(minX, maxX, self.BLOCKSIZE):
            for y in range(minY, maxY, self.BLOCKSIZE):
                pygame.draw.rect(self.screen, YELLOW, (x, y, self.BLOCKSIZE-2, self.BLOCKSIZE-2))

    def drawMap(self, minX, maxX, minY, maxY):
        for x in range(minX, maxX, self.BLOCKSIZE):
            for y in range(minY, maxY, self.BLOCKSIZE):
                rect = pygame.Rect(x, y, self.BLOCKSIZE, self.BLOCKSIZE)
                pygame.draw.rect(self.screen, BLACK, rect, 1)

    def cursorSelection(self, mx, my, drawing):
        x = (mx//self.BLOCKSIZE) 
        y = (my//self.BLOCKSIZE)
        if (self.map[x][y] != empty): return False
        self.screen.blit(drawing, (x*self.BLOCKSIZE, y*self.BLOCKSIZE))
        if (self.player1Turn): self.map[x][y] = player_1
        else: self.map[x][y] = player_2
        return True

    def Player1_Move(self, mx, my):
        if (self.cursorSelection(mx, my, self.drawX)):
            self.player1Turn = False
            return TicTacToe.checkWin(self.map, mx//self.BLOCKSIZE, my//self.BLOCKSIZE, self.winCondition)
        return -1
            
    def Player2_Move(self, mx, my):
        if (self.cursorSelection(mx, my, self.drawO)):
            self.player1Turn = True
            return TicTacToe.checkWin(self.map, mx//self.BLOCKSIZE, my//self.BLOCKSIZE, self.winCondition)
        return -1

    def getAlgorithm(self):
        start = time.time()
        print("Calculating for this AI move:", end=" ")
        tempMaze = [[value for value in row] for row in self.map]
        if (self.typeAlg == "MiniMax"):
            bestMove = OriginalMinimax.getMove(self.map, self.winCondition)[1]
        else:
            bestMove = AlphaBetaPruning.getMove(self.map, self.winCondition)[1]
        
        print(f"{time.time()-start}s")
        print(f"Get move at {bestMove}")
        self.map = tempMaze
        return bestMove
    
    def AI_Move(self):
        bestMove = self.getAlgorithm()
        self.map[bestMove[0]][bestMove[1]] = bot
        self.screen.blit(self.drawO, (bestMove[0]*self.BLOCKSIZE, bestMove[1]*self.BLOCKSIZE))
        self.player1Turn = True
        return TicTacToe.checkWin(self.map, bestMove[0], bestMove[1], self.winCondition)

    def End_Screen(self, font, winner):
        self.isEnd = True
        pygame.draw.rect(self.screen, WHITE, (0, self.HeightScreen/2-25, self.WidthScreen, 50), 0, 10)
        if (winner==draw): 
            string = "Draw"
            text = font.render(string, True, BLACK)
            self.screen.blit(text, (self.WidthScreen/2-25, self.HeightScreen/2-20))
        elif winner == player_1:
            string = "Player 1 win"
            text = font.render(string, True, BLACK)
            self.screen.blit(text, (self.WidthScreen/2-60, self.HeightScreen/2-20))
        elif winner == player_2:
            string = "Player 2 win"
            text = font.render(string, True, BLACK)
            self.screen.blit(text, (self.WidthScreen/2-60, self.HeightScreen/2-20)) 
        elif winner == bot:
            string = "Bot win"
            text = font.render(string, True, BLACK)
            self.screen.blit(text, (self.WidthScreen/2-50, self.HeightScreen/2-20)) 


    def Display(self):
        posX1 = 0
        posX2 = self.BLOCKSIZE*self.size
        posY1 = 0
        posY2 = self.BLOCKSIZE*self.size
        font=pygame.font.SysFont('comicsans', 25)
        print(f"Using Algorithm {self.typeAlg}")


        self.drawMap(posX1, posX2, posY1, posY2)
        self.fillFullMap(posX1, posX2, posY1, posY2)
        running = True
        while running:
            if (not self.isEnd and self.player1Turn==False and self.numberPlayers==1):
                result = self.AI_Move()
                if result!=nothing: self.End_Screen(font, result)
                
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    if (mouse_y>self.HeightScreen/2-25 and mouse_y<self.HeightScreen/2+25 and self.isEnd):
                        running = False
                        return "Play again"
                    if self.player1Turn and not self.isEnd:
                        result = self.Player1_Move(mouse_x, mouse_y)
                        if result!=nothing: self.End_Screen(font, result)
                    elif self.numberPlayers==2 and not self.isEnd:
                        result = self.Player2_Move(mouse_x, mouse_y)
                        if result!=-1: self.End_Screen(font, result)
            pygame.display.flip()
        return "End"

    def __del__(self):
        pygame.quit()


class SelectScreen:
    def __init__(self) -> None:
        pass

    def SelectPlayerScreen():
        WidthScreen = 750
        HeightScreen = 600
        pygame.init()
        running = True
        screen = pygame.display.set_mode((WidthScreen, HeightScreen))
        screen.fill(GRAY)
        
        def getString(string):
            font=pygame.font.SysFont('comicsans', 25)
            return font.render(string, True, WHITE)

        pygame.draw.rect(screen, BLACK, (275,200,200,50), 0, 10)
        screen.blit(getString("Player vs Player"), (285, 205))
        pygame.draw.rect(screen, BLACK, (275,300,200,50), 0, 10)
        screen.blit(getString("Player vs Bot"), (300, 305))
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (
                (mouse_x>275 and mouse_x<475 and mouse_y>200 and mouse_y<200+50) or 
                (mouse_x>275 and mouse_x<475 and mouse_y>300 and mouse_y<300+50)):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    return -1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (event.button == 1) and (mouse_x>275 and mouse_x<475 and mouse_y>200 and mouse_y<200+50): 
                        pygame.quit()
                        return 2
                    elif (event.button == 1) and (mouse_x>275 and mouse_x<475 and mouse_y>300 and mouse_y<300+50): 
                        pygame.quit()
                        return 1
            pygame.display.flip()
        pygame.quit()


    def SelectLevelScreen():
        WidthScreen = 750
        HeightScreen = 600
        pygame.init()
        running = True
        screen = pygame.display.set_mode((WidthScreen, HeightScreen))
        screen.fill(GRAY)
        
        def getString(string):
            font=pygame.font.SysFont('comicsans', 25)
            return font.render(string, True, WHITE)

        pygame.draw.rect(screen, BLACK, (275,200,200,50), 0, 10)
        screen.blit(getString("Map 3x3"), (325, 205))
        pygame.draw.rect(screen, BLACK, (275,300,200,50), 0, 10)
        screen.blit(getString("Map 5x5"), (325, 305))

        pygame.draw.rect(screen, BLACK, (275,400,100,50), 0, 10)
        screen.blit(getString("Custom"), (280, 405))
        base_font = pygame.font.Font(None, 52)
        user_text = ""
        user_rect = pygame.Rect(400,400,10,50)
        color_active = pygame.Color('lightskyblue3')
        color_passive = pygame.Color('chartreuse4')
        user_color = color_passive
        user_active = False

        warning = ""

        while running:
            screen.blit(getString(warning), (275, 100))
            if (user_active): user_color=color_active
            else: user_color=color_passive
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (
                (mouse_x>275 and mouse_x<475 and mouse_y>200 and mouse_y<200+50) or 
                (mouse_x>275 and mouse_x<475 and mouse_y>300 and mouse_y<300+50) or
                (mouse_x>275 and mouse_x<475 and mouse_y>400 and mouse_y<400+50)
                ):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    return -1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (event.button == 1) and (mouse_x>275 and mouse_x<475 and mouse_y>200 and mouse_y<200+50): 
                        pygame.quit()
                        return 3
                    elif (event.button == 1) and (mouse_x>275 and mouse_x<475 and mouse_y>300 and mouse_y<300+50): 
                        pygame.quit()
                        return 5
                    if event.button==1 and mouse_x>user_rect.x and mouse_x<user_rect.x+user_rect.width and mouse_y>user_rect.y and mouse_y<user_rect.y+user_rect.height:
                        if (user_active): user_active=False
                        else: user_active = True
                    if event.button==1 and mouse_x>275 and mouse_x<375 and mouse_y>400 and mouse_y<400+50:
                        try:
                            value = int(user_text)
                            return value
                        except:
                            warning = "Value is ambious!"
                if event.type == pygame.KEYDOWN and user_active==True:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
            pygame.draw.rect(screen, user_color, user_rect, 0, 10)
            user_surface = base_font.render(user_text, True, WHITE)
            screen.blit(user_surface, (user_rect.x+5, user_rect.y+5))
            user_rect.w = max(100, user_surface.get_width()+10)
            pygame.display.flip()
        pygame.quit()


    def SelectAlgorithmScreen():
        WidthScreen = 750
        HeightScreen = 600
        pygame.init()
        running = True
        screen = pygame.display.set_mode((WidthScreen, HeightScreen))
        screen.fill(GRAY)
        
        def getString(string):
            font=pygame.font.SysFont('comicsans', 25)
            return font.render(string, True, WHITE)

        pygame.draw.rect(screen, BLACK, (275,200,200,50), 0, 10)
        screen.blit(getString("MiniMax Alg"), (300, 205))
        pygame.draw.rect(screen, BLACK, (265,300,220,50), 0, 10)
        screen.blit(getString("A-B Prunching Alg"), (270, 305))
        # pygame.draw.rect(screen, BLACK, (240,400,300,50), 0, 10)
        # screen.blit(getString("Heuristic Prunching Alg"), (250, 405))

        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (
                (mouse_x>275 and mouse_x<475 and mouse_y>200 and mouse_y<200+50) or 
                (mouse_x>275 and mouse_x<475 and mouse_y>300 and mouse_y<300+50)):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    return -1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (event.button == 1) and (mouse_x>275 and mouse_x<475 and mouse_y>200 and mouse_y<200+50): 
                        pygame.quit()
                        return "MiniMax"
                    elif (event.button == 1) and (mouse_x>265 and mouse_x<475 and mouse_y>300 and mouse_y<300+50): 
                        pygame.quit()
                        return "AlphaBetaPruning"
            pygame.display.flip()
        pygame.quit()