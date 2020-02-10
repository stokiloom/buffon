l = list(map(int, input().split()))
k = 0
i = -1
while k < len(l):
    if l[k] == 0 and i == -1:
        i = k
    elif l[k] and i > -1:
        l[k], l[i] = l[i], l[k]
        k = i
        i = -1
    k +=1
print(l)