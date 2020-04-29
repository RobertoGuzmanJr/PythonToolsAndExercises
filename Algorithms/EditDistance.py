def OneEditApart(s,t):
    if abs(len(s) - len(t)) <= 1:
        numDifferences = 0
        if len(s) == len(t):
            for i in range(len(s)):
                if s[i] != t[i]:
                    numDifferences += 1
                if numDifferences > 1:
                    return False
            if numDifferences == 1:
                return True
            else:
                return False
        else:
            a = s if len(s) > len(t) else t
            b = t if a == s else s
            for j in range(len(b)):
                if b[j] != a[j] and b[j] != a[j+1]:
                    return False
                elif b[j] != a[j]:
                    numDifferences += 1
                if numDifferences > 1:
                    return False
            if numDifferences == 1:
                return True
            else:
                return False
    else:
        return False

if __name__ == '__main__':
    print(OneEditApart('Hi there','Hi there'))
    print(OneEditApart('XXYX','XXZX'))
    print(OneEditApart('XXXX','XXXX'))
    print(OneEditApart('good','bad'))