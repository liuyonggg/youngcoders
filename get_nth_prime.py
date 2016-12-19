from week1_lab import is_prime
def get_nth_prime(n):
    p = 2
    number_of_prime = 0
    res = 0
    while (True):
        if is_prime(p):
            res = p
            number_of_prime += 1
        if (number_of_prime == n):
            break
        p += 1
    return res

def test_nth_prime():
    assert (get_nth_prime(1) == 2)
    assert (get_nth_prime(2) == 3)
    assert (get_nth_prime(100) == 541)



