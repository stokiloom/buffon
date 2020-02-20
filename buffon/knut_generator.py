from time import time


def k1():
    global x
    tmp = str(int(x / 10 ** 9))
    tmpl = []
    for i in range(len(tmp)):
        tmpl.append(int(tmp[i]))
    return max(tmpl)


def k2():
    global x
    return ((x // 10 ** 8) % 10)


def k3():
    global x
    x = x + 5 * 10 ** 9 if x < 5 * 10 ** 9 else x


def k4():
    global x
    x = int(x * x // 10 ** 5) % 10 ** 10


def k5():
    global x
    x = (1001001001 * x) % 10 ** 10


def k6():
    global x
    x = x + 9814055677 if x < 10 ** 8 else 10 ** 10 - x


def k7():
    global x
    x = 10 ** 5 * (x % 10 ** 5) + x // 10 ** 5


def k8():
    k5()


def k9():
    global x
    x = int("".join([str(int(i) - (1 % (int(i) + 1))) for i in str(x)]))


def k10():
    global x
    x = x ** 2 + 99999 if x < 10 ** 5 else x - 99999


def k11():
    global x
    if x == 0:
        pass
    else:
        while x < 10 ** 9:
            x *= 10


def k12():
    global x
    x = (x * (x - 1) // 10 ** 5) % 10 ** 10


def k13():
    global y, z
    y -= 1
    z = k2() - 1


tmp = int(time())
"""
x = 6065038420
y = k1() + 1
z = k2()
switch = [None, k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13]
while y > 0:
    print(x)
    switch[z + 3]()
    z += 1
print(x)
"""
x = 0


def knut_generator(n, d, mode=1):
    if mode:
        file = open("knut.txt", 'a')
        print(' ', file=file)
    else:
        with open("knut.txt", 'r') as file:
            strfile = file.read().replace("\n", " ")
            a = list(map(int, strfile.split()))
            file.close()
            return a
    ans = []
    global x, y, z
    x = int(time() * 10 ** 10) % 10 ** 10
    switch = [None, k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13]
    for i in range(n):
        y = k1() + 1
        z = k2()
        while y > 0:
            switch[z + 3]()
            z += 1
        ans.append(x % (d + 1))
    print(*ans, file=file)
    file.close()
    return ans


if __name__ == "__main__":
    print(knut_generator(100, 100))
