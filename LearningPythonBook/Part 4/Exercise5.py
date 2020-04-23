"""
Write a function called copyDict(dict) that copies its dictionary arugment. It should return a new dictionary
containing all of the items in its argument. Use the dictonary keys method to iterate. Copying sequences is easy,
since x[:] will do it; is that also true of dictionaries?
"""
def copyDict(dict):
    res = {}
    for key in dict.keys():
        res[key] = dict[key]
    return res


dic = {'a': 1, 'b': 2, 'c': 3}

print(copyDict(dic))

