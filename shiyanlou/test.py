list = [[1,2,3],[4,5,6],[7,8,9]]

l = [list(row) for row in zip(*list)]

print(l)