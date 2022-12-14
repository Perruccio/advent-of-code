import time
def hourglass(obst, max_y, finish1=False, x=500, y=0):
    s = time.time()
    stone = len(obst)
    path = [(500,0)]
    while True:
        while True:
            if (x, y+1) not in obst:
                y += 1
            elif (x-1, y+1) not in obst:
                y += 1
                x -= 1 
            elif (x+1, y+1) not in obst:   
                y += 1
                x += 1 
            else:
                if y == max_y+1 and not finish1:
                    print(len(obst) - stone)     # Part 1 finish condition
                    finish1 = True
                obst.add((x,y))
                if (x,y) == (500,0):             # Part 2 finish condition
                    print(len(obst) - stone)                  
                    print(time.time() - s)
                    return
                path.pop()
                x,y = path[-1]
                break
            path.append((x,y))

obst = set()
import pathlib
for line in open(str(pathlib.Path(__file__).parent) + "/input.txt"):
    coords = line.split(" -> ")
    for c in range(len(coords)-1):
        x1, y1 = [int(xy) for xy in coords[c].split(",")]
        x2, y2 = [int(xy) for xy in coords[c+1].split(",")]

        s_x, big_x = sorted([x1, x2])
        s_y, big_y = sorted([y1, y2])

        if s_x == big_x:
            obst.update(set([(s_x, i) for i in range(s_y, big_y+1)]))
        elif s_y == big_y:
            obst.update(set([(i, s_y) for i in range(s_x, big_x+1)]))

max_y = max(y for x,y in obst)
obst.update(set((i, max_y+2) for i in range(490-(max_y),510+(max_y))))

new_obst = hourglass(obst, max_y)