#This comes from a Facebook interview preparation page. Given an integer,n, the idea is to print an n x n grid of spiraling numbers.
def spiral(n):
    #We begin by initializing everything to 0.
    arr = []
    for i in range(n):
        arr.append([])
    for j in arr:
        for i  in range(n):
            j.append(0)
    print(arr)

if __name__ == "__main__":
    spiral(3)
    spiral(4)

