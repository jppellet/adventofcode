from utils import *
from sys import exit


# OPEN, CLOSE = "([{<", ")]}>"
DELIMS = {
    "(" : ")",
    "[" : "]",
    "{" : "}",
    "<" : ">",
}
CORRUPT_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
COMPLETION_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


SAMPLE = False
data = read_lines(input_for(__file__, SAMPLE), str)

syntax_score = 0
completion_scores = []

for line in data:
    stack = []

    # Part 1

    for c in line:
        if c in DELIMS:
            stack.append(c)
        else:
            expected = DELIMS[stack.pop()]
            if expected != c:
                syntax_score += CORRUPT_POINTS[c]
                break

    # Part 2

    else: # incomplete line
        compl_score = 0
        for c in reversed(stack):
            compl_score *= 5
            compl_score += COMPLETION_POINTS[DELIMS[c]]
        completion_scores.append(compl_score)
        

# 1
print(syntax_score)

# 2
completion_scores.sort()
print(completion_scores[len(completion_scores) // 2])