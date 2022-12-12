from TicTacToe import *

bot = 3
player = 1
empty = 0
priority = 2
draw = 0
limitDepth = 4
limitMap = 5

#Static class and Static method !
class OriginalMinimax:
    def __init__(self) -> None:
        pass

    def SearchingBranch(matrix, depth, isMax, winCondition, user):
        size = len(matrix)
        if (isMax): bestValue = 2
        else: bestValue = -2
        bestMove = tuple()
        for i in range(size):
            for j in range(size):
                if (matrix[i][j] == empty):
                    matrix[i][j] = user
                    value = OriginalMinimax.MinMaxCalculation(matrix, i, j, depth+1, isMax, winCondition)
                    matrix[i][j] = empty
                    if (not isMax and value > bestValue):
                        bestValue = value
                        bestMove = (i, j)
                    elif (isMax and value < bestValue):
                        bestValue = value
                        bestMove = (i, j)
        return bestValue, bestMove

    def getMove(map, winCondition):
        return OriginalMinimax.SearchingBranch(map, 0, False, winCondition, bot)

    def MinMaxCalculation(matrix, botMoveX, botMoveY, depth, isMax, winCondition):
        resultCheck = TicTacToe.checkWin(matrix, botMoveX, botMoveY, winCondition)
        if resultCheck == bot: return 1
        elif resultCheck == player: return -1
        elif resultCheck == draw: return 0

        if (isMax):
            return OriginalMinimax.SearchingBranch(matrix, depth+1, False, winCondition, bot)[0]
        else:
            return OriginalMinimax.SearchingBranch(matrix, depth+1, True, winCondition, player)[0]



class AlphaBetaPruning:
    def __init__(self) -> None:
        pass

    def getMove(map, winCondition):
        global limitMap
        result = AlphaBetaPruning.getMax(map, -200, 200, 0, winCondition)
        #Apply Heuristic if search depth reaches limit
        if (len(map)>=limitMap and result[1]==(-1,-1)):
            print("(This Move by Heuristic)", end=": ")
            return HeuristicEvalution(map, player, bot, winCondition).getMove()
        return result
        
    def getMax(map, AlphaValue, BetaValue, depth, winCondition):
        bestValue = -200
        bestMove = (-1, -1)

        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j]==empty: continue
                result = TicTacToe.checkWin(map, i, j, winCondition)
                if result == player:
                    return (-1, bestMove)
                elif result == bot:
                    return (1, bestMove)
                elif result == draw:
                    return (0, bestMove)

        global limitDepth, limitMap
        if (len(map)>=limitMap and depth>=limitDepth):
            return (-200, bestMove)

        for i in range(len(map)):
            for j in range(len(map)):
                if map[i][j] == empty:
                    map[i][j] = bot
                    (minValue, minMove) = AlphaBetaPruning.getMin(map, AlphaValue, BetaValue, depth+1, winCondition)
                    if minValue > bestValue:
                        bestValue = minValue
                        bestMove = (i, j)
                    map[i][j] = empty
                    
                    if bestValue >= BetaValue:
                        return (bestValue, bestMove)

                    if bestValue > AlphaValue:
                        AlphaValue = bestValue
        return (bestValue, bestMove)


    def getMin(map, AlphaValue, BetaValue, depth, winCondition):
        BestValue = 200
        bestMove = (-1, -1)

        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j]==empty: continue
                result = TicTacToe.checkWin(map, i, j, winCondition)
                if result == player:
                    return (-1, bestMove)
                elif result == bot:
                    return (1, bestMove)
                elif result == draw:
                    return (0, bestMove)

        global limitDepth, limitMap
        if (len(map)>=limitMap and depth>=limitDepth):
            return (200, bestMove)

        for i in range(len(map)):
            for j in range(len(map)):
                if map[i][j] == empty:
                    map[i][j] = player
                    (maxValue, maxMove) = AlphaBetaPruning.getMax(map, AlphaValue, BetaValue, depth+1, winCondition)
                    if maxValue < BestValue:
                        BestValue = maxValue
                        bestMove = (i, j)
                    map[i][j] = empty

                    if BestValue <= AlphaValue:
                        return (BestValue, bestMove)

                    if BestValue < BetaValue:
                        BetaValue = BestValue

        return (BestValue, bestMove)


