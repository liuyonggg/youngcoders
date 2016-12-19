def dice():
    print ("This program will play dice 10 times start from the number you set")
    n = eval(input("Enter the first number you want to see, which must between 1 and 6: "))
    if n < 1 or n > 6:
        print ("Error: the number should be beween 1 and 6")
        return
    for i in range(10):
        print ("the round %d: value is %d" %(i, n%6))
        n = 13*n + 17;



def is_prime(n): 
	for i in range(2, n): 
		if n % i == 0: 
			return False 
	return True
 
def test_all_prime():
	n = input("Enter a number: ") 
	for x in range(2, int(n)): 
		if is_prime(x): 
			print(x, " is prime") 
		else: 
			print(x, " is not prime") 

x = 10
def test_local():
	y = 11
	print ("local environment:", locals())
	print ("global environment:", globals())

#test_local()

def file_test():
	f = open('a.txt', 'w')  # mode: r read w write b binary
	f.write('hello\n')
	f.close()
	f = open('a.txt', 'a')  # mode: r read w write b binary
	f.write('world')
	f.close()
	f = open('a.txt', 'r')  # mode: r read w write b binary
	l = f.readlines() 
	f.close()
	return l

#print (file_test())

