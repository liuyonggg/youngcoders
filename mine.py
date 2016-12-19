def find_mine(spaces):
    res = 0
    for i in range(len(spaces)):
        for j in range(len(spaces[0])):
            if spaces[i][j] == 1:
                print('found and destroyed mine in (%d, %d)' % (i, j))   
                res += 1
    return res

def test_find_mine():
    spaces = [[0, 0, 1], [0, 0, 0], [1, 1, 0]]
    assert (find_mine(spaces) == 3)

test_find_mine()
