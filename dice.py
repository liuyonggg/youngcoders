def dice():
    print("This program will play dice 10 times start from the number you set")
    n = eval(input("Enter the first number you want to see, which must between 1 and 6: "))
    if n < 1 or n > 6:
        print ("Error: the number should be beween 1 and 6")
        return
    for i in range(10):
        res = n % 6
        if res == 0:
            res = 6
        print("the %dth round: %d" % (i, res))
        n = 13 * n + 17

dice()
