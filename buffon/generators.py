from random import randint, shuffle
from math import sin, cos, pi
from time import time, sleep
from tkinter import *
from collections import Counter
from quantumrandom import get_data
from os import urandom
from knut_generator import knut_generator


def os_generator(n, d=1000, mode=1):
    tg = time()
    if mode:
        file = open("osgen.txt", 'a')
        print(' ', file=file)
    else:
        with open("osgen.txt", 'r') as file:
            strfile = file.read().replace("\n", " ")
            a = list(map(int, strfile.split()))
            file.close()
            return a
    a = [0] * n
    for i in range(n):
        a[i] = int(urandom(3).hex(), 16) % (d + 1)
    print('time: ', round(time() - tg, 3))
    print(*a, file=file)
    file.close()
    return a


def rand_generator(n, d=1000, mode=1):
    tg = time()
    if mode:
        file = open("randgen.txt", 'a')
        print(' ', file=file)
    else:
        with open("randgen.txt", 'r') as file:
            strfile = file.read().replace("\n", " ")
            a = list(map(int, strfile.split()))
            file.close()
            return a
    a = [0] * n
    for i in range(n):
        a[i] = randint(0, d)
    print('time: ', round(time() - tg, 3))
    print(*a, file=file)
    file.close()
    return a


def pi_buffon(a, n, d=1000, r=1, l=1):
    p = 0
    for i in range(0, n - 1, 2):
        y = a[i]
        alpha = a[i + 1]
        if l - r:
            if y * r <= l * d * sin((alpha * pi) / d):
                p += 1
        else:
            if y <= int(d * sin((alpha / d) * pi)):
                p += 1
    if p:
        return (n * l) / (p * r)
    else:
        return 0


def hit_or_miss(a, n, d=1000, r=1, l=1):
    p = 0
    for i in range(0, n - 1, 2):
        y = a[i]
        x = a[i + 1]
        if y ** 2 + x ** 2 <= d ** 2:
            p += 1
    if p:
        return (8 * p) / n
    else:
        return 0


def analiz_pi(a, d, delta, metod):
    k = 0
    while k <= len(a) - delta:
        yield metod(a[k: k + delta + 1], delta, d)
        k += delta


