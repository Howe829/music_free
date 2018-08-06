list=[]

def fib(n):
    if n==1 or n ==0:
        return 1
    else:
     return fib(n-1)+fib(n-2)


for i in range (9):
    print(fib(i))