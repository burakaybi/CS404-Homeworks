import time
import sys
from memory_profiler import memory_usage, profile


class Node:
    def __init__(self, x1, y1, x2=None, y2=None, parent=None):
        self.x_y = [(x1, y1)]
        if None != parent:
            self.parent = parent
        else:
            self.cost = 0

        if None != x1  and None != y2:
            self.x_y.append((x2, y2))

    def setParent(self, parent):
        self.parent = parent

    def setCost(self, cost):
        self.cost = cost


def add2queue(q, item):
    """
    q:  border as list object
    i:  item for added
    q:  your queue
    """
    length = len(q)
    if length > 0:
        minimum = q[0]
        maximum = q[length-1]
        if item[0] < minimum[0]:
            q.insert(0, item)
        elif item[0] > maximum[0]:
            q.append(item)
        else:
            tmp = 0
            for x in q:
                if x[0] < item[0]:
                    tmp = tmp + 1
            q.insert(tmp, item)
    else:
        q.append(item)

def is_in_the_arr(item, arr):
    for x in arr:
        if x[1].x_y == item.x_y:
            return x
    return None

def check_neighbors(ucsGraph, surface):
    if 1 == len(surface):  # the block is up
        x = surface[0][0]
        y = surface[0][1]
        neighbors = [Node(x, y-2, x, y-1),
                     Node(x, y+1, x, y+2),
                     Node(x-2, y, x-1, y),
                     Node(x+1, y, x+2, y)]
        for item in neighbors:
            for xy in item.x_y:
                x = xy[0]
                y = xy[1]
                try:
                    if "X" == ucsGraph[x][y]:
                        neighbors.remove(item)
                        break
                # means coordinates are out of bounds and we handle this exception and remove this coordinates our neighbors list
                except Exception as e:
                    neighbors.remove(item)
                    break
        return neighbors

    else:
        x1 = surface[0][0]
        y1 = surface[0][1]
        x2 = surface[1][0]
        y2 = surface[1][1]

        if x1 == x2:  # the block is vertical flat
            neighbors = [Node(x1, y1-1),
                         Node(x1, y2 + 1),
                         Node(x1 - 1, y1, x2 - 1, y2),
                         Node(x1 + 1, y1, x2 + 1, y2)]
            for item in neighbors:
                for xy in item.x_y:
                    x = xy[0]
                    y = xy[1]
                    try:
                        if "X" == ucsGraph[x][y]:
                            neighbors.remove(item)
                            break
                    # means coordinates are out of bounds and we handle this exception and remove this coordinates our neighbors list
                    except Exception as e:
                        neighbors.remove(item)
                        break
            return neighbors

        elif y1 == y2:  # the block is horizontal flat
            neighbors = [Node(x1, y1 - 1,x2, y2 - 1),
                         Node(x1, y1 + 1,x2, y2 + 1),
                         Node(x1 - 1, y1),
                         Node(x2 + 1, y2)]
            for item in neighbors:
                for xy in item.x_y:
                    x = xy[0]
                    y = xy[1]
                    try:
                        if "X" == ucsGraph[x][y]:
                            neighbors.remove(item)
                            break
                    # means coordinates are out of bounds and we handle this exception and remove this coordinates our neighbors list
                    except Exception as e:
                        neighbors.remove(item)
                        break
            return neighbors


@profile(precision=5)
def ucs(ucsGraph, start, g):
    """
    ucsGraph: game map representation as a matrix
    start: block starting position
    g: goal position
    return: UCS path
    """
    s_time = time.time()
    border = [(0, start)]  # priority, node
    banned = []

    while 0 != len(border):
        weight, node = border.pop(0)

        if node.x_y == g.x_y:
            elapsedTime=(time.time() - s_time)
            return node,elapsedTime

        success = check_neighbors(ucsGraph, node.x_y)
        for item in success:
            item.setParent(node)
            cost = node.cost + 1
            item.setCost(cost)

            borderCheck = is_in_the_arr(item, border)
            bannedCheck = is_in_the_arr(item, banned)

            if None == borderCheck and None == bannedCheck:
                add2queue(border, (cost, item))

            elif None != borderCheck and borderCheck[0] > cost:
                index = borderCheck.index(borderCheck)
                border[index] = (cost, item)

        add2queue(banned, (node.cost, node))
    print("*"*5 +" No Possible Path: "+ str((time.time() - s_time)) + " seconds  " + "*"*5 )
    return None

def pretier(Path):
    print("   The Game Map")
    res = [(sub[1], sub[0]) for sub in Path[0]]
    p = []
    for i in Path:
        p.append([(sub[1], sub[0]) for sub in i])
    filename = sys.argv[1]
    f = open(filename, mode='r')
    mm = f.readlines()
    satir =[]
    satir.append(" ")
    column = mm[0].replace("\n","")
    column = column.replace(" ","")
    for i in range(len(column)+1):
        satir.append(i)
    for i in range(len(column)+1):

        print(satir[i],end =" "),
    print()
    row= 0
    for i in mm:
        print(str(row)+ " " + i.replace("\n",""))
        row +=1
    print(" ")
    print("X,Y notation for each step ")
    print("Path: ", p)
if __name__ == '__main__':

    filename = sys.argv[1]
    f = open(filename, mode='r')

    MainGraph = []
    s_surface = []
    g_surface = []

    i = 0

    for line in iter(f.readline, ''):
        line = line.replace("\n", "")
        line = line.replace(" ", "")
        w = len(line)
        s = list(line[0:w])
        if 'S' in s:
            index = s.index('S')
            s_surface.append((i, index))
            if 'S' in s[index+1:]:
                index2 = s.index('S', index+1)
                s_surface.append((i, index2))
        elif 'G' in s:
            indexG = s.index('G')
            g_surface.append((i, indexG))
        MainGraph.append(s)
        i = i + 1

    f.close()

    if 1 == len(s_surface):
        start_node = Node(s_surface[0][0], s_surface[0][1])
    else:
        start_node = Node(s_surface[0][0], s_surface[0][1], s_surface[1][0], s_surface[1][1])

    g_node = Node(g_surface[0][0], g_surface[0][1])

    result,elapsedTime = ucs(MainGraph, start_node, g_node)

    path = []
    node = result
    while 0 != node.cost:
        path.append(node.x_y)
        if 0 != node.cost:
            node = node.parent
    path.append(node.x_y)

    path.reverse()
    print("*"*5 +"  Elapsed Time: "+ str(elapsedTime) + " seconds  " + "*"*5 )
    print("Start Point: " +str(s_surface)+ "  Goal Point: " + str(g_surface )+"\n")
    pretier(path)