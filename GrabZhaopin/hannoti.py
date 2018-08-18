

def hannoti(A,B,C,n):
    if n==1:
        print(A+'->'+C)
    else:
        hannoti(A,C,B,n-1)
        print(A+'->'+C)
        hannoti(B,A,C,n-1)


hannoti('a','b','c',3)
