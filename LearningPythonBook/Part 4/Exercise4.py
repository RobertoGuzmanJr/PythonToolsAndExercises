"""
Keywords: Change the adder function from exercise 2 to accept and sum/concatenate three arguments: def adder(good, bad, ugly).
Now, provide default values for each argument, and experiment with calling the function interactively. Try passing in one, two or three
arguments. Then try passing in keyword arguments. Does the call adder(good = 2, ugly = 1) work? Why? Finally, generalize the new adder to
accept and sum/concatenate an arbitrary number of keyword arguments.
"""

def adder (good = 1, bad = 2, ugly = 3):
    return good + bad + ugly

print(adder(4))
print(adder(4,5))
print(adder(4,5,6))
print(adder(ugly = 1, good=2))

def adder_gen (**kargs):
    x = list(kargs.values())[0]
    for key in list(kargs.keys())[1:]:
        x += kargs[key]
    return x

print(adder_gen(ghost = 1, goblin = 2, spirit = 32))