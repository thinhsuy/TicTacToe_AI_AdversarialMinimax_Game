player = 2
bot = 1
winRule = 4
defaultVal = 0
point = 1

def setPointRightDiagonal(map, pos):
    front = (pos[0]+winRule-1, pos[1]-winRule+1)
    back = (pos[0]-winRule+1, pos[1]+winRule-1)

    #tính thêm điểm cộng nếu có nhiều con liên tiếp nhau
    bonusPoint = 0
    for i, j in zip(range(front[0], back[0]-1, -1), range(front[1], back[1]+1, 1)):
        if (i<0 or i>=len(map) or j<0 or j>=len(map)): continue
        if (map[i][j] >= defaultVal): continue
        #nếu có nhìu mục tiêu liên tiếp nhau thì sẽ ưu tiên chặn player hơn là cố chấp thắng
        #vì Heuristic không đủ thông minh để đoán được suy tính của 1 con người -> ưu tiên chặn trước
        if map[i][j] == map[pos[0]][pos[1]]:
            bonusPoint+=2
        else: 
            bonusPoint+=1

    #ghi điểm cho chéo phải
    for i, j in zip(range(front[0], back[0]-1, -1), range(front[1], back[1]+1, 1)):
        if (i<0 or i>=len(map) or j<0 or j>=len(map)): continue
        #ghi cho đến khi gặp 1 đối thủ chặn đường thì nghĩa là từ sau kẻ đó sẽ ko được đánh nữa
        if map[i][j]<defaultVal and map[i][j]!=map[pos[0]][pos[1]]:
            return map
        if (map[i][j] < defaultVal): continue
        map[i][j]+=point+bonusPoint
    return map

def setPointLeftDiagonal(map, pos):
    front = (pos[0]-winRule+1, pos[1]-winRule+1)
    back = (pos[0]+winRule-1, pos[1]+winRule-1)

    #tính thêm điểm cộng nếu có nhiều con liên tiếp nhau
    bonusPoint = 0
    for i, j in zip(range(front[0], back[0]+1), range(front[1], back[1]+1)):
        if (i<0 or i>=len(map) or j<0 or j>=len(map)): continue
        if map[i][j] >= defaultVal: continue
        #nếu có nhìu mục tiêu liên tiếp nhau thì sẽ ưu tiên chặn player hơn là cố chấp thắng
        #vì Heuristic không đủ thông minh để đoán được suy tính của 1 con người -> ưu tiên chặn trước
        if map[i][j] == map[pos[0]][pos[1]]:
            bonusPoint+=2
        else: 
            bonusPoint+=1
    
    #ghi điểm cho chéo trái
    for i, j in zip(range(front[0], back[0]+1), range(front[1], back[1]+1)):
        if (i<0 or i>=len(map) or j<0 or j>=len(map)): continue
        #ghi cho đến khi gặp 1 đối thủ chặn đường thì nghĩa là từ sau kẻ đó sẽ ko được đánh nữa
        if map[i][j]<defaultVal and map[i][j]!=map[pos[0]][pos[1]]:
            return map
        if map[i][j] < defaultVal: continue
        map[i][j]+=point+bonusPoint
    return map

def setPointHorizonal(map, pos):
    front = pos[1]-winRule+1
    if (front<=0): front=0
    back = pos[1]+winRule-1
    if (back>=len(map)): back = len(map)-1

    #tính thêm điểm cộng nếu có nhiều con liên tiếp nhau
    bonusPoint = 0
    for i in range(front, back+1):
        if map[pos[0]][i]>=defaultVal: continue
        #nếu có nhìu mục tiêu liên tiếp nhau thì sẽ ưu tiên chặn player hơn là cố chấp thắng
        #vì Heuristic không đủ thông minh để đoán được suy tính của 1 con người -> ưu tiên chặn trước
        if map[pos[0]][i] == map[pos[0]][pos[1]]:
            bonusPoint+=2
        else: 
            bonusPoint+=1

    #ghi điểm cho đường ngang
    for i in range(front, back+1):
        #ghi cho đến khi gặp 1 đối thủ chặn đường thì nghĩa là từ sau kẻ đó sẽ ko được đánh nữa
        if map[pos[0]][i]<defaultVal and map[pos[0]][i]!=map[pos[0]][pos[1]]:
            return map
        if map[pos[0]][i]<defaultVal: continue
        map[pos[0]][i]+=point+bonusPoint
    return map

