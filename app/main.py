from AStar import *
from operator import itemgetter

import bottle
import copy
import math
import os
import sys

SNEK_BUFFER = 3

MODE ='foodguard'

EMPTY =0

SNAKE = 1
WALL = 2
SAFTEY = 3

FOOD = 5
GOLD = 7

grid = []
otherSnakes = []
allSnakes = []
foods=[]
goals=[]
mySnake = ''
width = 0
height = 0
myHealth = 100
myLength =1
mySnakeId = ''
#mode='foodeater'
mode='foodguard'

def init(postData):
    global width
    global height
    global grid 
    global otherSnakes
    global mySnake
    global myHealth
    global mySnakeId
    global foods
    global goals
    global mode
    global myLength

    data = postData

    width = data['width']
    height = data['height']
    mySnakeId = data['you']['id']
    grid = [[0 for col in xrange(height)] for row in xrange(width)]
    allSnakes = data['snakes']['data']
    otherSnakes =[]
    foods=[]

    foodData = data['food']['data']
    for snake in allSnakes:
        #print('ID=', mySnakeId)
        #print('SNAKE=', snake)
        if snake['id'] == mySnakeId:
            mySnake = snake
            myLength =int(mySnake['length'])
            myHealth =int(mySnake['health'])
        else:
            otherSnakes.append(snake)

        snakeCoords = []
        for coord in snake['body']['data']:
            grid[coord['x']][coord['y']] = SNAKE
            snakeCoords.append([coord['x'],coord['y']])
        snake['coords'] = snakeCoords
 

    print ('FOOD DATA ', foodData)
    for food in foodData:
        foods.append(food)

    #print ('GRID ', grid)

    createGoals()

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

def createGoals():
    global width
    global height
    global goals
    global mode
    global foods
    global myLength
    global myHealth

    goals=[]


    if mode=='foodeater':
        safetyAroundSnakeHead()
        for food in foods:
            print('Check food vs grid ', grid[food['x']][food['y']])
            if(int(grid[food['x']][food['y']])==0):
                goals.append({'x':food['x'],'y':food['y'],'score':4})

    elif mode=='foodguard':
        print('Foodguard mode initiated')
        print('GOALS ', goals)
        #print('len(otherSnakes)==1 and int((otherSnakes[0])[length]) < myLength ',len(otherSnakes), ' ',int((otherSnakes[0])['length']), ' ', myLength)
        if(len(otherSnakes)==1 and int((otherSnakes[0])['length']) < myLength and int((otherSnakes[0])['health']) < myHealth and myHealth>20):
            print("HERE WE GO")
            for food in foods:
                try:
                    if(int(grid[food['x']+1][food['y']+1])==0):
                        goals.append({'x':food['x']+1,'y':food['y']+1,'score':4})
                    if(int(grid[food['x']+1][food['y']-1])==0):
                        goals.append({'x':food['x']+1,'y':food['y']-1,'score':4})
                    if(int(grid[food['x']-1][food['y']+1])==0):
                        goals.append({'x':food['x']-1,'y':food['y']+1,'score':4})
                    if(int(grid[food['x']-1][food['y']-1])==0):
                        goals.append({'x':food['x']-1,'y':food['y']-1,'score':4})
                    print('GOALS ', goals)
                except:
                    pass
        else:
            safetyAroundSnakeHead()
            for food in foods:               
                print('Check food vs grid ', grid[food['x']][food['y']])
                if(int(grid[food['x']][food['y']])==0):
                    goals.append({'x':food['x'],'y':food['y'],'score':4})

    print('mySnake coords', mySnake['coords'])


    goals = sorted(goals, key = lambda p: distance(p,mySnake['coords'][0]))
    print('GOALS SORTED', goals)

#def reassesGrid():
#    global foods
#    for food in foods:
#       try:
#            grid[food['x'] - 1][food['y'] - 1] = FOOD 
#            grid[food['x'] - 1][food['y'] + 1] = FOOD 
#            grid[food['x'] + 1][food['y'] - 1] = FOOD 
#            grid[food['x'] + 1][food['y'] + 1] = FOOD 
#            grid[food['x']][food['y']] = EMPTY
#        except:
#            pass
    
def getGoalCoords():
    global goals
    goalCoords=[]
    for goal in goals:
        print('GOAL COORDS ', goal, ' ',goal['x'])
        goalCoords.append([goal['x'],goal['y']])
    return goalCoords