def neyman_generator(n, d=1000, mode=1):
    tg = time()
    if mode:
        file = open("neyman.txt", 'a')
        print(' ', file=file)
    else:
        with open("neyman.txt", 'r') as file:
            strfile = file.read().replace("\n", " ")
            a = list(map(int, strfile.split()))
            file.close()
            return a
    t = int(time() * 10 ** 6) % 10 ** 6
    a = [0] * n
    for i in range(n):
        t = (t / 10 ** 6) ** 2
        t = (int(t * 10 ** 12) // 10 ** 3) % 10 ** 6
        a[i] = t % (d + 1)
        # print(a[i], end=" ")
        if t == 0:
            t = int(time() * 10 ** 6) % 10 ** 6
    print('time: ', round(time() - tg, 3))
    print(*a, file=file)
    file.close()
    return a


def middle_generator(n, d, mode=1):
    tg = time()
    if mode:
        file = open("middle.txt", 'a')
        print(' ', file=file)
    else:
        with open("middle.txt", 'r') as file:
            strfile = file.read().replace("\n", " ")
            a = list(map(int, strfile.split()))
            file.close()
            return a
    r0 = int(time() * 10 ** 6) % 10 ** 6
    r1 = int(time() * 10 ** 12) % 10 ** 6
    a = [0] * n
    for i in range(n):
        r = ((r1 * r0) // 10 ** 3) % 10 ** 6
        r0 = r1
        r1 = r
        a[i] = r % (d + 1)
        # print(a[i], end=" ")
        if r == 0:
            r1 = int(time() * 10 ** 6) % 10 ** 6
    print('time: ', round(time() - tg, 3))
    print(*a, file=file)
    file.close()
    return a


def line_generator(n, d=1000, mode=1):
    tg = time()
    if mode:
        file = open("line.txt", 'a')
        print(' ', file=file)
    else:
        with open("line.txt", 'r') as file:
            strfile = file.read().replace("\n", " ")
            a = list(map(int, strfile.split()))
            file.close()
            return a
    x0 = int(time() * 10 ** 12) % 10 ** 12
    a = 1664525
    c = 1013904223
    m = 2 ** 32
    la = [0] * n
    for i in range(n):
        x = (a * x0 + c) % m
        la[i] = x % (d + 1)
        x0 = x
    print('time: ', round(time() - tg, 3))
    print(*la, file=file)
    file.close()
    return la


def fib_generator(n, d=1000, mode=1):
    tg = time()
    if mode:
        file = open("fibgen.txt", 'a')
        print(' ', file=file)
    else:
        with open("fibgen.txt", 'r') as file:
            strfile = file.read().replace("\n", " ")
            a = list(map(int, strfile.split()))
            file.close()
            return a
    m = 2 ** 32
    a = [0] * 55 + [0] * n
    a[0], a[1] = int(tg * 10 ** 6) % 10 ** 6 % m, int(tg * 10 ** 6) % 10 ** 6 % m
    for i in range(1, 55):
        a[i] = (a[i - 1] + a[i - 2]) % m
    for i in range(55, n + 55):
        a[i] = (a[i - 55] + a[i - 24]) % m
    print('time: ', round(time() - tg, 3))
    print(*[a[i] % (d + 1) for i in range(55, n + 55)], file=file)
    file.close()
    return [a[i] % (d + 1) for i in range(55, n + 55)]


def RSLOS(reg, mask, p):
    b0 = bin(mask & reg).count('1') % 2
    return ((reg << 1) | b0) % 2 ** p


def RSLOS_generator(n, d=1000, mode=1):
    tg = time()
    m = 2 ** 32
    reg = int(time() * 10 ** 10) % 10 ** 10 % 2 ** 32
    a = [0] * n
    if mode:
        file = open("rslos.txt", 'a')
        print(' ', file=file)
    else:
        file = open("rslos.txt", 'r')
        strfile = file.read().replace("\n", " ")
        a = list(map(int, strfile.split()))
        file.close()
        return a
    l = ['0'] * 32
    l[31] = l[5] = l[0] = '1'
    mask = int(''.join(reversed(l)), 2)
    # mask = 0b10000000000000000000000001000101
    #            0 1 4 6 30
    for i in range(n):
        b31 = 0
        dig = 0
        for j in range(32):
            reg = RSLOS(reg, mask, 32)
            b31 = reg >> 31
            dig = dig | b31
            if j < 31:
                dig = dig << 1
        a[i] = dig % (d + 1)
        print(a[i], file=file, end=" ")
        print(len(a) / n * 100, '%')

    file.close()
    print('time: ', round(time() - tg, 3))
    return a


def golmann_generator(n, d, mode=1):
    tg = time()
    m = 2 ** 32
    a = [0] * n
    if mode:
        file = open("gollman.txt", 'a')
        print(' ', file=file)
    else:
        with open("gollman.txt", 'r') as file:
            strfile = file.read().replace("\n", " ")
            a = list(map(int, strfile.split()))
            file.close()
            return a
    count_reg = 15
    reg = [0] * count_reg
    parametry = ((31, 7, 0),
                 (31, 13, 0),
                 (32, 7, 6, 2, 0),
                 (32, 7, 5, 3, 2, 1, 0),
                 (33, 13, 0),
                 (33, 16, 4, 1, 0),
                 (34, 8, 4, 3, 0),
                 (34, 7, 6, 5, 2, 1, 0),
                 (35, 2, 0),
                 (36, 11, 0),
                 (36, 6, 5, 4, 2, 1, 0),
                 (37, 6, 4, 1, 0),
                 (37, 5, 4, 3, 2, 1, 0),
                 (38, 6, 5, 1, 0),
                 (39, 4, 0),
                 (40, 5, 4, 3, 0),
                 (41, 3, 0),
                 (42, 7, 4, 3, 0),
                 (42, 5, 4, 3, 2, 1, 0),
                 (43, 6, 4, 3, 0),
                 (44, 6, 5, 2, 0),
                 (45, 4, 3, 1, 0),
                 (46, 8, 7, 6, 0),
                 (46, 8, 5, 3, 2, 1, 0))
    for i in range(count_reg):
        l = ['0'] * (parametry[i][0] + 1)
        for j in parametry[i]:
            l[j] = '1'
        reg[i] = [int(sum(parametry[i]) * time() * 10 ** 12) % 10 ** 12 % 2 ** (parametry[i][0] + 1),
                  int(''.join(reversed(l)), 2), (parametry[i][0] + 1)]

    for i in range(n):
        b31 = [0] * count_reg
        dig = 0
        # тактирование
        for j in range(32):
            takt = 1
            for k in range(count_reg):
                if takt:
                    reg[k][0] = RSLOS(*reg[k])
                takt = reg[k][0] >> (reg[k][2] - 1)
                b31[k] = takt
            dig = dig | sum(b31) % 2
            if j < 31:
                dig = dig << 1
        a[i] = dig % (d + 1)
        print(a[i], file=file, end=" ")
        print(len(a) / n * 100, '%')
    print('time: ', round(time() - tg, 3))

    file.close()
    return a


class mouse_generator():
    def __init__(self, n, d, mode=1):
        self.a = []
        if mode:
            self.file = open("mouse.txt", 'a')
            print(' ', file=self.file)
        else:
            self.file = open("mouse.txt", 'r')
            self.a = list(map(lambda x: int(x) % d, self.file.read().replace("\n", " ").split()))
            self.file.close()
            return
        self.n = n
        self.d = d
        self.mouseWin = Tk()
        self.mouseWin.protocol("WM_DELETE_WINDOW", self.onExit)
        self.proc = StringVar()
        self.mouseWin.title("Двигайте мышью в пределах окна для сбора случайных чисел")
        self.mouseWin.geometry("600x400")
        ProgressBar = Frame(self.mouseWin, bd=2, relief=RAISED)
        ProgressBar.pack(side=BOTTOM, fill=X)
        draw = Frame(self.mouseWin, bd=2, relief=RAISED)
        draw.pack(side=TOP, fill=BOTH)
        self.drawcan = Canvas(draw, width=590, height=390, border=1, relief=SUNKEN)
        self.drawcan.pack(side=TOP)
        lab = Label(ProgressBar, textvariable=self.proc)
        self.can = Canvas(ProgressBar, width=590, height=5, border=1, relief=SUNKEN)
        self.can.pack(side=TOP)
        lab.pack(side=TOP)
        self.proc.set(str(int(len(self.a) / self.n * 100)) + ' %')
        self.lastXY = 0, 0
        self.mouseWin.bind("<Motion>", self.onMotion)
        self.mouseWin.focus_set()
        self.mouseWin.grab_set()
        self.mouseWin.wait_window()
        # self.mouseWin.mainloop()

    def onExit(self):
        self.file.close()
        self.mouseWin.destroy()

    def onMotion(self, event):
        X, Y = event.x, event.y
        v = ((X - self.lastXY[0]) ** 2 + (Y - self.lastXY[1]) ** 2) ** 0.5
        if v - int(v) < 0.000001:
            return
        # self.drawcan.create_oval(X, Y, X + int(v), Y + int(v), width=0,
        #                          fill="#" + hex(randint(16, 255))[2:] + hex(randint(16, 255))[2:] + hex(
        #                              randint(16, 255))[2:])
        v = int(v * 10 ** 4) % 10 ** 6
        # if len(self.a) and self.a[-1]:
        #     v = self.a[-1] * v
        # print(v)
        self.a.append(v % (self.d + 1))
        print(self.a[-1], file=self.file, end=" ")
        self.proc.set(str(int(len(self.a) / self.n * 100)) + ' %')
        rec = self.can.create_rectangle(0, 0, int(len(self.a) / self.n * 590), 390, fill="blue")
        self.lastXY = X, Y
        if len(self.a) >= self.n:
            # print(*self.a)
            self.onExit()


def real_generator(n, d, mode=1):
    if mode:
        return []
    file = open("output.txt", "r")
    bits = file.read().replace("\n", "")
    bits = bits.replace(" ", "")
    a = []
    tmp = ""
    for si in bits:
        tmp += si
        if len(tmp) >= 16:
            a.append(int(tmp, 2) % (d + 1))
            # if len(a) >= n:
            #     break
            tmp = ""
    file.close()
    return a


def random_analiz(a, d):
    # b = [0] * (d + 1)
    # for i in a:
    #     # print(i)
    #     b[i] += 1
    av = sum(a) / len(a) / (d)
    D = sum([(a[i] / (d) - av) ** 2 for i in range(len(a))]) / len(a)
    G = D ** 0.5
    v = len([i for i in a if 0.2113 < (i / (d)) < 0.7887]) / len(a)
    print('матем. ожид.', av)
    print('дисперсия   ', D)
    print('станд. откл.', G)
    print('частотный', v)
    return av, D, G, v


def shuffle_generator(n, d, mode=1):
    tg = time()
    if mode:
        file = open("shuffle.txt", 'a')
        print(' ', file=file)
    else:
        with open("shuffle.txt", 'r') as file:
            strfile = file.read().replace("\n", " ")
            a = list(map(int, strfile.split()))
            file.close()
            return a
    a = [0] * n
    R = int(time() * 10 ** 8 % 10 ** 8)
    for i in range(n):
        R0 = int(str(R)[-2:] + str(R)[:-2])
        R1 = int(str(R)[2:] + str(R)[:2])
        R = (R1 + R0) % 10 ** 8
        a[i] = R % (d + 1)
    print('time: ', round(time() - tg, 3))
    print(*a, file=file)
    file.close()
    return a


def quantum_generator(n, d, mode=1):
    tg = time()
    a = []
    if mode:
        file = open("quantum.txt", 'a')
        print(' ', file=file)
    else:
        with open("quantum.txt", 'r') as file:
            strfile = file.read().replace("\n", " ")
            a = list(map(int, strfile.split()))
            file.close()
            return a
    while len(a) < n:
        a += list(map(lambda x: x % (d + 1), get_data(data_type='uint16', array_length=1024)))
        print(*a[-1024:], file=file, end=" ")
        print(len(a) / n * 100, '%')
    print('time: ', round(time() - tg, 3))
    file.close()
    return a


def ideal_generator(n, d, mode=1):
    a = []
    if mode:
        return []
    for i in range(1000):
        for j in range(1000):
            a += [i] + [j]
    return a


def fmouse_generator(n, d=1000, mode=1):
    if mode:
        file = open("mouse.txt", 'a')
        print(' ', file=file)
    else:
        with open("mouse.txt", 'r') as file:
            strfile = file.read().replace("\n", " ")
            a = list(map(int, strfile.split()))
            file.close()
            return a
    mouse = mouse_generator(n, d)
    #mouse.mouseWin.wait_window()
    return mouse.a


generators = (rand_generator,
              os_generator,
              neyman_generator,
              middle_generator,
              knut_generator,
              shuffle_generator,
              line_generator,
              fib_generator,
              RSLOS_generator,
              golmann_generator,
              fmouse_generator,
              quantum_generator,
              real_generator,
              ideal_generator)

desriptios = ("Генератор случайных чисел randint из "
              "стандартной библиотели Python random",
              "urandom Python OS",
              "Генератор фон Неймана",
              "Срединных произведений",
              "Генератор Кнута",
              "Перемешивание",
              "ЛКГ",
              "Фибоначчи со сдвигом",
              "РСЛОС",
              "Каскад Голлмана",
              "Движением мыши",
              "Квантовый генератор",
              "Тепловых шумов",
              '"Идеальный" генератор'
              )

if __name__ == "__main__":
    g = 10
    d = 999
    n = 1000
    delta = 100
    a = generators[g](n, d)
    print(len(a))

    print('-' * 30)
    random_analiz(a, d)
    print('-' * 30)

    bhit = []
    for pib in analiz_pi(a, d, delta, hit_or_miss):
        bhit.append(pib)
    pihit = sum(bhit) / len(bhit)
    hitD = (sum([(x - pi) ** 2 for x in bhit]) / len(bhit)) ** 0.5
    print(pihit, pi - pihit, hitD, sep='\n')
    print('-' * 30)
    bbuf = []
    for pib in analiz_pi(a, d, delta, pi_buffon):
        bbuf.append(pib)
    pibuf = sum(bbuf) / len(bbuf)
    bufD = (sum([(x - pi) ** 2 for x in bbuf]) / len(bbuf)) ** 0.5
    print(pibuf, pi - pibuf, bufD, sep='\n')
    print('-' * 30)
    print(pi)
