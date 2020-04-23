"""
Varargs: Generalize the adder function you wrote in the last exercise to compute the sum of an arbitrary number of arguments, and change the calls
to pass more or fewer than two arguments. What type is the return value sum? What happens if you type in arguments of different type?
"""
def adder (*x):
    res = x[0]
    for s in x[1:]:
        res += s
    return res

print(adder('hi','there','how','are','you','?'))
print(adder([1,2,3],[3,4,5],[3,2,1],[1,1,1]))
print(adder(4.56,2.142,2.3))

print(adder("hi"))
print(adder([2,3,1]))
print(adder(3.24))

print(adder("hi",54,22,[1,2,3]))