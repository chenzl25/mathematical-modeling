class Node:
  def __init__(self):
    self.upEdge = None
    self.downEdge = None
    self.rightEdge = None
    self.leftEdge = None
    self.edgeCount = None
    self.upDis = 0
    self.downDis = 0
    self.rightDis = 0
    self.upPr = None
    self.downPr = None
    self.rightPr = None
    self.isRightEnd = False
    self.isUpEnd = False
    self.isDownEnd = False
    self.dis = None

  def getEdgeCount(self):
    if self.edgeCount == None:
      self.edgeCount = 0
      if self.upEdge != None:
        self.edgeCount += 1
      if self.downEdge != None:
        self.edgeCount += 1
      if self.rightEdge != None:
        self.edgeCount += 1
    return self.edgeCount
  def calPr(self):
    if self.isRightEnd:
      return
    total = 0
    if self.upEdge != None and self.upEdge.upNode.dis != None:
      self.upPr = 1.0 / self.upEdge.upNode.dis
      total += self.upPr
    if self.downEdge != None and self.downEdge.downNode.dis != None:
      self.downPr = 1.0 / self.downEdge.downNode.dis
      total += self.downPr
    if self.rightEdge != None and self.rightEdge.rightNode.dis != None:
      self.rightPr = 1.0 / (self.rightEdge.rightNode.dis + 1e-5)
      total += self.rightPr
    
    if total == 0:
      return

    if self.upEdge != None and self.upEdge.upNode.dis != None:
      self.upPr /= total
    if self.downEdge != None and self.downEdge.downNode.dis != None:
      self.downPr /= total
    if self.rightEdge != None and self.rightEdge.rightNode.dis != None:
      self.rightPr /= total

class Edge:
  def __init__(self):
    self.capability = 100
    self.upQueueLen = 0
    self.downQueueLen = 0
    self.rightQueueLen = 0
    self.upNode = None
    self.downNode = None
    self.rightNode = None
    self.leftNode = None
    self.speed = 20 # default
    self.isHorizontal = False
    self.isVertical = False
    self.dis = 1 # default
  def moveCar(self, num, up = False):
    outLen = 0
    moveNode = None
    if self.isHorizontal:
      if self.rightQueueLen < num:
        outLen = self.rightQueueLen
        self.rightQueueLen = 0
      else:
        outLen = num
        self.rightQueueLen -= num
      moveNode = self.rightNode
    elif up:
      if self.upQueueLen < num:
        outLen = self.upQueueLen
        self.upQueueLen = 0
      else:
        outLen = num
        self.upQueueLen -= num
      moveNode = self.upNode
    else:
      if self.downQueueLen < num:
        outLen = self.downQueueLen
        self.downQueueLen = 0
      else:
        outLen = num
        self.downQueueLen -= num
      moveNode = self.downNode
    
    if moveNode.isRightEnd:
      return outLen
    
    moveNode.calPr()
    leftover = outLen
    if moveNode.upPr != None:
      moveNode.upEdge.upQueueLen += int(outLen * moveNode.upPr)
      leftover -= int(outLen * moveNode.upPr)
    if moveNode.downPr != None:
      moveNode.downEdge.downQueueLen += int(outLen * moveNode.downPr)
      leftover -= int(outLen * moveNode.downPr)
    if moveNode.rightPr != None:
      moveNode.rightEdge.rightQueueLen += int(outLen * moveNode.rightPr)
      leftover -= int(outLen * moveNode.rightPr)

    if leftover > 0: # TO MODIFY
      if moveNode.upEdge:
        moveNode.upEdge.upQueueLen += leftover
      elif moveNode.downEdge:
        moveNode.downEdge.downQueueLen += leftover
      elif moveNode.rightEdge:
        moveNode.rightEdge.rightQueueLen += leftover

