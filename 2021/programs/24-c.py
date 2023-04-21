# Assuming we need to hit every if-statement except the last...?
# 3rd digit can't be 9 or 4th target can't be hit

def run(input):
    w = z = 0

    def nextdigit():
        nonlocal input
        dig = int(input[0])
        input = input[1:]
        return dig


    w = nextdigit() # a
    z = (z * 26) + w + 4  # {a+4}

    w = nextdigit() # b
    z = (z * 26) + w + 16  # {a+4}{b+16}

    w = nextdigit() # c
    z = (z * 26) + w + 14 # {a+4}{b+16}{c+14}

    target = (z % 26) - 13  # = {c+1}
    z = z // 26             # = {a+4}{b+16}
    w = nextdigit() # d
    if (w != target):      # if d != c + 1
        z = (z * 26) + w + 3 

    # if d == c + 1 then z == {a+4}{b+16}

    w = nextdigit() # e
    z = (z * 26) + w + 11 # {a+4}{b+16}{e+11}

    w = nextdigit() # f
    z = (z * 26) + w + 13 # {a+4}{b+16}{e+11}{f+13}

    target = (z % 26) - 7 # f + 6
    z = z // 26           # {a+4}{b+16}{e+11}
    w = nextdigit() # g
    if (w != target):
        z = (z * 26) + w + 11

    # if g == f + 6 then z == {a+4}{b+16}{e+11}

    w = nextdigit() # h
    z = (z * 26) + w + 7  # {a+4}{b+16}{e+11}{h+7}

    target = (z % 26) - 12 # h - 5
    z = z // 26            # {a+4}{b+16}{e+11}
    w = nextdigit() # i
    if (w != target):
        z = (z * 26) + w + 12

    # if i == h - 5 then z == {a+4}{b+16}{e+11}

    w = nextdigit() # j
    z = (z * 26) + w + 15 # {a+4}{b+16}{e+11}{j+15}

    target = (z % 26) - 16 # j - 1
    z = z // 26            # {a+4}{b+16}{e+11}
    w = nextdigit() # k
    if (w != target):
        z = (z * 26) + w + 13

    # if k == j - 1 then z == {a+4}{b+16}{e+11}

    target = (z % 26) - 9 # e + 2
    z = z // 26           # {a+4}{b+16}
    w = nextdigit() # l
    if (w != target):
        z = (z * 26) + w + 1

    # if l == e + 2 then z == {a+4}{b+16}

    target = (z % 26) - 8 #  b + 8
    z = z // 26           # {a+4}
    w = nextdigit() # m
    if (w != target):
        z = (z * 26) + w + 15

    # if m == b + 8 then z == {a + 4}

    target = (z % 26) - 8   # a - 4
    z = z // 26             # 0
    w = nextdigit() # n
    if (w != target):
        z = (z * 26) + w + 4

    # if n == a - 4 then z == 0

    return z

def find_relations():
    divisors = [1, 1, 1, 26, 1, 1, 26, 1, 26, 1, 26, 26, 26, 26]
    added_to_x = [15, 14, 11, 13, 14, 15, -7, 10, -12, 15, -16, -9, -8, -8]
    added_to_y = [4, 16, 14, 3, 11, 13, 11, 7, 12, 15, 13, 1, 15, 4]
    stack = []
    result = []
    for i, divisor in enumerate(divisors):
        if divisor != 26:
            stack.append(i)
        else:
            prev_num = stack.pop()
            result.append((prev_num, i, added_to_y[prev_num] + added_to_x[i]))
    return result

print(find_relations())

# input = 99899999999999
# while "0" in str(input) or run(str(input)) != 0:
#     if input % 10000 == 111:
#         print(input)
#     input -= 1
# print(input)
