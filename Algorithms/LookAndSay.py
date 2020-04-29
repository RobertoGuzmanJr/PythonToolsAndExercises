def DetermineNextTerm(s):
    t = ""
    index = 0
    while index < len(s):
        value = s[index]
        numOfThem = 1
        index += 1
        while index < len(s) and s[index] == value:
            numOfThem += 1
            index += 1
        t += (str(numOfThem) + value)
    return t

def LookAndSay():
    numTerms = 11
    s = "1"

    for i in range(numTerms):
        print(s)
        s = DetermineNextTerm(s)

if __name__ == "__main__":
    LookAndSay()

