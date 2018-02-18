from AStar import *
import bottle
import copy
import math
import os
import sys

SNEK_BUFFER = 3

SNAKE = 1
WALL = 2
SAFTEY = 3

FOOD = 5
GOLD = 7

grid = []
otherSnakes = []
allSnakes = []
mySnake = ''
width = 0
height = 0
myHealth = 100
mySnakeId = ''

def init(postData):
    global width
    global height
    global grid 
    global otherSnakes
    global mySnake
    global myHealth
    global mySnakeId
    
    data = postData

    width = data['width']
    height = data['height']
    mySnakeId = data['you']['id']

    grid = [[0 for col in xrange(height)] for row in xrange(width)]
    allSnakes = data['snakes']
    foods= data['food']['data']
    for snake in allSnakes:
        print('ID=', mySnakeId)
        print('SNAKE=', snake)
        if snake['id'] == mySnakeId:
            mySnake = snake
            print('My snake is ', mySnake)
        else:
            otherSnakes.append(snake)

        snakeCoords = []
        for coord in snake['body']['data']:
            grid[coord['x']][coord['y']] = SNAKE
            snakeCoords.append([coord['x'],coord['y']])
        snek['coords'] = snakeCoords

    for food in foods:
        #if(snek['health'] < 40):
        grid[food['x']][food['y']] = FOOD

        #else:
        #    grid[food['x'] - 1][food['y'] - 1] = FOOD + 1
        #    grid[food['x'] - 1][food['y'] + 1] = FOOD + 1
        #    grid[food['x'] + 1][food['y'] - 1] = FOOD + 1
        #    grid[food['x'] + 1][food['y'] + 1] = FOOD + 1

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    print('WORKING ON GET REQUEST')
    head_url = '%s://%s/static/Traitor.gif' % (bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc)
    return {
        'color': '#ff0000',
        'head': head_url
    }

@bottle.post('//start')
def start():
    print('WORKING ON START REQUEST')
    return {
        'name': 'RomanInitial',
        'color': '#FF0000',
        'head_type': 'fang',
        'tail_type': 'round-bum',
        'taunt': 'battlesnake-python!',
        'secondary_color': '#FF00FF'
    }

