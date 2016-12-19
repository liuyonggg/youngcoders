money_you_have_beginning = 0
money_you_have = 0
money_you_bet = 0
game_you_played = 0
random_state = 0
NUM_SLOT = 39 

def get_random():
    global random_state
    random_state = random_state * 113 + 119
    return random_state

def run_roulette():
    return get_random() % NUM_SLOT

def bet_roulette():
    global money_you_bet
    money_you_bet = eval(input('{:30}:  '.format("please input money you bet")))
    num_bet =       eval(input('{:30}:  '.format("please input number you bet")))
    return num_bet

def report_roulette(win):
    global money_you_have_beginning
    global money_you_have
    global money_you_bet
    global game_you_played
    print ('*' * 80)
    print ('{:30}:  {:3d}'.format("game", game_you_played))
    print ('{:30}: ${:3d}'.format("you won", game_you_played))
    print ('{:30}: ${:3d}'.format("you have", money_you_have))
    print ('{:30}: ${:3d}'.format("you won totally", money_you_have - money_you_have_beginning))
    print ('*' * 80)
    

def play_roulette():
    global money_you_have_beginning
    global money_you_have
    global money_you_bet
    global game_you_played
    bet = bet_roulette()
    real = run_roulette()
    win = 0
    if bet == real:
        print ('{:30}: {:3d}'.format("YES, you WIN!!! it is ", bet))
        win = (NUM_SLOT-1) * money_you_bet
    else:
        print ('{:30}: {:3d}'.format("UH NO, you should bet on", real))
        win = -money_you_bet
    money_you_have += win
    money_you_bet = 0
    game_you_played += 1
    report_roulette(win)

def main():
    global money_you_have_beginning
    global money_you_have
    global money_you_bet
    global game_you_played
    global random_state
    money_you_have_beginning = money_you_have = 100

    print ('welcome to roulette!')
    while True:
        want_play = input('{:30}:  '.format("do you want to play(Y/N)"))
        want_play = want_play.upper()
        if want_play != 'Y':
            break
        play_roulette()
    print ('good luck, see you again')

if __name__ == '__main__':
    main()
