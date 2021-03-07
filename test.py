from time import perf_counter

t0 = perf_counter()

rows = 5
cols = 7
board = [[0]*9]
ans = []

def pprint(life):
    for row in life:
        for item in row:
            print(item, end=" ")
        print("")
    print("")

def count(life):
    out = 0
    for row in life:
        out += sum(row)
    return out

def iterate(life):
    newlife = []
    deaths = []
    for rownum in range(1,6):
        for colnum in range(1,8):
            surround = 0 - life[rownum][colnum]
            for a in range(rownum-1, rownum + 2):
                for b in range(colnum-1, colnum + 2):
                    surround += life[a][b]

            if life[rownum][colnum] == 0 and surround == 3:
                newlife.append([rownum,colnum])
            elif life[rownum][colnum] == 1 and surround != 3:
                deaths.append([rownum,colnum])

    for death in deaths:
        life[death[0]][death[1]] = 0
    for birth in newlife:
        life[birth[0]][birth[1]] = 1
    return life

for i in range(rows):
    row = []
    row.append(0)
    for element in input():
        if element == "-":
            row.append(0)
        elif element == "X":
            row.append(1)
    row.append(0)
    board.append(row)
board.append([0]*9)


for i in range(5):
    # pprint(board)
    board = iterate(board)
    ans.append(count(board))

for a in ans:
    print(a, end=" ")

print("")
tf = perf_counter() - t0
print(tf, "seconds")
