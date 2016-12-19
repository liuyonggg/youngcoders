def calculate_sum(numbers):
    ret = 0
    for x in numbers:
        ret += x # ret = ret + x
    return ret

def test_sum():
    numbers = [1, 2, 3]
    s = calculate_sum(numbers)
    assert(s == 6)

def test_big_sum():
    numbers = list(range(100000+1))
    s = calculate_sum(numbers)
    assert(s == 5000050000)

if __name__ == '__main__':
    test_sum()
    test_big_sum()