def safetyAroundSnakeHead():
    global otherSnakes
    global grid
    global myLength

    print('other snakes = ', otherSnakes)
    for otherSnake in otherSnakes:
        print('other snake length = ', int(otherSnake['length']), ' my length ', myLength)
        print('condition= ', int(otherSnake['length']) >= myLength )
        if (int(otherSnake['length']) >= myLength ):
            #dodge head  
            try:
                grid[otherSnake['coords'][0][0]][otherSnake['coords'][0][1] + 1] = SAFTEY
                print('grid safety point ', [otherSnake['coords'][0][0]],' ', [otherSnake['coords'][0][1] + 1] , ' = ', grid[otherSnake['coords'][0][0]][otherSnake['coords'][0][1] + 1])
            except:
                pass
            try:
                grid[otherSnake['coords'][0][0]][otherSnake['coords'][0][1] - 1] = SAFTEY
            except:
                pass
            try:
                grid[otherSnake['coords'][0][0] + 1][otherSnake['coords'][0][1]] = SAFTEY
            except:
                pass
            try:
                grid[otherSnake['coords'][0][0] - 1][otherSnake['coords'][0][1]] = SAFTEY
            except:
                pass
            try:
                grid[otherSnake['coords'][0][0] + 1][otherSnake['coords'][0][1] + 1] = SAFTEY
            except:
                pass
            try:
                grid[otherSnake['coords'][0][0] - 1][otherSnake['coords'][0][1] - 1] = SAFTEY
            except:
                pass
            try:
                grid[otherSnake['coords'][0][0] + 1][otherSnake['coords'][0][1] - 1] = SAFTEY
            except:
                pass
            try:
                grid[otherSnake['coords'][0][0] - 1][otherSnake['coords'][0][1] + 1] = SAFTEY
            except:
                pass
            grid[otherSnake['coords'][1][0]][otherSnake['coords'][1][1]]=SNAKE

@bottle.get('/')
def index():
    print('WORKING ON GET REQUEST')
    head_url = '%s://%s/static/Traitor.gif' % (bottle.request.urlparts.scheme, bottle.request.urlparts.netloc)
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
    global myLength
    global foods
    global grid
    global goals

    print('WORKING ON MOVE REQUEST')
    postData = bottle.request.json
    grid=[]
    init(postData)

            
    mySnake_head = mySnake['coords'][0]
    mySnake_coords = mySnake['coords']
    print('my snake coords are ', mySnake_coords)
    path = None

    #goals = sorted(goals, key=itemgetter('score'))
    

    for goal in goals:
        tentative_path = a_star(mySnake_head, [goal['x'],goal['y']], grid, mySnake_coords)
        if not tentative_path:
            print('no path to goal')
            continue

        print('for goal ', goal)
        print('temporary path is ', tentative_path)
        
        path_length = len(tentative_path)
        print('this path has length is ', path_length)
        # Update snake
        print('path length is ', path_length)
        print('mySnake length is ', myLength)
        if path_length < myLength:
            remainder = myLength - path_length
            new_mySnake_coords = list(reversed(tentative_path)) + mySnake_coords[:remainder]
        else:
            new_mySnake_coords = list(reversed(tentative_path))[:myLength]

        if grid[new_mySnake_coords[0][0]][new_mySnake_coords[0][1]] == goal:
            # we ate goal so we grow
            new_mySnake_coords.append(new_mySnake_coords[-1])

        # Create a new grid with the updates mySnake positions
        new_grid = copy.deepcopy(grid)

        for coord in mySnake_coords:
            new_grid[coord[0]][coord[1]] = 0
        for coord in new_mySnake_coords:
            new_grid[coord[0]][coord[1]] = SNAKE

        goaltotail = a_star([goal['x'],goal['y']],new_mySnake_coords[-1],new_grid, new_mySnake_coords)
        if goaltotail:
            path = tentative_path
            print('Before break')
            break

    print('path before if ',path)
    if not path:
        path = a_star(mySnake_head, mySnake['coords'][-1], grid, mySnake_coords)
    print('path after if ',path)

    despair = not (path and len(path) > 1)
    print('despair first time', despair)

    if despair:
        for neighbour in neighbours(mySnake_head,grid,0,mySnake_coords, [1,2,3]):
            path = a_star(mySnake_head, neighbour, grid, mySnake_coords)
            print('i\'m scared')
            break

    despair = not (path and len(path) > 1)

    print('despair second time time', despair)
    if despair:
        for neighbour in neighbours(mySnake_head,grid,0,mySnake_coords, [1,2]):
            path = a_star(mySnake_head, neighbour, grid, mySnake_coords)
            print('like so scared')
            break

    print('path before asserts ', path)
    if path:
        assert path[0] == tuple(mySnake_head)
        assert len(path) > 1

    print('path after asserts ', path)
    #print(grid)
    moveTo = ''
    try:
        print('try move to')
        moveTo = direction(path[0], path[1])
        
    except:
        try:
            if (grid[mySnake['coords'][0][0] + 1][mySnake['coords'][0][1]] != 1):
                moveTo = "right"
        except:
            pass
        try:
            if (grid[mySnake['coords'][0][0] - 1][mySnake['coords'][0][1]] != 1):
                moveTo = "left"
        
        except:
            pass
        try:
            if (grid[mySnake['coords'][0][0]][mySnake['coords'][0][1] + 1] != 1):
                moveTo = "down"
        except:
            pass
        try:
            if (grid[mySnake['coords'][0][0]][mySnake['coords'][0][1] - 1] != 1):
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
    return {
        'taunt': 'amen!'
    }

def distance(p, q):
    dx = abs(p['x'] - q[0])
    dy = abs(p['y'] - q[1])
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
