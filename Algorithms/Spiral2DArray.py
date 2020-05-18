"""
Write some code that can print out a spiral, 2D array. Some examples are shown below.

1

1 2
4 3

1 2 3
8 9 4
7 6 5

1  2  3  4
12 13 14 5
11 16 15 6
10 9  8  7

plus 11

so we go from 1 to n^2, inclusive.

"""
def create2DArray(n):
    arr = []
    for i in range(n):
        arr.append([])
    for j in range(n):
        for k in range(n):
            arr[j].append(0)
    leftToRight = True
    rightToLeft = False
    topToBottom = False
    bottomToTop = False
    rowIndex = 0
    colIndex = 0
    layer = 0
    for i in range(1,n*n+1):
        if leftToRight:
            arr[rowIndex][colIndex] = i
            colIndex += 1
            if colIndex == n or arr[rowIndex][colIndex] != 0:
                leftToRight = False
                topToBottom = True
                colIndex -= 1
                rowIndex += 1
        elif topToBottom:
            arr[rowIndex][colIndex] = i
            rowIndex += 1
            if rowIndex == n or arr[rowIndex][colIndex] != 0:
                topToBottom = False
                rightToLeft = True
                rowIndex -= 1
                colIndex -= 1
        elif rightToLeft:
            arr[rowIndex][colIndex] = i
            colIndex -= 1
            if colIndex < 0 or arr[rowIndex][colIndex] != 0:
                rightToLeft = False
                bottomToTop = True
                colIndex += 1
                rowIndex -= 1
        elif bottomToTop:
            arr[rowIndex][colIndex] = i
            rowIndex -= 1
            if arr[rowIndex][colIndex] != 0:
                bottomToTop = False
                leftToRight = True
                rowIndex += 1
                colIndex += 1
    for i in arr:
        print(" ".join(str(x) for x in i))

create2DArray(3)
print("----------------------")
create2DArray(4)
print("----------------------")
create2DArray(5)
