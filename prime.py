def is_prime(n):
    for i in range(2, n-1):
        if n % i == 0:
            return False
    return True

def test_prime():
    assert (is_prime(3))
    assert (not is_prime(4))
    assert (is_prime(13))
    assert (not is_prime(15))

def get_nth_prime(nth):
    p = 2
    number_of_prime = 0
    while True:
        if is_prime(p):
            number_of_prime += 1
            if number_of_prime == nth:
                break
        p += 1
    return p

def test_nth_prime():
    assert (get_nth_prime(1) == 2)
    assert (get_nth_prime(2) == 3)
    assert (get_nth_prime(3) == 5)
    assert (get_nth_prime(4) == 7)
    assert (get_nth_prime(100) == 541)


if __name__ == "__main__":
    test_prime()
    test_nth_prime()
    print ("finished")