class HeuristicEvalution:
    def __init__(self, map, yoursMove, rivalMove, winCondition) -> None:
        self.defaultMap = map
        self.size = len(map)
        #convert all value of player and bot to negative to distinguish with other values
        self.yours = -yoursMove
        self.rivals = -rivalMove
        self.winCondition = winCondition
        self.HeuristicMap = self.CovnertHeuristicMap()
        self.SetupDefaultPoint()
    
    def CovnertHeuristicMap(self):
        R = [[-value for value in row] for row in self.defaultMap]
        return R

    def SetupDefaultPoint(self):
        #set up for the first step, in which the original map should be
        #cause this is original, this do not need the AI Manual Treatment
        #imagine that BOT is filled all the map, after that find out the best Original Heuristic
        for i in range(self.size):
            for j in range(self.size):
                tempVal = self.HeuristicMap[i][j]
                if tempVal<0: continue  
                self.HeuristicMap[i][j]=bot
                self.RehearseStraight(i, j, bot, "vertical", False)
                self.RehearseStraight(j, i, bot, "horizonal", False)
                self.RehearseDiagonal(i, j, bot, "left", False)
                self.RehearseDiagonal(i, j, bot, "right", False)
                self.HeuristicMap[i][j]=tempVal+1
    
    def Manual_AI_Treatment_Straight(self, start, end, enemyFront, enemyBack):
        if (enemyFront!=-1 and enemyBack!=self.size):
            if abs(enemyFront-enemyBack)+1<self.winCondition:
                return -2, -2
        if (enemyFront!=-1): start=enemyFront
        if (enemyBack!=self.size): end=enemyBack
        return start, end

    def DefineStartEnd_StraightLine(self, vectorChange):
        start = vectorChange-self.winCondition-1
        #horizon would be from (x-n, y) to (x+n, y) with n steps
        #vertical would be from (x, y-n) to (x, y+n) with n steps
        if (start<0): start = 0
        end = vectorChange + self.winCondition+1
        if (end > self.size): end = self.size
        return start, end

    def RehearseStraight(self, vectorChange, vectorStay, target, direction, isManualTreatment):
        #this would run from start to end of each straight line
        start, end = self.DefineStartEnd_StraightLine(vectorChange)

        point, countAllies = 0, 0
        enemyFront, enemyBack = -1, self.size
        #if target is player, value must be higher little bit than bot
        # => make sure bot would priority block player
        if (-target==player): point = priority
        #first move that check how many "friends" or "enemy" on the road
        for i in range(start, end):
            if (direction=="vertical"): x, y = i, vectorStay
            else: x, y = vectorStay, i
            #if there is a friend, point woud plus 1
            if (self.HeuristicMap[x][y]==target):
                point+=1
                countAllies+=1
            elif (self.HeuristicMap[x][y]<0):
                if (i<vectorChange and i>enemyFront):
                    enemyFront = i
                if (i>vectorChange and i<enemyBack):
                    enemyBack = i
        
        #Manual AI Treatment, in case there are 2 enemies at front and back and the space between is smaller than winCondition -> skip it
        #else, cut the road shorter than original road
        if (isManualTreatment):
            start, end = self.Manual_AI_Treatment_Straight(start, end, enemyFront, enemyBack)
            if ((start, end)==(-2, -2)): return

        #if target nearly be win, the point would increase that encourage it to move this line
        if (isManualTreatment):
            if countAllies==self.winCondition-2 and target==-player: point+2
            elif countAllies==self.winCondition-1 and target==-player: point+1
        else:
            point = 1
        #set point to the road
        for i in range(start, end):
            if (direction=="vertical"): x, y = i, vectorStay
            else: x, y = vectorStay, i
            if self.HeuristicMap[x][y]>=0:
                self.HeuristicMap[x][y]+=point

    def DefineStartEnd_Diagonal(self, vectorX, vectorY, direction):
        startX, startY, endX, endY = vectorX, vectorY, vectorX, vectorY
        #left diagnol would be from (x-n, y-n) to (x+n, y+n) with n steps
        if (direction=="left"):
            stepX, stepY = 1, 1
        #right diagnol would be from (x+n, y-n) to (x-n, y+n) with n steps
        else:
            stepX, stepY = 1, -1
        #from (x, y) go back m step with step = winCondition -> have the start point
        for _ in range(self.winCondition-1):
            if ((direction=="left" and (startX==0 or startY==0)) or 
                (direction=="right" and (startX==0 or startY==self.size-1))): 
                    break
            else: 
                startX, startY = startX-stepX, startY-stepY
        #from (x, y) go forward m step with step = winCondition -> have the end point
        for _ in range(self.winCondition-1):
            if ((direction=="left" and (endX==self.size-1 or endY==self.size-1)) or
                (direction=="right" and (endX==self.size-1 or endY==0))): 
                    break
            else: 
                endX, endY = endX+stepX, endY+stepY
        return startX, startY, endX, endY

    def Manual_AI_Treatment_Diagonal(self, startX, startY, endX, endY, enemyFront, enemyBack, direction):   
        if  ((enemyFront!=(-1,-1) and enemyBack!=(self.size, self.size) and direction=="left") or 
            (enemyFront!=(-1, self.size) and enemyBack!=(self.size, -1) and direction=="right")):
            if (abs(enemyFront[0]-enemyBack[0]<self.winCondition)):
                return -2, -2, -2, -2
        if (direction=="left" and enemyFront!=(-1, -1)): startX, startY = enemyFront[0], enemyFront[1]
        if (direction=="left" and enemyBack!=(self.size, self.size)): endX, endY = enemyBack[0], enemyBack[1]
        if (direction=="right" and enemyFront!=(-1, self.size)): startX, startY = enemyFront[0], enemyFront[1]
        if (direction=="right" and enemyBack!=(self.size, -1)): endX, endY = enemyBack[0], enemyBack[1]
        return startX, startY, endX, endY

    def RehearseDiagonal(self, vectorX, vectorY, target, direction, isManualTreatment):
        #this would run from start to end of each diagonal
        startX, startY, endX, endY = self.DefineStartEnd_Diagonal(vectorX, vectorY, direction)

        #from start to end
        #check how many "friends" or "enemy" on the road
        i, j, point, count = startX, startY, 0, 0
        if (direction=="left"):
            enemyFront, enemyBack = (-1, -1), (self.size, self.size)
        else:
            enemyFront, enemyBack = (-1, self.size), (self.size, -1)
        #if target is player, value must be higher little bit than bot
        # => make sure bot would priority block player
        if (-target==player): point = priority
        while True:
            if (direction=="left"):
                if (i>endX and j>endY): break
                else: 
                    x, y= i, j
                    i, j = i+1, j+1
            else:
                if (i>endX and j<endY): break
                else:
                    x, y = i, j
                    i, j = i+1, j-1
            
            #if there is a friend, point woud plus 1
            if (self.HeuristicMap[x][y]==target):
                point+=1
                count+=1
            elif (self.HeuristicMap[x][y]<0):
                if (x<vectorX and x>enemyFront[0]):
                    enemyFront = (x, y)
                elif (x>vectorX and x<enemyBack[0]):
                    enemyBack = (x, y)


        #Manual AI Treatment, in case there are 2 enemies at front and back and the space between is smaller than winCondition -> skip it
        #else, cut the road shorter than original road
        if (isManualTreatment):
            startX, startY, endX, endY = self.Manual_AI_Treatment_Diagonal(startX, startY, endX, endY, enemyFront, enemyBack, direction)
            if ((startX, startY, endX, endY)==(-2, -2, -2, -2)): return

        #if target nearly be win, the point would increase that encourage it to move this line
        if (isManualTreatment):
            if count==self.winCondition-2 and target==-player: point+2
            elif count==self.winCondition-1 and target==-player: point+1
        else:
            point = 1
        #set point to the road
        i, j = startX, startY
        while True:
            if (direction=="left"):
                if (i>endX and j>endY): break
                else: 
                    x, y= i, j
                    i, j = i+1, j+1
            else:
                if (i>endX and j<endY): break
                else:
                    x, y = i, j
                    i, j = i+1, j-1
            if self.HeuristicMap[x][y]>=0:
                self.HeuristicMap[x][y]+=point
        
    def CalculateHeuristicValue(self):
        for i in range(self.size):
            for j in range(self.size):
                if (self.HeuristicMap[i][j]>=0): continue
                else:
                    target = self.HeuristicMap[i][j]
                    self.RehearseStraight(i, j, target, "vertical", True)
                    self.RehearseStraight(j, i, target, "horizonal", True)
                    self.RehearseDiagonal(i, j, target, "left", True)
                    self.RehearseDiagonal(i, j, target, "right", True)
    
    def ManhattanDistance(self, start, end):
        return abs(start[0]-end[0])+abs(start[1]-end[1])

    def FindMax(self):
        bestMove = tuple()
        bestValue = -200
        for i in range(self.size):
            for j in range(self.size):
                value = self.HeuristicMap[i][j]
                if (value<0): continue
                elif (value>bestValue):
                    bestValue = value
                    bestMove = (i, j)
        return (bestValue, bestMove)

    def getMove(self):
        self.CalculateHeuristicValue()
        return self.FindMax()
  