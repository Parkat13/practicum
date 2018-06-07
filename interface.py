# -*- coding: utf-8 -*-
from tkinter import *
import classes_for_project as cl
widgets, local_widgets = [], []
root = Tk()
root.geometry("800x500+300+100")
capital, n_pond, duration, forfeit, cost_forage, cost_fish, percent = 0, 0, 0, 0, 0, 0, 0
ponds, contract_fish, contract_forage = [], [], []
world = 0

def interface():# приветствие
    global widgets, root
    root.title('Рыбоводческое хозяйство')
    fra1 = Frame(root, width=800, height=150)
    lab1 = Label(root, text="Добро пожаловать! \n \n ", font="Roman 12")
    lab2 = Label(root, text="Вас приветствует экономическая игра: \n \n Рыбоводческое хозяйство", font="Roman 10")
    fra2 = Frame(root, width=800, height=250)
    but = Button(root, text="Далее")
    but.bind("<Button-1>", next1)
    fra1.grid(row=0, column=0)
    lab1.grid(row=1, column=0)
    lab2.grid(row=2, column=0)
    fra2.grid(row=3, column=0)
    but.grid(row=3, column=0, rowspan=2, columnspan=3)
    widgets = [fra1, lab1, lab2, fra2, but]
    root.mainloop()

def next1(event):# стартовый капитал
    global widgets, root, local_widgets
    for i in widgets:
        i.destroy()
    for i in local_widgets:
        i.destroy()
    fra1 = Frame(root, width=800, height=150)
    lab1 = Label(root, text="Для начала вам нужно выбрать \n \n стартовый капитал \n ", font="Roman 10")
    fra2 = Frame(root, width=800, height=140)
    ent1 = Entry(root, width=30, bd=3)
    lab2 = Label(root, text="   ", font="Roman 8", fg="red")
    fra3 = Frame(root, width=800, height=119)
    but1 = Button(root, text="Далее")
    but1.bind("<Button-1>", next2)
    fra1.grid(row=0, column=0)
    lab1.grid(row=1, column=0)
    fra2.grid(row=2, column=0)
    ent1.grid(row=2, column=0)
    lab2.grid(row=3, column=0)
    fra3.grid(row=4, column=0)
    but1.grid(row=4, column=0)
    widgets = [fra1, lab1, fra2, ent1, lab2, fra3, but1]

def next2(event):# проверка, что в строке указано число
    global capital, root, widgets
    capital_test = widgets[3].get()
    if capital_test.isdigit():
        capital = capital_test
        next3()
    else:
        widgets.append(Label(root, text="Нужно ввести число!", font="Roman 8", fg="red"))
        widgets[len(widgets)-1].grid(row=3, column=0)

def next3():# кол-во прудов
    global root, widgets
    for i in widgets:
        i.destroy()
    fra1 = Frame(root, width=800, height=150)
    lab1 = Label(root, text="Теперь нужно определить, сколько у \n \n Вас будет прудов \n ", font="Roman 10")
    fra2 = Frame(root, width=800, height=140)
    sca1 = Scale(root, orient=HORIZONTAL, length=300, from_=2, to=7, tickinterval=1, resolution=1)
    fra3 = Frame(root, width=800, height=170)
    but1 = Button(root, text="Далее")
    but1.bind("<Button-1>", next4)
    fra1.grid(row=0, column=0)
    lab1.grid(row=1, column=0)
    fra2.grid(row=2, column=0)
    sca1.grid(row=2, column=0)
    fra3.grid(row=4, column=0)
    but1.grid(row=4, column=0)
    widgets = [fra1, lab1, fra2, sca1, fra3, but1]

def next4(event):# проверка, что в строке указано число
    global n_pond, root, widgets, ponds
    n_pond = widgets[3].get()
    ponds = []
    for j in range(int(n_pond)):
        ponds.append([])
    next5()

