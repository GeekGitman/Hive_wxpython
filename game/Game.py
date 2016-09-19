import math
import copy

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

def hashPos(pos):
    hpos = '%d'%pos[0]+'%d'%pos[1]
    return hash(hpos)

class Game:
    def __init__(self):
        self.__P1 = 0                     #玩家一，执黑棋，先手
        self.__P2 = 1                     #玩家二，执白棋，后手
        self.__NEAR = [[0, 1], [1, 1], [1, 0], [0, -1], [-1, -1], [-1, 0]]                    #周围一圈的坐标偏移量，从上方开始顺时针
        self.__STARTPOSITION = [0, 0, -1]                  #默认的启示位置，棋子在这个坐标时表示尚未下该子
        self.__numOfPlayers = 2                   #人类玩家数量。取值为1或2
        self.__map = [[], []]                 #棋盘状态。第一列是玩家一的棋子所在坐标。坐标为三维，表示位置和高度。在桌面，记为高度1。顺序是1蜂后，3工蚁，2蜘蛛，3蟋蟀，2甲虫。第二列为玩家二，顺序相同
        self.__action = [0, 0, 1]                    #记录最后一步棋子的位置，游戏中高亮显示
        self.__round = 1                  #记录当前回合数
        self.__currentPlayer = self.__P1                   #当前下子的玩家。
        self.__first = -1
        self.__drawFlag = 0
        self.__find = {}
        for i in range(11):                 #初始化所有棋子
            self.__map[0].append(self.__STARTPOSITION)
            self.__map[1].append(self.__STARTPOSITION)
        self.__angleWeight = self.__getAngleWeight()
        self.__axleWeight = self.__getAxleWeight()
        self.__kindWeight = [[20, 15, 15, 15, 10, 10, 5, 5, 5, 1, 1],[45, 40, 40, 40, 35, 35, 30, 30, 30, 25, 25]]

    def restart(self):
        self.__init__()

    def __changePlayer(self):                 #回合结束，下子玩家交替
        self.__currentPlayer = 1 - self.__currentPlayer

    def getCurrentPlayer(self):
        return self.__currentPlayer

    def getRound(self):
        return self.__round

    def setNumOfPlayers(self, num):
        self.__numOfPlayers = num

    def getNumOfPlayers(self):
        return self.__numOfPlayers

    def getCurrentState(self):                  #返回[地图状态，最后一步]
        return [self.__map, self.__action]

    def moveChess(self, id, goal):                  #移动棋子到指定位置。其中goal必须从下面的getSuccessor函数中取得，否则会导致错误
        if (self.__round == 1) and (self.__currentPlayer == 0):
            self.__first = id
        if self.__map[self.__currentPlayer][id] != self.__STARTPOSITION:
            if self.__map[self.__currentPlayer][id][2] > 1:
                del self.__find[hashPos(self.__map[self.__currentPlayer][id])][-1]
            else:
                del self.__find[hashPos(self.__map[self.__currentPlayer][id])]
        self.__map[self.__currentPlayer][id] = goal
        try:
            self.__find[hashPos(goal)].append([self.__currentPlayer, id])
        except:
            self.__find[hashPos(goal)]=[[self.__currentPlayer, id]]
        self.__action = goal
        if self.__currentPlayer == self.__P2:                   #玩家二下完子后，回合数加一
            self.__round += 1
        self.__changePlayer()                     #玩家交替
        self.__drawFlag = 0
        return True

    def skipRound(self):
        self.__changePlayer()
        self.__drawFlag += 1

    def getFirst(self):
        return self.__first

    def isLose(self, player):                   #判断该玩家是否失败
        if self.__map[player][0] ==  self.__STARTPOSITION:                  #若蜂后还未下出，则不会失败
            return False
        return self.__getBlank(player, 0) == []                   #若蜂后周围没有空位，则失败

    def isWin(self, player):                    #判断该玩家是否胜利
        return self.isLose(1 - player)                  #若对手失败，则玩家胜利

    def isDraw(self):
        return self.__drawFlag >= 2

    def isEnd(self):
        return self.isWin(0) or self.isWin(1) or self.isDraw()

    def __getBlank(self, player, id):                 #获取某个棋子周围的空位。返回[坐标1，坐标2，1]的列表表示
        blank = []
        if self.__map[player][id] == self.__STARTPOSITION:                  #若该子尚未下出，则没有空位
            return []
        for near in self.__NEAR:                      #考察周围六个位置
            checkPos = [self.__map[player][id][0] + near[0], self.__map[player][id][1] + near[1], 1]
            try:
                self.__find[hashPos(checkPos)]
            except:
                blank.append(checkPos)
        return blank

    def getChessNum(self, var):                  #获得某玩家某棋子的同类棋子尚未下出的数量
        num = 0
        player = var[0]
        id = var[1]
        if id == 0:
            if self.__map[player][0] == self.__STARTPOSITION:
                num = 1
        elif id < 4:
            for i in range(3):
                if self.__map[player][i + 1] == self.__STARTPOSITION:
                    num += 1
        elif id < 6:
            for i in range(2):
                if self.__map[player][i + 4] == self.__STARTPOSITION:
                    num += 1
        elif id < 9:
            for i in range(3):
                if self.__map[player][i + 6] == self.__STARTPOSITION:
                    num += 1
        else:
            for i in range(2):
                if self.__map[player][i + 9] == self.__STARTPOSITION:
                    num += 1
        return num

    def getSuccessor(self, id):                 #返回当前玩家某个棋子的后继，用[坐标1，坐标2，高度]的列表表示
        next = []
        if self.__round == 1:                 #第一回合的先手玩家默认下在桌面原点
            if self.__currentPlayer == self.__P1:
                next = [[0, 0, 1]]
                return next
            else:                       #第一回合的后手玩家只能下在先手的边上
                for near in self.__NEAR:
                    next.append(near + [1])
                return next
        if self.__map[self.__currentPlayer][0] == self.__STARTPOSITION:                   #若蜂后未下出
            if (self.__round == 4) and (id != 0):                 #第四回合必须下蜂后，若此时选择的棋子不是蜂后则没有后继
                return next
            elif self.__map[self.__currentPlayer][id] != self.__STARTPOSITION:                    #己方蜂后未下出，其他已下出的棋子不能移动
                return next
        if self.__map[self.__currentPlayer][id] == self.__STARTPOSITION:                  #新下出的棋子必须靠在己方其他桌面上棋子的空白位置
            for i in range(11):
                if self.__map[self.__currentPlayer][i][2] == 1:
                    for blank in self.__getBlank(self.__currentPlayer, i):
                        if blank not in next:
                            next.append(blank)
            return next
        if self.__isCovered(self.__currentPlayer, id):                  #若棋子被盖住，则不能移动
            return next
        if id == 0:                 #以下表示不同种类的棋子按各自的规则移动
            next = self.__getBeeSuccessor(self.__currentPlayer)
            return next
        if id in [1, 2, 3]:
            next = self.__getAntSuccessor(self.__currentPlayer, id)
            return next
        if id in [4, 5]:
            next = self.__getSpiderSuccessor(self.__currentPlayer, id)
            return next
        if id in [6, 7, 8]:
            next = self.__getCricketSuccessor(self.__currentPlayer, id)
            return next
        if id in [9, 10]:
            next = self.__getBeetleSuccessor(self.__currentPlayer, id)
            return next

    def getAllSuccessors(self):
        next = []
        beenext = []
        unset = []
        num = 0
        player = self.__currentPlayer
        # judge chess except for queen
        for i in range(1, 10):
            pos = self.__map[player][i]
            for checkPos in self.getSuccessor(i):
                if pos != self.__STARTPOSITION:
                    if pos[2] == 1:
                        del self.__find[hashPos(pos)]
                    else:
                        del self.__find[hashPos(pos)][-1]
                    self.__map[player][i] = checkPos
                    if checkPos[2] == 1:
                        self.__find[hashPos(checkPos)] = [[player, i]]
                    else:
                        self.__find[hashPos(checkPos)].append([player, i])
                    if self.isWin(player):
                        if checkPos[2] == 1:
                            del self.__find[hashPos(checkPos)]
                        else:
                            del self.__find[hashPos(checkPos)][-1]
                        self.__map[player][i] = pos
                        if pos[2] == 1:
                            self.__find[hashPos(pos)] = [[player, i]]
                        else:
                            self.__find[hashPos(pos)].append([player, i])
                        return [[i, checkPos]]
                    next.append([i, checkPos])
                    if checkPos[2] == 1:
                        del self.__find[hashPos(checkPos)]
                    else:
                        del self.__find[hashPos(checkPos)][-1]
                    self.__map[player][i] = pos
                    if pos[2] == 1:
                        self.__find[hashPos(pos)] = [[player, i]]
                    else:
                        self.__find[hashPos(pos)].append([player, i])
                else:
                    self.__map[player][i] = checkPos
                    self.__find[hashPos(checkPos)] = [[player, i]]
                    if self.isWin(player):
                        del self.__find[hashPos(checkPos)]
                        self.__map[player][i] = pos
                        return [[i,checkPos]]
                    next.append([i,checkPos])
                    del self.__find[hashPos(checkPos)]
                    self.__map[player][i] = pos
        next1 = []
        for chess in next:
            if [chess[1][0]-self.__map[1-player][0][0], chess[1][1]-self.__map[1-player][0][1]] in (self.__NEAR + [0, 0]):
                next1.append(chess)
        # judge queen
        if self.__map[player][0] != self.__STARTPOSITION:
            num = len(self.__getBlank(player, 0))
        pos = self.__map[player][0]
        for checkPos in self.getSuccessor(0):
            if self.__map[player][0] != self.__STARTPOSITION:
                del self.__find[hashPos(pos)]
                self.__map[player][0] = checkPos
                self.__find[hashPos(checkPos)] = [[player, 0]]
                if self.isWin(player):
                    del self.__find[hashPos(checkPos)]
                    self.__map[player][0] = pos
                    self.__find[hashPos(pos)] = [[player, 0]]
                    return [[0,checkPos]]
                newnum = len(self.__getBlank(player, 0))
                if newnum >= num:
                    beenext.append([0,pos])
                del self.__find[hashPos(checkPos)]
                self.__map[player][0] = pos
                self.__find[hashPos(pos)] = [[player, 0]]
            else:
                self.__map[player][0] = checkPos
                self.__find[hashPos(checkPos)] = [[player, 0]]
                if self.isWin(player):
                    del self.__find[hashPos(checkPos)]
                    self.__map[player][0] = pos
                    return [[0,checkPos]]
                beenext.append([0, checkPos])
                del self.__find[hashPos(checkPos)]
                self.__map[player][0] = pos
        if self.__getBlank(player,0)<=3 and beenext!=[]:
            print 'beenext:',beenext
            return beenext
        # return successors that has to choose randomly
        if next1 != []:
            return next1 + beenext
        else:
            return next + beenext


    def hasNext(self):
        next = []
        unset = []
        for chess in range(11):
            if self.__map[self.__currentPlayer][chess] != self.__STARTPOSITION:
                succes = self.getSuccessor(chess)
                for succ in succes:
                    next.append([chess,succ])
            else:
                unset.append(chess)
        if unset != []:
            succes = self.getSuccessor(unset[0])
            for chess in unset:
                for succ in succes:
                    next.append([chess,succ])
        return len(next) == 0

    def __isCovered(self, player, id):                    #某个棋子是否被覆盖
        checkPos = self.__map[player][id]                 #对于当前棋子的位置，若存在相同位置高度更高的棋子，则被覆盖
        if checkPos[2] != len(self.__find[hashPos(checkPos)]):
            return True
        else:
            return False

    def __isConnectivity(self):                   #判断当前游戏是否连通。使用种子染色法
        domain = [([True]*11) for i in range(2)]                  #宽搜查重数组。True表示进过宽搜队列了。注意未下出的棋子不能考虑进来，故也置为True
        for temp in self.__find.values():
            for chess in temp:
                domain[chess[0]][chess[1]] = False
        startID = domain[1 - self.__currentPlayer].index(False)
        domain[1 - self.__currentPlayer][startID] = True
        queue = Queue()
        queue.push(self.__map[1 - self.__currentPlayer][startID])
        while not queue.isEmpty():
            node = queue.pop()
            for near in self.__NEAR:                  #将已下出的未考察过的相邻棋子加入宽搜队列中
                checkPos = [node[0] + near[0], node[1] + near[1]]
                try:
                    for chess in self.__find[hashPos(checkPos)]:
                        if not domain[chess[0]][chess[1]]:
                            domain[chess[0]][chess[1]] = True
                            queue.push(self.__map[chess[0]][chess[1]])
                except:
                    continue
        return domain[0].count(False) + domain[1].count(False) == 0                 #若查重数组全为True，则表示全部连通了

    def __getLegalOneSteps(self, player, id):                 #获得某个棋子在桌面上（！）的合法一步移动位置，返回[坐标1，坐标2，1]列表
        next = []
        pos = self.__map[player][id]
        del self.__find[hashPos(pos)]
        self.__map[player][id] = self.__STARTPOSITION
        flag = self.__isConnectivity()
        self.__find[hashPos(pos)] = [[player, id]]
        self.__map[player][id] = pos
        if not flag:
            return next
        blankPos = self.__getBlank(player, id)
        for goal in range(6):                   #满足以下三点移动是合法的：1、目标位置是空的；2、目标位置的左右有且只有一个位置有棋子；3、移动后不导致连通性破坏。六个方向分别考虑
            flag = True
            left = goal - 1
            if left == -1:
                left = 5
            right = goal + 1
            if right == 6:
                right = 0
            checkPos = [pos[0] + self.__NEAR[goal][0], pos[1] + self.__NEAR[goal][1], 1]
            leftPos =  [pos[0] + self.__NEAR[left][0], pos[1] + self.__NEAR[left][1], 1]
            rightPos =  [pos[0] + self.__NEAR[right][0], pos[1] + self.__NEAR[right][1], 1]
            if not ((checkPos in blankPos) and (((leftPos in blankPos) and (rightPos not in blankPos))or((leftPos not in blankPos) and (rightPos in blankPos)))):
                flag = False
            if flag:
                next.append(checkPos)
        return next

    def __getBeeSuccessor(self, player):                  #蜂后只能在桌面上，一次移动一步
        return self.__getLegalOneSteps(player, 0)

    def __getAntSuccessor(self, player, id):                  #工蚁能在桌面上移动任意步，采用宽搜
        next = []
        queue = Queue()
        begin = self.__map[player][id]
        next.append(begin)                  #为了方便，先将起始点添加进队列中，最后再删去
        queue.push(begin)
        while not queue.isEmpty():
            node = queue.pop()
            del self.__find[hashPos(self.__map[player][id])]
            self.__map[player][id] = node                 #假设工蚁移动到了这个（合法的）位置后
            self.__find[hashPos(node)] = [[player, id]]
            oneSteps = self.__getLegalOneSteps(player, id)
            for step in oneSteps:
                if step not in next:
                    next.append(step)
                    queue.push(step)
        del(next[0])
        del self.__find[hashPos(self.__map[player][id])]
        self.__map[player][id] = begin                    #将工蚁放回原位
        self.__find[hashPos(begin)] = [[player, id]]
        return next

    def __getSpiderSuccessor(self, player, id):                   #蜘蛛每次必须在桌面上走三步且不能回头，利用函数嵌套，用带深度的深搜递归实现
        next = []

        def dfs(depth, path):
            if (depth == 3) and (path[3] not in next):                  #走了不回头的三步了，将到达的位置加入结果中
                next.append(path[3])
            else:
                begin = path[depth]
                oneSteps = self.__getLegalOneSteps(player, id)
                for step in oneSteps:
                    if step not in path:                    #不允许回头
                        path.append(step)
                        del self.__find[hashPos(self.__map[player][id])]
                        self.__map[player][id] = step                 #假设蜘蛛移动到了这个位置
                        self.__find[hashPos(step)] = [[player, id]]
                        dfs(depth + 1, path)
                        del(path[-1])
                        del self.__find[hashPos(self.__map[player][id])]
                        self.__map[player][id] = begin                #回溯，将蜘蛛放回原位
                        self.__find[hashPos(begin)] = [[player, id]]

        dfs(0, [self.__map[player][id]])
        return next

    def __getCricketSuccessor(self, player, id):                  #蟋蟀每次可以朝六个方向跳到相邻其它棋子的尽头，然后落回桌面上
        next = []
        begin = self.__map[player][id]
        del self.__find[hashPos(begin)]
        self.__map[player][id] = self.__STARTPOSITION                   #先检查蟋蟀离开是否会导致不连通
        if not self.__isConnectivity():
            self.__find[hashPos(begin)] = [[player, id]]
            self.__map[player][id] = begin
            return []
        self.__find[hashPos(begin)] = [[player, id]]
        self.__map[player][id] = begin

        def isOccupied(checkPos):
            try:
                self.__find[hashPos(checkPos)]
            except:
                return False
            return True

        for near in self.__NEAR:                      #对于六个方向分别考察
            checkPos = [begin[0] + near[0], begin[1] + near[1], 1]
            while isOccupied(checkPos):                     #直到该方向的尽头
                checkPos[0] += near[0]
                checkPos[1] += near[1]
            if checkPos != [begin[0] + near[0], begin[1] + near[1], 1]:                 #若该方向无相邻棋子，则不能移动
                next.append(checkPos)
        return next

    def __getBeetleSuccessor(self, player, id):                   #甲虫的移动相对复杂。分为甲虫在桌面上和不再桌面上两种情况
        next = []
        around = []
        begin = self.__map[player][id]
        for near in self.__NEAR:                      #先获得周围六个相邻位置的高度。
            checkPos = [begin[0] + near[0], begin[1] + near[1], 0]
            try:
                checkPos[2] = self.__map[self.__find[hashPos(checkPos)][-1][0]][self.__find[hashPos(checkPos)][-1][1]][2]
                around.append(checkPos)
            except:
                around.append(checkPos)
                continue
        if begin[2] == 1:                   #若甲虫在桌面上，考察六个方向
            for goal in range(6):
                flag = True
                left = goal - 1
                if left == -1:
                    left = 5
                right = goal + 1
                if right == 6:
                    right = 0
                checkPos = around[goal]
                leftPos =  around[left]
                rightPos =  around[right]
                if checkPos[2] == 0:                    #若目标点也在桌面上，那么合法的移动需要遵循的规则与getLegalOneSteps相同
                    if (((leftPos[2] == 0) and (rightPos[2] == 0)) or ((leftPos[2] > 0) and (rightPos[2] > 0))):
                        flag = False
                else:                   #若目标点不在桌面上，那么需要满足：1、目标点没被阻挡；2、且移动后不导致连通性被破坏
                    if (leftPos[2] > checkPos[2]) and (rightPos[2] > checkPos[2]):
                        flag = False
                if flag:
                    del self.__find[hashPos(begin)]
                    self.__map[player][id] = [checkPos[0], checkPos[1], checkPos[2] + 1]
                    if checkPos[2] != 0:
                        self.__find[hashPos([checkPos[0], checkPos[1], checkPos[2] + 1])].append([player, id])
                    else:
                        self.__find[hashPos([checkPos[0], checkPos[1], checkPos[2] + 1])] = [[player, id]]
                    flag = self.__isConnectivity()
                    if checkPos[2] != 0:
                        del self.__find[hashPos([checkPos[0], checkPos[1], checkPos[2] + 1])][-1]
                    else:
                        del self.__find[hashPos([checkPos[0], checkPos[1], checkPos[2] + 1])]
                    self.__map[player][id] = begin
                    self.__find[hashPos(begin)] = [[player, id]]
                if flag:
                    next.append([checkPos[0], checkPos[1], checkPos[2] + 1])
        else:                   #若甲虫不在桌面上，分别考察六个方向
            for goal in range(6):
                flag = True
                left = goal - 1
                if left == -1:
                    left = 5
                right = goal + 1
                if right == 6:
                    right = 0
                checkPos = around[goal]
                leftPos =  around[left]
                rightPos =  around[right]
                if min(leftPos[2], rightPos[2]) > max(checkPos[2], begin[2] - 1):                   #无论目标点的高度，只需要满足左右两点不同时高于当前高度减一和目标高度即可移动
                    flag = False
                if flag:
                    next.append([checkPos[0], checkPos[1], checkPos[2] + 1])
        return next

    def deepCopy(self):
        g = Game()
        g.setNumOfPlayers(self.__numOfPlayers)
        g._Game__map = copy.deepcopy(self.__map)
        g._Game__action = self.__action
        g._Game__round = self.__round
        g._Game__currentPlayer = self.__currentPlayer
        g._Game__first = self.__first
        g._Game__find = copy.deepcopy(self.__find)
        g._Game__drawFlag = self.__drawFlag
        return g

    def __getAngleWeight(self):
        weight = [([0] * 60) for i in range(60)]
        for i in range(30):
            x = 0
            y = i
            value = i*6
            weight[x + 30][y + 30] = value
            for j in range(3):
                for k in range(i):
                    x += self.__NEAR[j + 2][0]
                    y += self.__NEAR[j + 2][1]
                    value -= 1
                    weight[x + 30][y + 30] = value
                    weight[-x + 30][y - x + 30] = value
        return weight

    def __getAxleWeight(self):
        weight = [([0]*60) for i in range(60)]
        for i in range(60):
            weight[i] = i - 30
        return weight

    def normalize(self):
        if self.__first == -1:
            return [self.__map,[]]
        centre = self.__map[0][self.__first]
        newMap = copy.deepcopy(self.__map)

        for pos in (newMap[0] + newMap[1]):
            if pos != self.__STARTPOSITION:
                pos[0] -= centre[0]
                pos[1] -= centre[1]

        max = 0
        temp = copy.deepcopy(newMap)
        for i in range(2):
            for j in range(11):
                if newMap[i][j] != self.__STARTPOSITION:
                    max += self.__angleWeight[newMap[i][j][0] + 30][newMap[i][j][1] + 30]*self.__kindWeight[i][j]
        for angle in range(5):
            score = 0
            for i in range(2):
                for j in range(11):
                    if newMap[i][j] != self.__STARTPOSITION:
                        a = newMap[i][j][0]
                        b = newMap[i][j][1]
                        newMap[i][j][0] = a - b
                        newMap[i][j][1] = a
            for i in range(2):
                for j in range(11):
                    if newMap[i][j] != self.__STARTPOSITION:
                        score += self.__angleWeight[newMap[i][j][0] + 30][newMap[i][j][1] + 30]*self.__kindWeight[i][j]
            if score > max:
                max = score
                temp = copy.deepcopy(newMap)
        newMap = copy.deepcopy(temp)

        max = 0
        for i in range(2):
            for j in range(11):
                if newMap[i][j] != self.__STARTPOSITION:
                    max += self.__axleWeight[newMap[i][j][0] + 30]*self.__kindWeight[i][j]
        score = 0
        for i in range(2):
            for j in range(11):
                if newMap[i][j] != self.__STARTPOSITION:
                    score += self.__axleWeight[-newMap[i][j][0] + 30]*self.__kindWeight[i][j]
        if score > max:
            for i in range(2):
                for j in range(11):
                    if newMap[i][j] != self.__STARTPOSITION:
                        newMap[i][j][0] = -newMap[i][j][0]
                        newMap[i][j][1] += newMap[i][j][0]

        return [newMap,[0,0,-1]]
