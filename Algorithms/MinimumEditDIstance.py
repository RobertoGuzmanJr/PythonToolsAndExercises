"""
This is a classic problem: find the minimum edit distance between two strings, where an edit can be an insert of a new
character, a delete of an existing character, or a modification of an existing character.

SOLUTION:

    "" a c e d f
""   0 1 2 3 4 5
a    1 0 1 2 3 4
b    2 1 1 2 3 4
c    3 2 1 2 3 4
d    4 3 2 2 2 3
e    5 4 3 2 3 3
f    6 5 4 3 3 3

The table above was filled in according to the following rule:

T[i][j] = min(T[i-1][j], T[i][j-1], T[i-1][j-1]) + (0 if s[i]==t[j] else 1)

"""
def MinimumEditDistance(s,t):
    m = len(s) + 1
    n = len(t) + 1

    #Initialize it.
    array = [[0 for y in range(n)] for x in range(m)]

    #Dynamic programming algorithm to fill in all values in the table.
    for i in range(m):
        for j in range(n):
            if i == 0:
                array[i][j] = j
            elif j == 0:
                array[i][j] = i
            else:
                array[i][j] = min(array[i][j-1],array[i-1][j-1],array[i-1][j]) + (0 if s[i-1] == t[j-1] else 1)
    return array[m-1][n-1]


print(MinimumEditDistance("abcdef","acedf"))
