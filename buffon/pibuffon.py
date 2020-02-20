from tkinter import *
from generators import *
from math import pi
from tkinter.messagebox import showinfo, showerror


# from ctypes import *
# import platform
# if int(platform.win32_ver()[0]) > 7:
#     windll.shcore.SetProcessDpiAwareness(1)
class PI_Buffon:
    def __init__(self):
        self.win_create()
        self.needles = StringVar()
        self.experience = StringVar()
        self.long_needle = StringVar()
        self.long_desk = StringVar()
        self.cur_algo = IntVar()
        self.check_file = IntVar()
        self.tools_create()
        self.progressbar_create()
        self.algo_create()
        self.graf_create()

    def win_create(self):
        self.win = Tk()
        self.win.title("Задача Бюффона")
        self.win.geometry("1024x768+100+100")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW", self.onClose)

    def algo_create(self, parrent=None):
        if not parrent:
            parrent = self.win
        self.algo = Frame(parrent, bd=1, relief=RAISED)
        self.algo.pack(side=RIGHT, padx=5, pady=5, fill=Y)
        Label(self.algo, text="Выбор алгоритма\nгенерации случайных чисел").pack(side=TOP, padx=5, pady=5)
        self.algo_list = Listbox(self.algo, bd=2, relief=SUNKEN, width=25, height=len(generators))
        self.algo_list.pack(side=TOP, padx=5, pady=5)
        self.algo_list.bind("<<ListboxSelect>>", self.algoSelect)
        Label(self.algo, text="Описание алгоритма\nи анализ результатов").pack(side=TOP, padx=5, pady=5)
        self.algo_descript = Text(self.algo, width=20, height=20, wrap=WORD)
        self.algo_descript.pack(side=TOP, padx=5, pady=5)
        for g in generators:
            self.algo_list.insert(END, str(g).split()[1])

    def algoSelect(self, event):
        if not self.algo_list.curselection():
            self.GO.config(state=DISABLED)
            return
        self.GO.config(state=NORMAL)
        self.cur_algo.set(self.algo_list.curselection()[0])
        self.algo_descript.delete(1.0, END)
        self.algo_descript.insert(END, desriptios[self.cur_algo.get()])

    def tools_create(self, parrent=None):
        if not parrent:
            parrent = self.win
        self.needles.set('1000')
        self.experience.set('10')
        self.long_desk.set('1')
        self.long_needle.set('1')
        self.tools = Frame(parrent, bd=1, relief=RAISED)
        self.tools.pack(side=TOP, padx=5, pady=5, fill=X)
        # Label(self.tools, text="Параметры задачи:").pack(side=TOP, pady=5)
        Label(self.tools, text="Количество бросков:").pack(side=LEFT, padx=5)
        num_needles = Entry(self.tools, textvariable=self.needles, width=8)
        num_needles.pack(side=LEFT, pady=5)
        num_needles.bind("<KeyRelease>",
                         lambda event: self.needles.set(
                             '0' if not self.needles.get().isdecimal() else (str(int(self.needles.get()) % 1000001))))
        Label(self.tools, text="Количество опытов:").pack(side=LEFT, padx=5)
        num_experience = Entry(self.tools, textvariable=self.experience, width=8)
        num_experience.pack(side=LEFT, pady=5)
        num_experience.bind("<KeyRelease>",
                            lambda event: self.experience.set('0' if not self.experience.get().isdecimal() else (
                                '0' if not self.needles.get() else str(
                                    int(self.experience.get()) % 101))))
        Label(self.tools, text="Длина иглы:").pack(side=LEFT, padx=5)
        num_long = Entry(self.tools, textvariable=self.long_needle, width=3)
        num_long.pack(side=LEFT, pady=5)
        num_long.bind("<KeyRelease>",
                      lambda event: self.long_needle.set(
                          '0' if not self.long_needle.get().isdecimal() else (str(int(self.long_needle.get()) % 11))))
        Label(self.tools, text="Расстояние между линиями:").pack(side=LEFT, padx=5)
        num_desk = Entry(self.tools, textvariable=self.long_desk, width=3)
        num_desk.pack(side=LEFT, pady=5)
        num_desk.bind("<KeyRelease>",
                      lambda event: self.long_desk.set(
                          '0' if not self.long_desk.get().isdecimal() else (str(int(self.long_desk.get()) % 11))))
        Checkbutton(self.tools, text="Из файла", variable=self.check_file).pack(side=LEFT, padx=5)
        self.GO = Button(self.tools, text="Эксперимент", width=12, command=self.onExp, state=DISABLED)
        self.GO.pack(side=LEFT, padx=20, pady=10)
        self.EXIT = Button(self.tools, text="Выход", width=12, command=self.onClose)
        self.EXIT.pack(side=LEFT, padx=20, pady=10)

    def progressbar_create(self, parrent=None):
        if not parrent:
            parrent = self.win
        self.progressbar = Frame(parrent, bd=2, relief=RAISED)
        self.progressbar.pack(side=TOP, padx=5, fill=BOTH)
        self.progresscan = Canvas(self.progressbar, width=1020, height=5, border=1, relief=SUNKEN)
        self.progresscan.pack(side=TOP, padx=1)

    def onClose(self):
        self.win.destroy()

    def graf_create(self, parrent=None):
        if not parrent:
            parrent = self.win
        self.graf = Frame(parrent, bd=2, relief=RAISED)
        self.graf.pack(side=LEFT, padx=5, pady=5, fill=Y)
        self.can = Canvas(self.graf, width=810, height=665, bg="black")
        self.can.pack(side=TOP, padx=5, pady=5)
        self.blank_canvas()

    def onExp(self):
        if not (int(self.needles.get()) and int(self.experience.get()
                                                and int(self.long_desk.get()) and int(self.long_needle.get()))):
            return
        self.progresscan.delete(ALL)
        self.algo_descript.delete(1.0, END)
        # self.blank_canvas()
        self.GO.config(state=DISABLED)
        self.algo_list.config(state=DISABLED)
        self.buflist = []
        self.hitlist = []
        n = int(self.needles.get()) * 2
        l = int(self.long_needle.get())
        r = int(self.long_desk.get())
        k = self.algo_list.curselection()[0]
        t = time()
        b = []
        if self.check_file.get():
            b = generators[k](n, 999, 1 - self.check_file.get())
        for i in range(int(self.experience.get())):
            self.progresscan.create_rectangle(0, 0,
                                              (i + 1) * 1020 // int(self.experience.get()), 10, fill="blue")
            self.progresscan.update()
            if len(b) >= n:
                a = b[:n]
                b = b[n:]
            else:
                a = generators[k](n, 999)
                if len(a) < n:
                    showerror('Ошибка генерации!',
                              'Невозможно сгенерировать {} чисел'.format(
                                  int(self.needles.get()) * int(self.experience.get())))
                    self.GO.config(state=NORMAL)
                    self.algo_list.config(state=NORMAL)
                    self.progresscan.delete(ALL)
                    return
            self.buflist.append(pi_buffon(a, n, 999, r, l))
            self.hitlist.append(hit_or_miss(a, n, 999, r, l))
        self.algo_descript.insert(END, "Время работы: " + str(round(time() - t, 3)))
        av, D, G, v = random_analiz(a, 999)
        self.algo_descript.insert(END, "\nСреднее: " + str(round(av, 5)))
        self.algo_descript.insert(END, "\nДисперсия: " + str(round(D, 5)))
        self.algo_descript.insert(END, "\nСт. откл.: " + str(round(G, 5)))
        self.algo_descript.insert(END, "\nЧаст. анализ: " + str(round(v, 5)))
        self.blank_canvas((self.buflist, self.hitlist))
        self.GO.config(state=NORMAL)
        self.algo_list.config(state=NORMAL)
        self.progresscan.delete(ALL)

    def blank_canvas(self, a=None):
        self.can.delete(ALL)
        canxy = (40, 620)
        canw = 760
        canh = 600
        cancol = "white"
        self.can.create_line(canxy[0], canxy[1], canxy[0], canxy[1] - canh,
                             arrowshape="15 25 5", arrow="last", fill=cancol, width=3)
        self.can.create_line(canxy[0], canxy[1], canxy[0] + canw, canxy[1],
                             arrowshape="15 25 5", arrow="last", fill=cancol, width=3)
        for y in range(1, 30):
            self.can.create_text(20, canxy[1] - y * canh // 30,
                                 fill=cancol, text=str(round(3.0 + 0.01 * y, 3)))
            self.can.create_oval(canxy[0] - 3, canxy[1] - y * canh // 30 - 3,
                                 canxy[0] + 3, canxy[1] - y * canh // 30 + 3,
                                 fill="blue")
            # self.can.create_line(canxy[0] + 3, canxy[1] - y * canh // 40,
            #                      canxy[0] + canw, canxy[1] - y * canh // 40,
            #                      fill="lightgray", dash=[5, 10])
        self.can.create_line(canxy[0] + 3, canxy[1] - (pi - 3.0) * 100 * canh // 30,
                             canxy[0] + canw, canxy[1] - (pi - 3.0) * 100 * canh // 30,
                             fill="yellow", width=3)
        n = int(self.experience.get()) + 1
        for x in range(1, n):
            if n <= 51:
                self.can.create_text(canxy[0] + x * (canw - 15) // n, canxy[1] + 15,
                                     fill=cancol, text=str(x))
                self.can.create_oval(canxy[0] + x * (canw - 15) // n + 3, canxy[1] + 3,
                                     canxy[0] + x * (canw - 15) // n - 3, canxy[1] - 3,
                                     fill="blue")
            # self.can.create_line(canxy[0] + 3, canxy[1] - y * canh // 10,
            #                      canxy[0] + canw, canxy[1] - y * canh // 10,
            #                      fill="lightgray", dash=[5, 10])
        if not a:
            return
        self.algo_descript.insert(END, "\n\nСреднее Бюффон:\n" + str(round(sum(a[0]) / len(a[0]), 7)))
        self.algo_descript.insert(END, "\nСт.откл. Бюффон:\n" +
                                  str(round((sum([(x - sum(a[0]) / len(a[0])) ** 2 for x in a[0]]) / len(a[0])) ** 0.5,
                                            7)))
        self.algo_descript.insert(END, "\nРазность: " + str(round(sum(a[0]) / len(a[0]) - pi, 7)))

        self.algo_descript.insert(END, "\n\nСреднее HitOrMiss:\n" + str(round(sum(a[1]) / len(a[1]), 7)))
        self.algo_descript.insert(END, "\nСт.откл. HitOrMiss:\n" +
                                  str(round((sum([(x - sum(a[1]) / len(a[1])) ** 2 for x in a[1]]) / len(a[1])) ** 0.5,
                                            7)))
        self.algo_descript.insert(END, "\nРазность: " + str(round(sum(a[1]) / len(a[1]) - pi, 7)))
        self.can.create_line(canxy[0] + 3, canxy[1] - (sum(a[0]) / len(a[0]) - 3.0) * 100 * canh // 30,
                             canxy[0] + canw, canxy[1] - (sum(a[0]) / len(a[0]) - 3.0) * 100 * canh // 30,
                             fill="red", width=3)
        self.can.create_line(canxy[0] + 3, canxy[1] - (sum(a[1]) / len(a[1]) - 3.0) * 100 * canh // 30,
                             canxy[0] + canw, canxy[1] - (sum(a[1]) / len(a[1]) - 3.0) * 100 * canh // 30,
                             fill="green", width=3)
        l1 = 3.0
        l2 = 3.0
        for i in range(len(a[0])):
            self.can.create_oval(canxy[0] + (i + 1) * (canw - 15) // n - 5,
                                 canxy[1] - (a[0][i] - 3.0) * 100 * canh // 30 - 5,
                                 canxy[0] + (i + 1) * (canw - 15) // n + 5,
                                 canxy[1] - (a[0][i] - 3.0) * 100 * canh // 30 + 5,
                                 fill="red")
            if i:
                self.can.create_line(canxy[0] + (i) * (canw - 15) // n,
                                     canxy[1] - (l1 - 3.0) * 100 * canh // 30,
                                     canxy[0] + (i + 1) * (canw - 15) // n,
                                     canxy[1] - (a[0][i] - 3.0) * 100 * canh // 30,
                                     fill="red")
            l1 = a[0][i]
            self.can.create_oval(canxy[0] + (i + 1) * (canw - 15) // n - 5,
                                 canxy[1] - (a[1][i] - 3.0) * 100 * canh // 30 - 5,
                                 canxy[0] + (i + 1) * (canw - 15) // n + 5,
                                 canxy[1] - (a[1][i] - 3.0) * 100 * canh // 30 + 5,
                                 fill="green")
            if i:
                self.can.create_line(canxy[0] + (i) * (canw - 15) // n,
                                     canxy[1] - (l2 - 3.0) * 100 * canh // 30,
                                     canxy[0] + (i + 1) * (canw - 15) // n,
                                     canxy[1] - (a[1][i] - 3.0) * 100 * canh // 30,
                                     fill="green")
            l2 = a[1][i]


if __name__ == "__main__":
    main = PI_Buffon()
    main.win.mainloop()