def next5():# содержание прудов
    global root, widgets, n_pond
    for i in widgets:
        i.destroy()
    fra1 = Frame(root, width=800, height=50)
    lab1 = Label(root, text="Выберете, сколько рыб и какого вида \n \n находятся в каждом из прудов \n \n ", font="Roman 10")
    lab2 = Label(root, text=" Вид рыб \n \n \n \n", font="Arial 9")
    lab3 = Label(root, text="Количество рыб \n \n \n \n", font="Arial 9")
    txt1 = Text(root,width=70,height=13,font="8", state=DISABLED)
    widgets = []
    for i in range(int(n_pond)):
        fra0 = Frame(root, width=100, height=50)
        if len(str(i+1))==1:
            lab0 = Label(fra0, text="      Пруд №" + str(i+1) + "               \n ", font="Arial 8")
        else:
            lab0 = Label(fra0, text="      Пруд №" + str(i+1) + "              \n ", font="Arial 8")
        lab0.grid(row=i, column=0)
        widgets.append(lab0)
        lis0 = Listbox(fra0, selectmode=SINGLE, height=1)
        for j in cl.fish:
            lis0.insert(END, j)
        lis0.grid(row=i, column=1)
        lis0.bind("<<ListboxSelect>>", (lambda x: get_pond(x.widget, x.widget.curselection())))
        widgets.append(lis0)
        lab01 = Label(fra0, text="         \n ", font="Arial 8")
        lab01.grid(row=i, column=2)
        widgets.append(lab01)
        sca0 = Scale(fra0, orient=HORIZONTAL, length=300, from_=0, to=50, tickinterval=10, resolution=1)
        sca0.grid(row=i, column=3)
        widgets.append(sca0)
        txt1.window_create(END, window=fra0)
    scr = Scrollbar(root)
    scr.config(command=txt1.yview)
    txt1.config(yscrollcommand=scr.set)
    fra1.grid(row=0, column=0, columnspan=3)
    lab1.grid(row=1, column=0, columnspan=3)
    lab2.grid(row=2, column=1)
    lab3.grid(row=2, column=2)
    scr.place(x=748, y=170, height=260)
    txt1.grid(row=3, column=0, columnspan=3)
    widgets = widgets + [fra1, lab1, lab2, lab3, txt1, scr]
    but1 = Button(root, text="Далее")
    but1.bind("<Button-1>", next6)
    but1.place(x=350, y=450)
    widgets.append(but1)

def get_pond(wid, res):
    global ponds,  widgets
    nn = 0
    for j in widgets:
        if j == wid:
            break
        else:
            nn+=1
    number = (nn-1)//4
    if len(res):
        ponds[number] = cl.fish[int(res[0])]

def next6(event):# сохранение данных о прудах
    global widgets, n_pond, ponds
    for i in range(int(n_pond)):
        if ponds[i] == []:
            ponds[i] = [cl.fish[0], widgets[i*4+3].get()]
        else:
            ponds[i] = [ponds[i], widgets[i*4+3].get()]
    next7()

def next7():# длительность контракта
    global root, widgets
    for i in widgets:
        i.destroy()
    fra1 = Frame(root, width=800, height=150)
    lab1 = Label(root, text="Теперь нужно определить длительность \n \n контракта \n ", font="Roman 10")
    fra2 = Frame(root, width=800, height=60)
    sca1 = Scale(root, orient=HORIZONTAL, length=300, from_=6, to=24, tickinterval=3, resolution=3)
    fra3 = Frame(root, width=800, height=80)
    fra4 = Frame(root, width=800, height=50)
    but1 = Button(root, text="Далее")
    but1.bind("<Button-1>", next8)
    fra1.grid(row=0, column=0)
    lab1.grid(row=1, column=0)
    fra2.grid(row=2, column=0)
    sca1.grid(row=3, column=0)
    fra3.grid(row=4, column=0)
    fra4.grid(row=5, column=0)
    but1.grid(row=5, column=0)
    widgets = [fra1, lab1, fra2, sca1, fra3, fra4, but1]