def setPointVertical(map, pos):
    front = pos[0]-winRule+1
    if (front<=0): front=0
    back = pos[0]+winRule-1
    if (back>=len(map)): back = len(map)-1

    #tính thêm điểm cộng nếu có nhiều con liên tiếp nhau
    bonusPoint = 0
    for i in range(front, back+1):
        if map[pos[0]][i]>=defaultVal: continue
        #nếu có nhìu mục tiêu liên tiếp nhau thì sẽ ưu tiên chặn player hơn là cố chấp thắng
        #vì Heuristic không đủ thông minh để đoán được suy tính của 1 con người -> ưu tiên chặn trước
        if map[pos[0]][i] == map[pos[0]][pos[1]]:
            bonusPoint+=2
        else: 
            bonusPoint+=1

    #ghi điểm cho đường dọc
    for i in range(front, back+1):
        #ghi cho đến khi gặp 1 đối thủ chặn đường thì nghĩa là từ sau kẻ đó sẽ ko được đánh nữa
        if map[i][pos[1]]<defaultVal and map[i][pos[1]]!=map[pos[0]][pos[1]]:
            return map
        if map[i][pos[1]]<defaultVal: continue
        map[i][pos[1]]+=point+bonusPoint
    return map

def setDefaultHeuristic(map):
    #gán giá trị cơ bản Heuristic cho map trước
    #đây là giá trị bàn cờ lúc chưa có gì cả
    for i in range(len(map)):
        for j in range(len(map)):
            temp = map[i][j]
            #if (temp < defaultVal): continue
            #gán tạm vị trí đó là có đi rồi để tính điểm
            map[i][j]=-bot
            map = setPointHorizonal(map, (i, j))
            map = setPointVertical(map, (i, j))
            map = setPointLeftDiagonal(map, (i, j))
            map = setPointRightDiagonal(map, (i, j))
            #tính xong thì trả lại như cũ
            map[i][j]=temp+1
    
    return map

def setHeuristic(map):
    #gán giá trị Heuristic tương ứng với từng vị trí được đánh
    #đây là giá trị bàn cờ đã có các bước đi
    maze = [[0 for _ in range(len(map))] for _ in range(len(map))]
    maze = setDefaultHeuristic(maze)
    for i in range(len(map)):
        for j in range(len(map)):
            if (map[i][j]==player or map[i][j]==bot): maze[i][j]=-map[i][j]

    for i in range(len(maze)):
        for j in range(len(maze)):
            if maze[i][j]>=defaultVal: continue
            maze = setPointHorizonal(maze, (i, j))
            maze = setPointVertical(maze, (i, j))
            maze = setPointLeftDiagonal(maze, (i, j))
            maze = setPointRightDiagonal(maze, (i, j))
    return maze
            
def getMax(map):
    #tìm ra giá trị cao nhất
    map = setHeuristic(map)
    max = -10000
    move = tuple()
    for i in range(len(map)):
        for j in range(len(map)):
            if (map[i][j]>=defaultVal and map[i][j]>max):
                max = map[i][j]
                move = (i, j)
    return move

maze = [[0 for _ in range(5)] for _ in range(5)]
maze[0][0] = player
a = getMax(maze)

#impot file này và gọi hàm getMax(map) và truyền vào tọa độ bàn cờ hiện tại
#hàm này sẽ trả về 1 tuple(x, y) với (x, y) là vị trí BOT sẽ đi
#vì đây chỉ là Heuristic nên người chơi có thê trick 1 vài bước để giành chiến thắng
#hàm Heuristic này vẫn còn rất là basic, nên hãy cải tiến nó thêm nếu muốn chắc chắn win hơn