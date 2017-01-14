class random(object):

    def __init__(self, seed=0):
        self.state = seed

    def random(self):
        self.state = self.state * 113 + 119
        return self.state

class roulette(object):
    def __init__(self, num_slot=39):
        self.num_slot = num_slot
        self.random = random(0)
        self.num = 0

    def play(self, num, bet):
        "return money you win"
        self.num = self.random.random() % self.num_slot
        res = bet * (self.num_slot-1) if self.num == num else 0
        return res

class game(object):
    def __init__(self, money=100, num_slot=39):
        self.money_init = money
        self.money = money
        self.num_slot = num_slot
        self.round = 0
        self.round_num = 0
        self.roulette = roulette(self.num_slot)

    def banner(self):
        return 'welcome to roulette!'

    def leave_msg(self):
        return 'thanks for playing, good bye'

    def report_msg(self):
        res = """\
*******************************************************************
game:      {game:3d}
you have: ${money:3d}
you won:  ${won:3d}
*******************************************************************
        """.format(game=self.round, money=self.money, won=self.money-self.money_init)
        return res

    def win_msg(self):
        return 'YES, you WIN!!!'

    def lose_msg(self):
        return 'OH NO, you LOSE!!!'

    def round_msg(self):
        return "IT IS %d" % self.round_num

    def check_num(self, num, err):
        "True: pass, False: failed with error message set in err"
        err = ""
        if num < 0 or num > self.num_slot:
            err = "wrong input: should be within 0 and %d" % self.num_slot
            return False
        return True

    def check_bet(self, bet, err):
        "True: pass, False: failed with error message set in err"
        err = ""
        if bet < 0 or bet > self.money:
            err = "wrong input: should be within 0 and %d" % self.money
            return False
        return True

    def play(self, num, bet):
        "True: win, False: lose"
        assert (bet <= self.money)
        self.money -= bet
        self.money += self.roulette.play(num, bet)
        self.round_num = self.roulette.num
        return self.round_num == num

def main():
    gm = game()
    print (gm.banner())
    while input('{:30}:  '.format("do you want to play(Y/N) ")).upper() == 'Y':
        err = ""
        money_you_bet = 0
        number_you_bet = 0
        while True:
            money_you_bet = eval(input("please input money you bet "))
            if gm.check_bet(money_you_bet, err):
                break
            print (err)
        while True:
            number_you_bet = eval(input("please input number you bet "))
            if gm.check_num(number_you_bet, err):
                break
            print (err)
        res = gm.play(number_you_bet, money_you_bet)
        print(gm.round_msg())
        if res:
            print(gm.win_msg())
        else:
            print(gm.lose_msg())
        print(gm.report_msg())

if __name__ == "__main__":
    main()
