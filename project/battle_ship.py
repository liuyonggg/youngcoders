import random
random.seed(0)

ship_grid_user = None
attack_grid_user = None

ship_grid_pc = None
attack_grid_pc = None

def init_board():
    global ship_grid_user
    global attack_grid_user
    global ship_grid_pc
    global attack_grid_pc
    ship_grid_user = [\
                     [True, True, False, False, False, False, False, False, False], 
                     [True, True, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                    [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     ]
    attack_grid_user = [\
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 

                        ]
    ship_grid_pc = [\
                     [True, True, False, False, False, False, False, False, False], 
                     [True, True, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     ]
    attack_grid_pc = [\
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 
                     [False, False, False, False, False, False, False, False, False], 

                     ]


def display(ship, attack):
    i = 65
    print ("- 1 2 3 4 5 6 7 8 9")
    for s, a in zip(ship, attack):
        line = "%s " % chr(i)
        for s1, a1 in zip(s, a):
            if a1:
                if s1:
                    line += 'X '
                else:
                    line += 'O '
            else:
                line += '  '
        i += 1
        print (line)

def attack(coordinate, grid):
    assert(len(coordinate) == 2)
    grid[coordinate[0]][coordinate[1]] = True

def check_win(ship_grid, attack_grid):
    for i in range(len(ship_grid)):
        for j in range(len(ship_grid[0])):
            if ship_grid[i][j] == True and attack_grid[i][j] == False:
                return False
    return True

def strategy(grid):
    i = 0
    while True:
        coordinate = [random.randint(0, 8), random.randint(0, 8)]
        if not(grid[coordinate[0]][coordinate[1]]):
            return coordinate
        i += 1
        if i > 1000:
            assert(False)

def place_ship(ship_grid):
    coordinate = strategy(ship_grid)
    ship_grid[coordinate[0]][coordinate[1]] = True

def game_play():
    global attack_grid_user
    global attack_grid_pc
    global ship_grid_user
    global ship_grid_pc
    init_board()
    while True:
        cr = strategy(attack_grid_user)
        attack(cr, attack_grid_user)
        cr = strategy(attack_grid_pc)
        attack(cr, attack_grid_pc)
        pc_win = check_win(ship_grid_user, attack_grid_user)
        user_win = check_win(ship_grid_pc, attack_grid_pc)
        if user_win and pc_win:
            print ("Tie")
            return
        elif user_win:
            print ("user win")
            return
        elif pc_win:
            print ("pc win")
            return
        else:
            pass

def test_attack():
    global ship_grid_user
    global attack_grid_user
    global ship_grid_pc
    global attack_grid_pc
    init_board()
    attack([0, 0], attack_grid_user)
    attack([0, 1], attack_grid_user)
    attack([1, 0], attack_grid_user)
    attack([1, 1], attack_grid_user)
    attack([0, 0], attack_grid_pc)
    attack([0, 1], attack_grid_pc)
    attack([1, 0], attack_grid_pc)
    attack([1, 2], attack_grid_pc)
    display(ship_grid_user, attack_grid_user)
    print()
    display(ship_grid_pc, attack_grid_pc)
    print(check_win(ship_grid_user, attack_grid_user))
    print(check_win(ship_grid_pc, attack_grid_pc))

def test_check_win():
    global ship_grid_user
    global attack_grid_user
    global ship_grid_pc
    global attack_grid_pc
    init_board()
    assert(check_win(ship_grid_user, attack_grid_user) == False)
    attack([0, 0], attack_grid_user)
    attack([0, 1], attack_grid_user)
    attack([1, 0], attack_grid_user)
    attack([1, 1], attack_grid_user)
    assert(check_win(ship_grid_user, attack_grid_user) == True)

def test_strategy():
    global attack_grid_pc
    global attack_grid_user
    global ship_grid_user
    global ship_grid_pc
    init_board()
    for i in range(10):
        coordinate = strategy(attack_grid_pc)
        assert (attack_grid_pc[coordinate[0]][coordinate[1]] == False)
        attack(coordinate, attack_grid_pc)
    display(ship_grid_pc, attack_grid_pc)

def test_display():
    global attack_grid_pc
    global attack_grid_user
    global ship_grid_user
    global ship_grid_pc
    init_board()
    display(ship_grid_user, attack_grid_user)

def test_game_play():
    game_play()
    display(ship_grid_user, attack_grid_user)
    display(ship_grid_pc, attack_grid_pc)

#test_display()
#play()

#test_attack()
#test_check_win()
#test_strategy()

test_game_play()


