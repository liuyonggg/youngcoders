random_state = 0
def get_random():
    global random_state
    random_state = random_state * 113 + 119
    return random_state

def shuffle(deck_of_cards):
    shuffled_deck = []
    while deck_of_cards:
        rand_card = get_random()%len(deck_of_cards)
        shuffled_deck.append(deck_of_cards.pop(rand_card))
    return shuffled_deck

def shuffle_2(deck_of_cards):
    num_of_cards = len(deck_of_cards)
    num_of_iterations = 3
    shuffled_deck = deck_of_cards
    for i in range(num_of_iterations):
        sub_deck_1 = shuffled_deck[:num_of_cards//2]
        sub_deck_2 = shuffled_deck[num_of_cards//2:]
        shuffled_deck = []
        while (sub_deck_1 and sub_deck_2):
            if get_random() % 2:
                shuffled_deck.append(sub_deck_1.pop())
            else:
                shuffled_deck.append(sub_deck_2.pop())
        shuffled_deck += sub_deck_1 + sub_deck_2
    return shuffled_deck
    

def sort_cards(deck_of_cards):
    sorted_deck = [0] * 13
    for x in deck_of_cards:
        sorted_deck[x-1] = x
    return sorted_deck

def test_random():
    global random_state
    random_state = 0
    print (get_random(), get_random())
    

def test_shuffle():
    global random_state
    random_state = 0
    deck_of_cards = list(range(1, 14))
    shuffled_deck = shuffle(deck_of_cards)
    print (shuffled_deck)


def test_shuffle_2():
    global random_state
    random_state = 0
    deck_of_cards = list(range(1, 14))
    shuffled_deck = shuffle_2(deck_of_cards)
    print (shuffled_deck)

def test_sort():
    deck_of_cards = list(range(1, 14))
    shuffled_deck = shuffle(deck_of_cards)
    print ('deck after shuffle: ', shuffled_deck)
    sorted_deck = sort_cards(shuffled_deck)
    print ('deck after sort   : ', sorted_deck)

if __name__ == '__main__':
    test_random()
    test_shuffle()
    test_shuffle_2()
    test_sort()
