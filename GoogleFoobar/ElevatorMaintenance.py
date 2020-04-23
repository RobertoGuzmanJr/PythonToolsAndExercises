def solution(l):
    unsorted = list()

    #strategy is, for each word, to loop through each string and update variables based on what we see.
    #Then, we will be able to determine the values of each position,  the number of characters for each, etc.
    for i in range(0,len(l)):
        current_string = l[i]

        major_start = 0
        major_end = -1

        minor_start = -1
        minor_end = -1

        revision_start = -1
        revision_end = -1

        for c in range(0,len(current_string)):
            if current_string[c] == '.' and major_end == -1:
                major_end = c
                minor_start = c+1
            elif current_string[c] == '.' and minor_end == -1:
                minor_end = c
                revision_start = c+1
        #now, some cleanup.
        # if the major_end is still -1, it means that there are no decimals and the whole thing is a major.
        if major_end == -1:
            major_end = len(current_string)
        # if the minor start is larger than -1, and the minor end is -1, it means that the end of the minor is
        # the end of the string
        if minor_start > 0 and minor_end == -1:
            minor_end = len(current_string)
        # if revision_start is larger than -1, then we know the length of the string is revision end
        if revision_start > 0 and revision_end == -1:
            revision_end = len(current_string)

        #now we need to collect, for each component, the value and the length.
        #add the major term
        value = [[int(current_string[major_start:major_end]),major_end-major_start]]

        #add the minor term, if it exists.
        if minor_start > 0:
            value.append([int(current_string[minor_start:minor_end]),minor_end-minor_start])

        #add the revision term, if it exists.
        if revision_start > 0:
            value.append([int(current_string[revision_start:revision_end]),revision_end-revision_start])
        unsorted.append(value)
    return(unsorted)

print(solution(["1.0"]))