def parse(lines: str) -> list[int]:
    return [int(line.strip()) for line in lines.splitlines()]

p1 = parse("""40
26
44
14
3
17
36
43
47
38
39
41
23
28
49
27
18
2
13
32
29
11
25
24
35""")

p2 = parse("""19
15
48
37
6
34
8
50
22
46
20
21
10
1
33
30
4
5
7
31
12
9
45
42
16""")

def won(who: str, p: list[int]) -> None:
    score = 0
    for i in range(1, len(p) + 1):
        score += i * p[len(p) - i]
    print(who, "won with", score)

round = 0
while True:
    # print(f"{p1=}")
    # print(f"{p2=}")
    # print("--")
    if round % 100 == 0:
        print(f"{round=}")
    round += 1

    if len(p1) == 0:
        won("p2", p2)
        break
    if len(p2) == 0:
        won("p1", p1)
        break
    p1c = p1.pop(0)
    p2c = p2.pop(0)
    if p1c > p2c:
        p1.append(p1c)
        p1.append(p2c)
    elif p1c < p2c:
        p2.append(p2c)
        p2.append(p1c)
    else:
        print("Tie")
        break