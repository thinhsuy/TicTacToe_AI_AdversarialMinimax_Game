#Static class and Static method !
class TicTacToe:
    def __init__(self) -> None:
        pass

    def checkDraw(map):
        for row in map:
            for value in row:
                if (value==0): return False
        return True
    
    def checkDiagonal(map, vectorX, vectorY, target, direction, winCondition):
        size = len(map)
        startX, startY, endX, endY = vectorX, vectorY, vectorX, vectorY
        if (direction=="left"):
            stepX, stepY = 1, 1
        else:
            stepX, stepY = 1, -1
        #start and end would be the whole line to check value is respective
        #different directions of diagonal lead to different way to calculate
        for _ in range(winCondition-1):
            if ((direction=="left" and (startX==0 or startY==0)) or 
                (direction=="right" and (startX==0 or startY==size-1))): 
                    break
            else: 
                startX, startY = startX-stepX, startY-stepY
        for _ in range(winCondition-1):
            if ((direction=="left" and (endX==size-1 or endY==size-1)) or
                (direction=="right" and (endX==size-1 or endY==0))): 
                    break
            else: 
                endX, endY = endX+stepX, endY+stepY
    
        #check the first element because next would check the current with the previous one is same or not
        x, y = startX, startY
        if ((map[x][y]==target)): 
            respectively = 1
        else: 
            respectively = 0

        #from the second element and go on to check
        if (direction=="left"):
            i, j = startX+1, startY+1
        else:
            i, j = startX+1, startY-1
        #the loop now if take the distinct way to make formula
        while True:
            #the left diagonal would increase x+1 and y+1 gradually
            if (direction=="left"):
                if (i>endX and j>endY): break
                else: 
                    x, y, preX, preY = i, j, i-1, j-1
                    i, j = i+1, j+1
            #the right one would increase x+1 and decrease y-1 gradually
            else:
                if (i>endX and j<endY): break
                else:
                    x, y, preX, preY = i, j, i-1, j+1
                    i, j = i+1, j-1
            
            checkValue = map[x][y]
            prevValue = map[preX][preY]

            #if current one is same with previous one, respectiveness would + 1
            if (checkValue==target and prevValue==target): 
                respectively+=1
            #after become 0 above, next value would be 1 as same as the checking of first element
            elif (checkValue==target and prevValue!=target): 
                respectively=1
        if (respectively==winCondition): return True
        else: return False

    def checkStraightLine(map, vectorChange, vectorStay, target, direction, winCondition):
        size = len(map)
        #start and end would be the whole line to check value is respective
        start = vectorChange-winCondition-1
        if (start<0): start = 0
        end = vectorChange+winCondition+1
        if (end > size): end = size

        #check the first element because next would check the current with the previous one is same or not
        if (direction=="vertical"): x, y = start, vectorStay
        else: y, x = start, vectorStay
        if ((map[x][y]==target)): 
            respectively = 1
        else: 
            respectively = 0

        #from the second element and go on to check
        for i in range(start+1, end):
            if (direction=="vertical"):
                x, y, preX, preY = i, vectorStay, i-1, vectorStay
            else:
                x, y, preX, preY = vectorStay, i, vectorStay, i-1
            
            checkValue = map[x][y]
            prevValue = map[preX][preY]

            #if current one is same with previous one, respectiveness would + 1
            if (checkValue==target and prevValue==target): 
                respectively+=1
            #after become 0 above, next value would be 1 as same as the checking of first element
            elif (checkValue==target and prevValue!=target): 
                respectively=1

        if (respectively==winCondition): return True
        else: return False

    def checkWin(map, currentMoveX, currentMoveY, winCondition):
        target = map[currentMoveX][currentMoveY]
        if (TicTacToe.checkStraightLine(map, currentMoveX, currentMoveY, target, "vertical", winCondition)):
            return target
        elif (TicTacToe.checkStraightLine(map, currentMoveY, currentMoveX, target, "horizonal", winCondition)):
            return target
        elif (TicTacToe.checkDiagonal(map, currentMoveX, currentMoveY, target, "left", winCondition)):
            return target
        elif (TicTacToe.checkDiagonal(map, currentMoveX, currentMoveY, target, "right", winCondition)):
            return target
        if (TicTacToe.checkDraw(map)): return 0
        return -1