class Graph:
  def __init__(self, matrix):
    self.matrix = matrix
    self.fixMatrix =None
    self.nodes = None
    self.inputEdges = None
    self.outputCarCount = 0
    self.construct()
  def construct(self):
    self._construct(self.matrix)
    self.removeImpossibleEdge()
    self.addInputEdge()
    self.calDis()
    self.removeImpossibleEdge2()

  def _construct(self, matrix, isFix = False):
    w, h = len(matrix[0]) + 1, len(matrix) + 1
    nodes = getMatrix(h, w)
    for i in range(h):
      for j in range(w):
        nodes[i][j] = Node()
        if j == w-1:
          nodes[i][j].isRightEnd = True
        if i == 0:
          nodes[i][j].isUpEnd = True
        if i == h-1:
          nodes[i][j].isDownEnd = True
    for i in range(h-1):
      for j in range(w-1):
        if matrix[i][j] == 0:
          upEdge = Edge()
          upEdge.isHorizontal = True
          downEdge = Edge()
          downEdge.isHorizontal = True
          leftEdge = Edge()
          leftEdge.isVertical = True
          rightEdge = Edge()
          rightEdge.isVertical = True
          nodes[i][j].rightEdge = upEdge
          upEdge.rightNode = nodes[i][j+1]
          nodes[i][j+1].leftEdge = upEdge
          upEdge.leftNode = nodes[i][j]
          
          nodes[i][j].downEdge = leftEdge
          leftEdge.downNode = nodes[i+1][j]
          nodes[i+1][j].upEdge = leftEdge
          leftEdge.upNode = nodes[i][j]

          nodes[i][j+1].downEdge = rightEdge
          rightEdge.downNode = nodes[i+1][j+1]
          nodes[i+1][j+1].upEdge = rightEdge
          rightEdge.upNode = nodes[i][j+1]
          
          nodes[i+1][j].rightEdge = downEdge
          downEdge.rightNode = nodes[i+1][j+1]
          nodes[i+1][j+1].leftEdge = downEdge
          downEdge.leftNode = nodes[i+1][j]

    for j in range(w-1):
      if nodes[0][j].rightEdge == None:
        edge = Edge()
        nodes[0][j].rightEdge = edge
        edge.rightNode = nodes[0][j+1]
        edge.isHorizontal = True
        nodes[0][j+1].leftEdge = edge
        edge.leftNode = nodes[0][j]
      if nodes[h-1][j].rightEdge == None:
        edge = Edge()
        nodes[h-1][j].rightEdge = edge
        edge.rightNode = nodes[h-1][j+1]
        edge.isHorizontal = True
        nodes[h-1][j+1].leftEdge = edge
        edge.leftNode = nodes[h-1][j]
    
    for i in range(h-1):
      if nodes[i][0].downEdge == None:
        edge = Edge()
        edge.isVertical = True
        nodes[i][0].downEdge = edge
        edge.downNode = nodes[i+1][0]
        nodes[i+1][0].upEdge = edge
        edge.upNode = nodes[i][0]

    self.nodes = nodes

  def removeImpossibleEdge(self):
    w, h = len(self.nodes[0]), len(self.nodes)
    fixMatrix = getMatrix(h-1, w-1)
    change = False
    for i in range(h-1):
      for j in range(w-1):
        fixMatrix[i][j] = self.matrix[i][j]

    for j in range(w-1):
      first = -1
      last  = -1
      for i in range(h-1):
        if self.matrix[i][j] == 1:
          if first == -1:
            first = i
            continue
          last = i
      if first == -1 or last == -1 or first == last:
        continue
      for k in range(first+1, last+1):
        if fixMatrix[k][j] == 0:
          fixMatrix[k][j] = 1
          change = True
  
    if change == True:
      self._construct(fixMatrix, True)

  def removeImpossibleEdge2(self):
    w, h = len(self.nodes[0]), len(self.nodes)
    for j in range(w-1):
      first = -1
      last  = -1
      for i in range(h-1):
        if self.matrix[i][j] == 1:
          if first == -1:
            first = i
            last  = i
            continue
          last = i
      if first != -1:
        for k in range(first):
          if self.nodes[k][j+1].downEdge:
            self.nodes[k][j+1].downEdge.downNode = None
            self.nodes[k][j+1].downEdge = None
      if last != -1:
        for k in range(last+1,h):
          if self.nodes[k][j+1].upEdge:
            self.nodes[k][j+1].upEdge.upNode = None
            self.nodes[k][j+1].upEdge = None

  def addInputEdge(self):
    w, h = len(self.nodes[0]), len(self.nodes)
    inputEdges = []
    for i in range(h):
      edge = Edge()
      inputEdges.append(edge)
      edge.rightNode = self.nodes[i][0]
      edge.isHorizontal = True
      edge.capability = 100000000
      edge.rightQueueLen = edge.capability

    self.inputEdges = inputEdges

  def calDis(self):
    w, h = len(self.nodes[0]), len(self.nodes)
    visit = getMatrix(h, w, False)
    queue = []
    for i in range(h):
      queue.append((i, w-1))
      self.nodes[i][w-1].dis = 0

    while len(queue) != 0:
      x,y = queue[0]
      print x,y
      queue = queue[1:]
      cur = self.nodes[x][y]
      if visit[x][y] == True:
        continue
      visit[x][y] = True
      if cur.leftEdge and visit[x][y-1] == False:
        if self.nodes[x][y-1].dis == None:
          self.nodes[x][y-1].dis = cur.leftEdge.dis + cur.dis
        else:
          self.nodes[x][y-1].dis = min(self.nodes[x][y-1].dis, cur.leftEdge.dis + cur.dis)
        queue.append((x, y-1))
      if cur.upEdge and visit[x-1][y] == False:
        if self.nodes[x-1][y].dis == None:
          self.nodes[x-1][y].dis = cur.upEdge.dis + cur.dis
        else:
          self.nodes[x-1][y].dis = min(self.nodes[x-1][y].dis, cur.upEdge.dis + cur.dis)
        queue.append((x-1, y))
      if cur.downEdge and visit[x+1][y] == False:
        if self.nodes[x+1][y].dis == None:
          self.nodes[x+1][y].dis = cur.downEdge.dis + cur.dis
        else:
          self.nodes[x+1][y].dis = min(self.nodes[x+1][y].dis, cur.downEdge.dis + cur.dis)
        queue.append((x+1, y))

  def printDis(self):
    w, h = len(self.nodes[0]), len(self.nodes)
    for i in range(h):
      for j in range(w):
        print self.nodes[i][j].dis,
      print
  
  def printPr(self):
    w, h = len(self.nodes[0]), len(self.nodes)
    for i in range(h):
      for j in range(w):
        self.nodes[i][j].calPr()
        # print self.nodes[i][j].dis,
        print '(', '^:' ,self.nodes[i][j].upPr, 'v:', self.nodes[i][j].downPr, '>:', self.nodes[i][j].rightPr, ')',
      print

  def printDirection(self):
    nodes = self.nodes
    w, h = len(nodes[0]), len(nodes)
    for i in range(h):
      for j in range(w):
        print '..',
        print '--' if nodes[i][j].rightEdge and nodes[i][j].rightEdge.isHorizontal and j!=w-1 else '  ',
      print
      if i != h-1:
        for j in range(w):
          print '|' if nodes[i][j].downEdge and nodes[i][j].downEdge.isVertical and j!=w-1 else ' ',
          print ' ',
      print

  def printQueueLen(self):
    nodes = self.nodes
    w, h = len(nodes[0]), len(nodes)
    for i in range(h):
      for j in range(w):
        print '..',
        print nodes[i][j].rightEdge.rightQueueLen if nodes[i][j].rightEdge and j!=w-1 else '  ',
      print
      if i != h-1:
        for j in range(w):
          print nodes[i][j].downEdge.downQueueLen if nodes[i][j].downEdge and j!=w-1 else ' ',
          print nodes[i+1][j].upEdge.upQueueLen if nodes[i+1][j].upEdge and j!=w-1 else ' ',
          print ' ',
      print

  def printGraph(self):
    nodes = self.nodes
    w, h = len(nodes[0]), len(nodes)
    for i in range(h):
      for j in range(w):
        print '..',
        print '->' if nodes[i][j].rightEdge and j!=w-1 else '  ',
      print
      if i != h-1:
        for j in range(w):
          print '|' if nodes[i][j].downEdge and j!=w-1 else ' ',
          print '^' if nodes[i+1][j].upEdge and j!=w-1 else ' ',
          print ' ',
        print
        for j in range(w):
          print 'v' if nodes[i][j].downEdge and j!=w-1 else ' ',
          print '|' if nodes[i+1][j].upEdge and j!=w-1 else ' ',
          print ' ',
      print

  def flow(self, num, times):
    self.outputCarCount = 0 # init
    nodes = self.nodes
    w, h = len(nodes[0]), len(nodes)
    T = times
    while T != 0:
      T -= 1
      # iterate from right to left, move car from left to right
      for j in range(w-1)[::-1]:
        for i in range(h):
          if self.nodes[i][j].rightEdge:
            out = self.nodes[i][j].rightEdge.moveCar(int(self.nodes[i][j].rightEdge.speed))
            if self.nodes[i][j].rightEdge.rightNode.isRightEnd:
              self.outputCarCount += out
          
      # iterate from up to down, move car from down to up
      for i in range(1, h):
        for j in range(w):
          if self.nodes[i][j].upEdge:
            self.nodes[i][j].upEdge.moveCar(int(self.nodes[i][j].upEdge.speed), up = True) # TO MODIFY
      
      # iterate from down to up, move car from up to down
      for i in range(h-1)[::-1]:
        for j in range(w):
          if self.nodes[i][j].downEdge:
            self.nodes[i][j].downEdge.moveCar(int(self.nodes[i][j].downEdge.speed), up = False) # TO MODIFY

      for i in range(len(self.inputEdges)):
        self.inputEdges[i].moveCar(num)
      self.printQueueLen()
      print 'outputCarCount: ', self.outputCarCount



