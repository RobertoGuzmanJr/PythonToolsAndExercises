"""
This is a classic problem. The idea is that you have two strings, s and t. You want to return the largest substring
that is common to both. To solve this problem, we use dynamic programming as follows.

SOLUTION:

   q p t g b a c
a  0 0 0 0 0 1 0
b  0 0 0 0 1 0 0
b  0 0 0 0 1 0 0
a  0 0 0 0 0 2 0
c  0 0 0 0 0 0 3
c  0 0 0 0 0 0 1

For this one, the key is to check the value of the two characters for the string s and t and then add one to the diagonal
entry if they agree and 0 otherwise.

"""
def LargestCommonSubstring(s,t):
    m = len(s)
    n = len(t)

    #Initialize it.
    array = [[0 for y in range(n)] for x in range(m)]

    maxValue = 0
    max_i = -1
    max_j = -1

    #Now fill in the table using dynamic programming.
    for i in range(m):
        for j in range(n):
            value = 0
            if 0 in [i,j]:
                value = 1 if s[i] == t[j] else 0
            else:
                value = 0 if s[i] != t[j] else array[i-1][j-1] + 1
            if value > maxValue:
                maxValue = value
                max_i - i
                max_j = j
            array[i][j] = value
    print("The maximum length of the common substring is {0}.".format(maxValue))
    print("The maximum length substring is: {0}".format(t[max_j-maxValue+1:max_j+1]))
    #print(array)

print(LargestCommonSubstring("qptgbac","abbacc"))
print(LargestCommonSubstring("the ghost is in the pantry.","the ghast is in this pantry."))