def next8(event):# параметры контракта
    global root, duration, widgets
    duration = widgets[3].get()
    for i in widgets:
        i.destroy()
    fra1 = Frame(root, width=800, height=50)
    lab1 = Label(root, text="Теперь выберете, сколько рыбы будете продавать \n \n и корма покупать каждую неделю \n \n ", font="Roman 10")
    lab2 = Label(root, text="     Кг рыбы  \n \n \n \n \n", font="Arial 8")
    lab3 = Label(root, text="Цена за кг\n \n \n \n \n", font="Arial 8")
    lab4 = Label(root, text=" Кг корма  \n \n \n \n \n", font="Arial 8")
    lab5 = Label(root, text="Цена за кг   \n \n \n \n \n", font="Arial 8")
    txt1 = Text(root, width=70, height=13, font="8", state=DISABLED)
    widgets = []
    for i in range(int(duration)//3):
        fra0 = Frame(root, width=100, height=50)
        if len(str(i*3)) == 1:
            lab0 = Label(fra0, text="  " + str(i*3) + "-" + str((i+1)*3) + " неделя   \n ", font="Arial 8")
        else:
            lab0 = Label(fra0, text="  " + str(i*3) + "-" + str((i+1)*3) + " неделя \n ", font="Arial 8")
        lab0.grid(row=i, column=0)
        widgets.append(lab0)
        sca01 = Scale(fra0, orient=HORIZONTAL, length=100, from_=0, to=30, tickinterval=10, resolution=1)
        sca01.grid(row=i, column=1)
        widgets.append(sca01)
        sca02 = Scale(fra0, orient=HORIZONTAL, length=180, from_=0, to=150, tickinterval=30, resolution=1)
        sca02.grid(row=i, column=2)
        widgets.append(sca02)
        sca03 = Scale(fra0, orient=HORIZONTAL, length=100, from_=0, to=30, tickinterval=10, resolution=1)
        sca03.grid(row=i, column=3)
        widgets.append(sca03)
        sca04 = Scale(fra0, orient=HORIZONTAL, length=180, from_=0, to=150, tickinterval=30, resolution=1)
        sca04.grid(row=i, column=4)
        widgets.append(sca04)
        txt1.window_create(END, window=fra0)
    scr = Scrollbar(root)
    scr.config(command=txt1.yview)
    txt1.config(yscrollcommand=scr.set)
    fra1.grid(row=0, column=0, columnspan=8)
    lab1.grid(row=1, column=0, columnspan=8)
    lab2.grid(row=2, column=3)
    lab3.grid(row=2, column=4)
    lab4.grid(row=2, column=5)
    lab5.grid(row=2, column=6)
    scr.place(x=748, y=170, height=260)
    txt1.grid(row=3, column=0, columnspan=8)
    widgets = widgets + [fra1, lab1, lab2, lab3, lab4, lab5, txt1, scr]
    but1 = Button(root, text="Далее")
    but1.bind("<Button-1>", next9)
    but1.place(x=350, y=450)
    widgets.append(but1)

def next9(event):
    global widgets, duration, contract_fish, contract_forage
    contract_fish, contract_forage = [], []
    for i in range(int(duration)//3):
        contract_fish.append([widgets[i*5+1].get(), widgets[i*5+2].get()])
        contract_forage.append([widgets[i*5+3].get(), widgets[i*5+4].get()])
    next10()

def next10():# последние параметры: процент гибели, стоимость корма, стоимость рыбы, неустойка
    global root, widgets
    for i in widgets:
        i.destroy()
    fra1 = Frame(root, width=800, height=20)
    lab1 = Label(root, text="Остались последние параметры \n \n \n Определите величину неустойки, выплачиваемую \n при невыполнении обязательств по контракту: \n ", font="Roman 10")
    ent1 = Entry(root, width=30, bd=3)
    lab2 = Label(root, text="\n \nСтоимость кг мальков для развода: \n ", font="Roman 10")
    ent2 = Entry(root, width=30, bd=3)
    lab3 = Label(root, text="\n \nСтоимость кг корма: \n ", font="Roman 10")
    ent3 = Entry(root, width=30, bd=3)
    lab4 = Label(root, text="\n \nПроцент гибели рыбы при неблагоприятных факторах: \n ", font="Roman 10")
    sca1 = Scale(root, orient=HORIZONTAL, length=600, from_=0, to=100, tickinterval=10, resolution=1)
    lab5 = Label(root, text=" \n  \n ", font="Roman 9")
    fra2 = Frame(root, width=800, height=50)
    but1 = Button(root, text="Далее")
    but1.bind("<Button-1>", next11)
    fra1.grid(row=0, column=0)
    lab1.grid(row=1, column=0)
    ent1.grid(row=2, column=0)
    lab2.grid(row=3, column=0)
    ent2.grid(row=4, column=0)
    lab3.grid(row=5, column=0)
    ent3.grid(row=6, column=0)
    lab4.grid(row=7, column=0)
    sca1.grid(row=8, column=0)
    lab5.grid(row=9, column=0)
    fra2.grid(row=10, column=0)
    but1.grid(row=10, column=0)
    widgets = [fra1, lab1, ent1, lab2, ent2, lab3, ent3, lab4, sca1, lab5, fra2, but1]

def next11(event):
    global widgets, forfeit, cost_forage, cost_fish, percent
    local_forfeit = widgets[2].get()
    local_forage = widgets[6].get()
    local_fish = widgets[4].get()
    local_percent = widgets[8].get()
    if local_forfeit.isdigit() and local_forage.isdigit() and local_fish.isdigit():
        forfeit = local_forfeit
        cost_forage = local_forage
        cost_fish = local_fish
        percent = local_percent
        last()
    else:
        widgets.append(Label(root, text="Нужно ввести числа!", font="Roman 9", fg="red"))
        widgets[len(widgets) - 1].grid(row=9, column=0)

def last():# окончательное окно
    global widgets, root, world, capital, n_pond, ponds, duration, contract_fish, contract_forage, forfeit, cost_fish, cost_forage, percent
    for i in widgets:
        i.destroy()
    cl.clean_queue = []
    world = cl.game_world(capital, n_pond, ponds, duration, contract_fish, contract_forage, forfeit, cost_fish, cost_forage, percent)
    fra1 = Frame(root, width=800, height=50)
    fra2 = Frame(root, width=800, height=40)
    txt1 = Text(root, width=70, height=13, font="8", state=DISABLED)
    str_lab = ''
    for j in range(int(n_pond)):
        str_lab = str_lab + ("пруд №" + str(j+1) + ": " + ponds[j][0] + "(" + str(ponds[j][1]) + ")\n")
    lab1 = Label(txt1, text="1 неделя \nКапитал: "
                            + str(capital)
                            + "\nКоличество корма: 0\nСостояние прудов: \n"
                            + str_lab
                            + "Параметры контракта на эту неделю: \n"
                            + str(contract_fish[0][0]) + " кг рыбы за " + str(contract_fish[0][1]) + " за кг, " + str(contract_forage[0][0]) + " кг корма за " + str(contract_forage[0][1]) + " за кг\n"
                            + " \n", font="Arial 10", width=100)
    txt1.window_create(END, window=lab1)
    scr = Scrollbar(root)
    scr.config(command=txt1.yview)
    txt1.config(yscrollcommand=scr.set)
    fra1.grid(row=0, column=0, columnspan=2)
    txt1.grid(row=1, column=0, columnspan=2)
    fra2.grid(row=2, column=0, columnspan=2)
    scr.place(x=748, y=51, height=213)
    but1 = Button(root, text="Купить мальков")
    but1.bind("<Button-1>", get_fish)
    sca1 = Scale(root, orient=HORIZONTAL, length=400, from_=0, to=100, tickinterval=10, resolution=1)
    but2 = Button(root, text="Купить корм")
    but2.bind("<Button-1>", get_forage)
    sca2 = Scale(root, orient=HORIZONTAL, length=400, from_=0, to=100, tickinterval=10, resolution=1)
    but3 = Button(root, text="Следующая неделя")
    but3.bind("<Button-1>", update_week)
    but3.place(x=280, y=440)
    but1.grid(row=3, column=0)
    sca1.grid(row=3, column=1)
    but2.grid(row=4, column=0)
    sca2.grid(row=4, column=1)
    widgets = [fra1, lab1, txt1, scr, fra2, but1, sca1, but2, sca2, but3]

def get_fish(event):
    global widgets, world
    fish = widgets[6].get()
    world.buy_fish(fish)
    if cl.flag_buy_fish:
        lab = Label(widgets[2], text="У Вас недостаточно средств \n", font="Arial 10", width=100)
        widgets[2].window_create(END, window=lab)
        widgets.append(lab)
    else:
        str_lab = ''
        for j in range(int(world.owner.n_pond)):
            str_lab = str_lab + ("пруд №" + str(j + 1) + ": " + world.owner.ponds[j].status + "(взрослых: " + str(
                world.owner.ponds[j].population_adults) + "; молодых: " + str(
                world.owner.ponds[j].population_young) + ")\n")
        lab = Label(widgets[2], text=str_lab, font="Arial 10", width=100)
        widgets[2].window_create(END, window=lab)
        widgets.append(lab)

def get_forage(event):
     global widgets, world
     forage = widgets[8].get()
     world .buy_forage(forage)
     if cl.flag_buy_forage:
         lab = Label(widgets[2], text="У Вас недостаточно средств \n", font="Arial 10", width=100)
         widgets[2].window_create(END, window=lab)
         widgets.append(lab)
     else:
         lab = Label(widgets[2], text="Количество корма: " + str(world.owner.forage) + "\n", font="Arial 10", width=100)
         widgets[2].window_create(END, window=lab)
         widgets.append(lab)

def update_week(event):
    global world, widgets
    if world.end_of_game:
        finish()
    else:
        world.update()
        str_lab = ''
        for j in range(int(world.owner.n_pond)):
            str_lab = str_lab + ("пруд №" + str(j+1) + ": " + world.owner.ponds[j].status + "(взрослых: " + str(world.owner.ponds[j].population_adults) +"; молодых: " + str(world.owner.ponds[j].population_young) + ")\n")
        if world.time > duration:
            lab = Label(widgets[2], text=str(world.time)
                                         + " неделя \nКапитал: "
                                         + str(world.owner.capital)
                                         + "\nКоличество корма: "
                                         + str(world.owner.forage)
                                         + "\nСостояние прудов: \n"
                                         + str_lab
                                         + "\n"
                                         , font="Arial 10", width=100)
        else:
            lab = Label(widgets[2], text="\n"
                                         + str(world.time)
                                         + " неделя \nКапитал: "
                                         + str(world.owner.capital)
                                         + "\nКоличество корма: "
                                         + str(world.owner.forage)
                                         + "\nСостояние прудов: \n"
                                         + str_lab
                                         + "Параметры контракта на эту неделю: \n"
                                         + str(
                                             world.owner.contract_fish[(world.time - 1) // 3][0]) + " кг рыбы за " + str(
                                             world.owner.contract_fish[(world.time - 1) // 3][1]) + " за кг, " + str(
                                             world.owner.contract_forage[(world.time - 1) // 3][0]) + " кг корма за " + str(
                                             world.owner.contract_forage[(world.time - 1) // 3][1]) + " за кг\n"
                                         , font="Arial 10", width=100)
        widgets[2].window_create(END, window=lab)
        widgets.append(lab)
        if world.factor:
            lab1 = Label(widgets[2], text="Вода в прудах похолодала \n " + str(percent) + " процентов рыбы погибло :(\n", font="Arial 10", width=100)
            widgets[2].window_create(END, window=lab1)
            widgets.append(lab1)

def finish():
    global local_widgets, world
    local_root = Tk()
    local_root.title('Конец игры')
    local_root.geometry("400x300+500+200")
    fra1 = Frame(local_root, width=400, height=100)
    if world.win_game:
        lab1 = Label(local_root, text="Вы выиграли! \n \n Хотите начать сначала?", font="Roman 10")
    else:
        lab1 = Label(local_root, text="Вы проиграли :( \n \n Хотите начать сначала?", font="Roman 10")
    fra2 = Frame(local_root, width=400, height=100)
    but1 = Button(local_root, text="Новая игра")
    but2 = Button(local_root, text="Выход")
    but1.bind("<Button-1>", next1)
    but2.bind("<Button-1>", end)
    fra1.grid(row=0, column=0)
    lab1.grid(row=1, column=0)
    fra2.grid(row=2, column=0)
    but1.grid(row=2, column=0)
    but2.grid(row=2, column=0)
    but1.place(x=50, y=200)
    but2.place(x=250, y=200)
    local_widgets = [fra1, lab1, fra2, but1, but2, local_root]

def end(event):
    global root, local_widgets
    root.destroy()
    local_widgets[-1].destroy()
    exit(0)

interface()