def getMatrix(h, w, init = -1):
  result = []
  for x in range(0, h):
    result.append([])
    for y in range(0, w):
      result[x].append(init)
  return result

if __name__ == '__main__':
  # m = getMatrix(5, 3)
  # m[0][0], m[0][1], m[0][2] = 1, 1, 1
  # m[1][0], m[1][1], m[1][2] = 1, 1, 1
  # m[2][0], m[2][1], m[2][2] = 1, 1, 1 
  # m[3][0], m[3][1], m[3][2] = 1, 1, 1 
  # m[4][0], m[4][1], m[4][2] = 1, 1, 1 

  # m = getMatrix(4, 3)
  # m[0][0], m[0][1], m[0][2] = 0, 1, 0
  # m[1][0], m[1][1], m[1][2] = 1, 1, 1 
  # m[2][0], m[2][1], m[2][2] = 1, 1, 0 
  # m[3][0], m[3][1], m[3][2] = 0, 1, 0 

  m = getMatrix(3, 3)
  m[0][0], m[0][1], m[0][2] = 1, 1, 1
  m[1][0], m[1][1], m[1][2] = 0, 0, 1 
  m[2][0], m[2][1], m[2][2] = 0, 1, 1 

  # m = getMatrix(5, 4)
  # m[0][0], m[0][1], m[0][2], m[0][3] = 1, 1, 1, 1
  # m[1][0], m[1][1], m[1][2], m[1][3] = 0, 0, 1, 1
  # m[2][0], m[2][1], m[2][2], m[2][3] = 1, 1, 1, 1
  # m[3][0], m[3][1], m[3][2], m[3][3] = 1, 0, 1, 0
  # m[4][0], m[4][1], m[4][2], m[4][3] = 1, 1, 0, 1


  g = Graph(m)
  g.printGraph()
  g.printDis()
  g.printPr()
  g.printDirection()
  g.flow(30, 20)