@bottle.post('//move')
def move():
    global width
    global height
    global data
    global mySnake
    global mySnakeId

    print('WORKING ON MOVE REQUEST')
    postData = bottle.request.json
    init(postData)
    ID = snek['id']
    ourHealth = snek['health']
    for enemy in otherSnakes:
        #if (enemy['id'] == ID):
        #    ourHealth = enemy['health']
        #    continue
              
        #print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
        #grid[enemy['coords'][0][0]*2-enemy['coords'][1][0]][enemy['coords'][0][1]*2
        #- enemy['coords'][1][1]] = GOLD
        #data['gold'].append([enemy['coords'][0][0]*2 -
        #enemy['coords'][1][0],enemy['coords'][0][1]*2 -
        #enemy['coords'][1][1]])

   
        #if distance(snek['coords'][0], enemy['coords'][0]) > SNEK_BUFFER:
        #    continue

       
        if (enemy['length'] >= snek['length'] - 1):
            #dodge
            try:
                if enemy['coords'][0][1] < data['height'] - 1:
                    grid[enemy['coords'][0][0]][enemy['coords'][0][1] + 1] = SAFTEY             
                if enemy['coords'][0][1] > 0:
                    grid[enemy['coords'][0][0]][enemy['coords'][0][1] - 1] = SAFTEY
                if enemy['coords'][0][0] < data['width'] - 1:
                    grid[enemy['coords'][0][0] + 1][enemy['coords'][0][1]] = SAFTEY
                if enemy['coords'][0][0] > 0:
                    grid[enemy['coords'][0][0] - 1][enemy['coords'][0][1]] = SAFTEY
            except:
                pass    
            try:
                grid[enemy['coords'][0][0]][enemy['coords'][0][1]] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0]][enemy['coords'][0][1] + 1] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0]][enemy['coords'][0][1] - 1] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0] + 1][enemy['coords'][0][1]] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0] - 1][enemy['coords'][0][1]] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0] + 1][enemy['coords'][0][1] + 1] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0] - 1][enemy['coords'][0][1] - 1] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0] + 1][enemy['coords'][0][1] - 1] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0] - 1][enemy['coords'][0][1] + 1] = SAFTEY
            except:
                pass
            grid[enemy['coords'][1][0]][enemy['coords'][1][1]] = 1
            grid[enemy['coords'][0][0]][enemy['coords'][0][1]] = 1
            
            #for cords in enemy['coords']:
             #   x=cords[0]
              #  y=cords[1]
               # try:
               #     grid[x-1][y] = SAFTEY
               # except:
               #     pass
               # try:
               #     grid[x+1][y] = SAFTEY
               # except:
               #     pass
               # try:
               #     grid[x][y-1] = SAFTEY
               # except:
               #     pass
               # try:
               #     grid[x][y+1] = SAFTEY
               # except:
               #     pass

            

    #print('grid is ',grid)
    snek_head = snek['coords'][0]
    #print('snekHead is ', snek['coords'][0])
    #print('snek head makred as ',
    #grid[snek['coords'][0][0]][snek['coords'][0][1]])
    snek_neck = snek['coords'][1]
    snek_coords = snek['coords']
    print('snake coords are ', snek_coords)
    path = None
    middle = [data['width'] / 2, data['height'] / 2]
    #foods = sorted(data['food'], key = lambda p: distance(p,snek_head ))
    #golds = sorted(data['gold'], key = lambda p: distance(p,snek_head ))

    bestScore = 4
    if (ourHealth > 100):
        bestScore = 10
        
    bestGoals = []
    print('best goals are',bestGoals)
    #print grid
    for col in xrange(data['height']):
        for row in xrange(data['width']):
            if grid[row][col] > bestScore:
                bestScore = grid[row][col]
                
    for col in xrange(data['height']):
        for row in xrange(data['width']):
            if grid[row][col] == bestScore:
                bestGoals.append([row,col])
                
    #print "BS",bestScore
    #print "BG",bestGoals
    
    ##print foods
    #if data['mode'] == 'advanced':
        #foods = data['gold'] + foods #+ heads
        #print("")
    foods = sorted(bestGoals, key = lambda p: distance(p,snek_head))
    print('best goals are ', foods)
        
    for food in foods:
        if food in snek_coords:
            print('DANGER_DANGER')
            print('DANGER FOOD ', food)
            #grid[food[0]],[food[1]]=SNAKE
            continue
        ##print food
        tentative_path = a_star(snek_head, food, grid, snek_coords)
        print('SNEK HEAD ',snek_head)
        print('SNEK COORDS',snek_coords)
        if not tentative_path:
            print('no path to food')
            continue

        print('for food ', food)
        print('temporary path is ', tentative_path)
        
        path_length = len(tentative_path)
        snek_length = len(snek_coords) + 1
        print('this path has length is ', path_length)
        #dead = False
        #for enemy in data['snakes']:
        #    if enemy['id'] == ID:
        #        continue
        #    if path_length > distance(enemy['coords'][0], food):
        #        dead = True
        #if dead:
        #    continue

        # Update snek
        print('after path length 0')
        print('path length is ', path_length)
        print('snek length is ', snek_length)
        if path_length < snek_length:
            remainder = snek_length - path_length
            new_snek_coords = list(reversed(tentative_path)) + snek_coords[:remainder]
        else:
            new_snek_coords = list(reversed(tentative_path))[:snek_length]

        if grid[new_snek_coords[0][0]][new_snek_coords[0][1]] == FOOD:
            # we ate food so we grow
            new_snek_coords.append(new_snek_coords[-1])

        # Create a new grid with the updates snek positions
        new_grid = copy.deepcopy(grid)

        for coord in snek_coords:
            new_grid[coord[0]][coord[1]] = 0
        for coord in new_snek_coords:
            new_grid[coord[0]][coord[1]] = SNAKE

        ##printg(grid, 'orig')
        ##printg(new_grid, 'new')

        ##print snek['coords'][-1]
        foodtotail = a_star(food,new_snek_coords[-1],new_grid, new_snek_coords)
        if foodtotail:
            path = tentative_path
            print('Before break')
            break
        ##print "no path to tail from food"

    ##print grid
    print('path before if ',path)
    if not path:

        path = a_star(snek_head, snek['coords'][-1], grid, snek_coords)
    print('path after if ',path)

    despair = not (path and len(path) > 1)
    print('despair first time', despair)

    if despair:
        for neighbour in neighbours(snek_head,grid,0,snek_coords, [1,2,3]):
            path = a_star(snek_head, neighbour, grid, snek_coords)
            print('i\'m scared')
            break

    despair = not (path and len(path) > 1)

    print('despair second time time', despair)
    if despair:
        for neighbour in neighbours(snek_head,grid,0,snek_coords, [1,2]):
            path = a_star(snek_head, neighbour, grid, snek_coords)
            print('like so scared')
            break

    print('path before asserts ', path)
    if path:
        assert path[0] == tuple(snek_head)
        assert len(path) > 1

    print('path after asserts ', path)
    #print(grid)
    moveTo = ''
    try:
        print('try move to')
        moveTo = direction(path[0], path[1])
        
    except:
        try:
            if (grid[snek['coords'][0][0] + 1][snek['coords'][0][1]] != 1):
                moveTo = "right"
        except:
            pass
        try:
            if (grid[snek['coords'][0][0] - 1][snek['coords'][0][1]] != 1):
                moveTo = "left"
        
        except:
            pass
        try:
            if (grid[snek['coords'][0][0]][snek['coords'][0][1] + 1] != 1):
                moveTo = "down"
        except:
            pass
        try:
            if (grid[snek['coords'][0][0]][snek['coords'][0][1] - 1] != 1):
                moveTo = "up"
        except:
            pass
        print('move to ',moveTo)
    return {
        'move': moveTo,
        'taunt': 'Whatever'
    }
    

@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'amen!'
    }

def distance(p, q):
    dx = abs(p[0] - q[0])
    dy = abs(p[1] - q[1])
    return dx + dy

def closest(items, start):
    closest_item = None
    closest_distance = 10000

    # TODO: use builtin min for speed up
    for item in items:
        item_distance = distance(start, item)
        if item_distance < closest_distance:
            closest_item = item
            closest_distance = item_distance

    return closest_item

def direction(from_cell, to_cell):
    dx = to_cell[0] - from_cell[0]
    dy = to_cell[1] - from_cell[1]
    #print ('FROM CELL ',from_cell)
    #print ('TO CELL ',to_cell)
    #print ('DX=',dx, ' DY= ',dy)
    if dx == 1:
        print('RIGHT')
        return 'right'
    elif dx == -1:
        print('LEFT')
        return 'left'
    elif dy == -1:
        print('UP')
        return 'up'
    elif dy == 1:
        print('DOWN')
        return 'down'

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
