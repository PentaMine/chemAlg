l = []
while True:
    i = input().split(" ")
    if len(i) == 1:
        break
    l.append(i)
    print(i, l)


for i in l:
    print(f"{i[0]} \t{i[1]}")