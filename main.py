from matplotlib.pyplot import (
    plot, xlabel, ylabel, legend, grid, savefig, clf, figure
)
from matplotlib import use
use('agg')
from flet import (
    # Layout controls
    Page, Container, Column, ResponsiveRow, Card, NavigationBar, NavigationDestination, Image, ListView,
    # Input controls
    TextField, Dropdown, dropdown, InputFilter, KeyboardType,
    # Button controls
    ElevatedButton, Text, TextButton, icons,
    # Dialogs
    AlertDialog, SnackBar,
    # Other
    app, colors
)
from numpy import zeros
from math import sin
from os import remove, path, makedirs, listdir, rename
from screeninfo import get_monitors

PATH_TO_GRAPh = "data\graph.png"

path_to_eq1 = "data\eq1.png"
path_to_eq2 = "data\eq2.png"

graphChanged = False
eqChanged = False

global heightMinus


from numpy import linspace
from scipy.integrate import solve_ivp
# Класс инициализирующий все параметры конечного уравнения
class LastEquation(object):
    def __init__(self, n: int):
        self.n = n
        self.a_0 = 0
        self.a_1 = 0
        self.a_2 = 0
        self.a_3 = 0
        self.b_0 = 0

    def init_order_2(self, a_0: float, a_1: float, a_2: float, b_0: float):
        self.a_0 = a_0
        self.a_1 = a_1
        self.a_2 = a_2
        self.b_0 = b_0

    def init_order_3(self, a_0: float, a_1: float, a_2: float, a_3: float, b_0: float):
        self.a_0 = a_0
        self.a_1 = a_1
        self.a_2 = a_2
        self.a_3 = a_3
        self.b_0 = b_0

    def show_inf(self):
        print(self.n, self.a_0, self.a_1, self.a_2, self.a_3, self.b_0)

# Класс для решения системы уравнений
class Solver:
        def __init__(self, equation_function, initial_conditions, t_span, y, last_equation):
            self.equation_function = equation_function
            self.initial_conditions = initial_conditions
            self.t_span = t_span
            self.y = y
            self.last_equation = last_equation

        def solve(self):
            solution = solve_ivp(self.equation_function, self.t_span, self.initial_conditions,
                                 method='RK45',
                                 # Параметр, определяющий моменты времени (100 точек),
                                 # в которые будет выполняться интерполяция результата
                                 t_eval=linspace(self.t_span[0], self.t_span[1], 300), args=(self.y, self.last_equation))
            return solution


# Функция для решения системы 2 порядка
def func(t, x, y, last_equation: LastEquation):
    if(y == "1"):
        y_param = 1
    else:
        y_param = sin(t)

    if(last_equation.n == 2):
        dxdt = zeros(2)
        dxdt[0] = x[1]
        dxdt[1] = (1 / last_equation.a_2) * (last_equation.b_0*y_param - last_equation.a_1*x[1] - last_equation.a_0*x[0])
        return dxdt
    else:
        dxdt = zeros(3)
        dxdt[0] = x[1]
        dxdt[1] = x[2]
        dxdt[2] = (1 / last_equation.a_3) * (last_equation.b_0*y_param - last_equation.a_2*x[2] - last_equation.a_1*x[1] - last_equation.a_0*x[0])
        return dxdt

def getLatexCodeForNonKoshi(order, a0, a1, a2, a3, b0):
    if order == 2:
        return f"${a2:g} \cdot x_{{2}}''(t) + {a1:g} \cdot x_{{1}}'(t) + {a0:g} \cdot x_{{0}}(t) = {b0:g} \cdot y(t)$"
    else:
        return f"${a3:g} \cdot x_{{3}}'''(t) + {a2:g} \cdot x_{{2}}''(t) + {a1:g} \cdot x_{{1}}'(t) + {a0:g} \cdot x_{{0}}(t) = {b0:g} \cdot y(t)$"
    
def getLatexCodeForKoshi(order, a0, a1, a2, a3, b0):
    if order == 2:
        fraction = ""
        if a2 != 1:
            fraction = f"\\frac{{1}}{{{a2:g}}} \cdot "

        return f"$x'_{{1}}(t) = x_{{2}}(t),$" + '\n' + f"$x'_{{2}}(t) = {fraction} ({b0:g} \cdot y(t) - {a1:g} \cdot x_{{1}}(t) - {a0:g} \cdot x_{{0}}(t)).$"
    else:
        fraction = ""
        if a3 != 1:
            fraction = f"\\frac{{1}}{{{a3:g}}} \cdot "

        return f"$x'_{{1}}(t) = x_{{2}}(t),$" + '\n' + f"$x'_{{2}}(t) = x_{{3}}(t),$" + '\n' + f"$x'_{{3}}(t) = {fraction} ({b0:g} \cdot y(t) - {a2:g} \cdot x_{{2}}(t) - {a1:g} \cdot x_{{1}}(t) - {a0:g} \cdot x_{{0}}(t)).$"

def main(page: Page):
    page.title = "Лабораторная работа №1"
    page.window_width = 900
    page.window_height = 800
    heightMinus = 0

    # Получаем разрешение экрана
    for m in get_monitors():
        page.window_height = min(m.height, page.window_height)
        if m.height < 1080:
            heightMinus = 30

    # Функция для закрытия диалогового окна
    def closeDialog(e):
        page.dialog.open = False
        page.update()

    def validateData():
        problemFields = []
        # Проверка на ввод всех необходимых данных в нужные поля
        global fields
        fields = {'Порядок': modelOrder,
                'a0': a0,
                'a1': a1,
                'a2': a2,
                'a3': a3,
                'b0': b0,
                'x0': x0,
                'x_0': x_0,
                'x__0': x__0,
                'y(t)': y_dropdown,
                'Интервал t': interval}

        if not modelOrder.value:
            problemFields.append(modelOrder)

        elif modelOrder.value == "2":
            fieldsToCheck = ['a0', 'a1', 'a2', 'b0', 'x0', 'x_0']
            for field in fieldsToCheck:
                if not fields[field].value:
                    problemFields.append(fields[field])
            
            if a2.value == "0":
                problemFields.append(a2)

        elif modelOrder.value == "3":
            fieldsToCheck = ['a0', 'a1', 'a2', 'a3', 'b0', 'x0', 'x_0', 'x__0']
            for field in fieldsToCheck:
                if not fields[field].value:
                    problemFields.append(fields[field])

            if a3.value == "0":
                problemFields.append(a3)

        if not y_dropdown.value:
            problemFields.append(y_dropdown)
        if not interval.value:
            problemFields.append(interval)


        if len(problemFields) != 0:
            # Всем пробленным полям добавляется иконка ошибки
            for field in problemFields:
                field.icon = icons.ERROR_OUTLINE

            # Создание диалогового окна с ошибкой
            errorDialog = AlertDialog(
                modal=True,
                title=Text("Ошибка ввода данных"),
                content=Text("Заполнены не все необходимые поля"),
                actions=[
                    TextButton("OK", on_click=closeDialog),
                ]
            )

            page.dialog = errorDialog
            errorDialog.open = True
            page.update()
            return 0

        for field in fields.values():
            field.value = str(field.value).replace(",", ".")

        return 1
    
    def saveEquation(code, path):
        fig = figure()
        ax = fig.add_axes([0,0,1,1])

        t = ax.text(0.5, 0.5, code,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=20, color='black')

        bbox = t.get_window_extent()

        # Установка размеров области отрисовки
        fig.set_size_inches(bbox.width/80,bbox.height/80) # dpi=80

        ### Отрисовка или сохранение формулы в файл
        savefig(path, dpi=400)

    # Функция отправки введенный данных для вычисления
    def sendData(e):
        # Валидация данных на предмет заполненности полей
        if (not validateData()):
            return
        if not a3.value:
            a3.value = 0

        latexCodeNonKoshi = getLatexCodeForNonKoshi(int(modelOrder.value), float(a0.value), float(a1.value), float(a2.value), float(a3.value), float(b0.value))
        latexCodeKoshi = getLatexCodeForKoshi(int(modelOrder.value), float(a0.value), float(a1.value), float(a2.value), float(a3.value), float(b0.value))

        saveEquation(latexCodeNonKoshi, path_to_eq1)
        saveEquation(latexCodeKoshi, path_to_eq2)

        # Сохраняем пустой график
        clf()

        # Задаем размеры графика
        fig = figure()

        # Выбор параметров для последнего уравнения
        lastEquation = LastEquation(int(modelOrder.value))
        if(lastEquation.n == 3):
            lastEquation.init_order_3(
                                    float(a0.value),
                                    float(a1.value),
                                    float(a2.value),
                                    float(a3.value),
                                    float(b0.value))
        else:
            lastEquation.init_order_2(
                                    float(a0.value),
                                    float(a1.value),
                                    float(a2.value),
                                    float(b0.value))
        # Параметр y (либо y(t) = 1, либо y(t) = sin(t))
        y_parametr = y_dropdown.value
        # Начальные значения x(0), x'(0), x''(0) для 2 и 3 порядка модели
        if(lastEquation.n == 3):
            y0 = [float(x0.value), float(x_0.value), float(x__0.value)]
        else:
            y0 = [float(x0.value), float(x_0.value)]

        # Интервал интегрирования
        interval.value = int(float(interval.value))
        t_span = [0, interval.value]
        # Составление системы для решения
        system = Solver(func, y0, t_span, y_parametr, lastEquation)
        # Решение системы
        solution = system.solve()
        # Вывод графиков

        # Проверка наличия папки data
        if not path.exists("data"):
            makedirs("data")

        plot(solution.t, solution.y[0], label='x1(t)')
        plot(solution.t, solution.y[1], label="x2(t)")

        if(lastEquation.n == 3):
            plot(solution.t, solution.y[2], label="x3(t)")            
        
        xlabel('t, с')
        ylabel('xi(t)')
        legend()
        grid()
        savefig(PATH_TO_GRAPh)

        global graphChanged
        graphChanged = True
        global eqChanged
        eqChanged = True
        
        # Открытие SnackBar с уведомлением об успешном расчёте
        successNotification = SnackBar(
            Text("Решение успешно вычислено"),
            bgcolor=colors.GREEN_200
        )
        successNotification.open = True
        page.snack_bar = successNotification

        page.update()

    def orderChanged(e):
        aFields = [a0, a1, a2, a3, b0]
        xFields = [x0, x_0, x__0]
        if modelOrder.value.isdigit():
            if int(modelOrder.value) > 3:
                modelOrder.value = 3
            # Делаем поле ввода активными в зависимости от порядка модели
            for i in range(0, int(modelOrder.value) + 1):
                aFields[i].disabled = False
            for i in range(0, int(modelOrder.value)):
                xFields[i].disabled = False

            # Делаем поля ввода неактивными в зависимости от порядка модели
            for i in range(int(modelOrder.value) + 1, 4):
                aFields[i].value = ""
                aFields[i].disabled = True
            for i in range(int(modelOrder.value), 3):
                xFields[i].value = ""
                xFields[i].disabled = True
        else:
            # Если порядок не число, то делаем поля ввода неактивными и пустыми
            for filed in aFields:
                filed.value = ""
                filed.disabled = True
            for filed in xFields:
                filed.value = ""
                filed.disabled = True
        page.update()

    # Удаляет иконку ошибки при наведении на поле
    def removeIcon(e):
        if e.control.icon is not None:
            e.control.icon = None
            page.update()

    title1 = Text("Ввод порядка модели", weight="bold", size=20)

    # Проверка на ввод цифр, запятой и точки
    inp_filter = InputFilter(regex_string= r"^-?\d*[\.,]?\d*$",allow= True, replacement_string="")

    modelOrder = Dropdown(label="Порядок модели", options=[
        dropdown.Option("2"),
        dropdown.Option("3")],
        col={"md": 12},
        on_change=orderChanged,
        on_focus=removeIcon)

    a0 = TextField(label="a0", disabled=True,  keyboard_type=KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon, col={"md": 4})
    a1 = TextField(label="a1", disabled=True,  keyboard_type=KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon, col={"md": 4})
    a2 = TextField(label="a2", disabled=True,  keyboard_type=KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon, col={"md": 4})
    a3 = TextField(label="a3", disabled=True,  keyboard_type=KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon, col={"md": 6})
    b0 = TextField(label="b0", disabled=False, keyboard_type=KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon, col={"md": 6})

    title2 = Text("Ввод начальных условий", weight="bold", size=20)

    x0   = TextField(label="x(0)"  , disabled=True, keyboard_type=KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon, col={"md": 4})
    x_0  = TextField(label="x'(0)" , disabled=True, keyboard_type=KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon, col={"md": 4})
    x__0 = TextField(label="x''(0)", disabled=True, keyboard_type=KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon, col={"md": 4})

    title3 = Text("Выбор параметров", weight="bold", size=20)
    y_dropdown = Dropdown(label="y(t)", options=[
        dropdown.Option("1"),
        dropdown.Option("sin(t)")],
        width=200,
        on_focus=removeIcon,
        col={"md": 6}
    )
    interval = TextField(label="Интервал интегрирования", keyboard_type=KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon, col={"md": 6})

    def on_navBar_change(event):
        if event.control.selected_index == 0:
            # Первая страница
            page.controls = [lv, navBar]
        elif event.control.selected_index == 1:
            # Вторая страница
            # Переименовываем файл графика
            global graphChanged
            if graphChanged:
                global PATH_TO_GRAPh
                newpath = PATH_TO_GRAPh[:-4] + "_.png"
                rename(PATH_TO_GRAPh, newpath)
                PATH_TO_GRAPh = newpath

            # Поле для графика
            imageCard = Card(
                Container(
                    Column(
                        [
                            Text("График", weight="bold", size=20),
                            ResponsiveRow(
                                [
                                    Image(
                                        src=PATH_TO_GRAPh,
                                        col={"md": 12},
                                        height = 500
                                    )
                                ] 
                            )
                        ],
                    spacing=15
                    ),
                padding=20
                )        
            )
            page.controls = [imageCard, navBar]
            graphChanged = False
        elif event.control.selected_index == 2:
            # Третья страница
            global eqChanged
            if eqChanged:
                global path_to_eq1
                global path_to_eq2
                newpathToEq1 = path_to_eq1[:-4] + "_.png"
                newpathToEq2 = path_to_eq2[:-4] + "_.png"
                rename(path_to_eq1, newpathToEq1)
                rename(path_to_eq2, newpathToEq2)
                path_to_eq1 = newpathToEq1
                path_to_eq2 = newpathToEq2

            # Третья страница
            eqCard1 = Card(
                Container(
                    Column(
                        [
                            Text("Уравнение в обыкновенной форме", weight="bold", size=20),
                            ResponsiveRow(
                                [
                                    Image(
                                        src=path_to_eq1
                                    )
                                ],
                                spacing=15
                            )
                        ],
                        spacing=15
                    ),
                    padding=20
                )
            )
            eqCard2 = Card(
                Container(
                    Column(
                        [
                            Text("Уравнение в нормальной форме Коши", weight="bold", size=20),
                            ResponsiveRow(
                                [
                                    Image(src=path_to_eq2)
                                ],
                                spacing=15
                            )
                        ],
                        spacing=15
                    ),
                    padding=20
                )
            )
            page.controls = [eqCard1, eqCard2, navBar]

            eqChanged = False

        page.update()

    navBar = NavigationBar(
        destinations=[
            NavigationDestination(label="Параметры", icon=icons.EDIT_OUTLINED, selected_icon=icons.EDIT),
            NavigationDestination(label="График", icon=icons.AUTO_GRAPH),
            NavigationDestination(label="Уравнения", icon=icons.FUNCTIONS_OUTLINED, selected_icon=icons.FUNCTIONS)
        ],
        height=70,
        on_change=on_navBar_change
    )
    
    # Карточка с вводом информации о порядке модели
    card1 = Card(
        Container(
            Column(
                [
                    title1,
                    modelOrder,
                    ResponsiveRow(
                        [a0, a1, a2]
                    ),

                    ResponsiveRow(
                        [a3, b0]
                    )
                ],
                spacing=15
            ),
            padding=20
        )
    )

    # Карточка с вводом информации о начальных условиях
    card2 = Card(
        Container(
            Column(
                [
                    title2,
                    ResponsiveRow(
                        [x0, x_0, x__0]
                    )
                ],
                spacing=15
            ),
            padding=20
        )
    )

    # Карточка с вводом информации об интервале интегрирования
    card3 = Card(
        Container(
            Column(
                [
                    title3,
                    ResponsiveRow(
                        [y_dropdown, interval]
                    )
                ],
                spacing=15
            ),
            padding=20
        )
    )

    # Кнопка отправки
    button = Container(
        ResponsiveRow(
            [
                ElevatedButton(text="Отправить", on_click=sendData, icon=icons.SEND, height=50)
            ]
        )
    )

    # Пасхалка с авторами
    def openEgg(e):
        eggDialog = AlertDialog(
            modal=True,
            title=Text("Авторы"),
            content=Text("Колганов Роман\nПлюснин Савелий\nЕгоров Дмитрий\nГунько Данила"),
            actions=[
                TextButton("Спасибо", on_click=closeDialog),
            ]
        )

        page.dialog = eggDialog
        eggDialog.open = True
        page.update()
    
    egg = TextButton(on_click=openEgg, icon=icons.INFO_OUTLINE)

    lv = ListView(
        controls=[
            card1, card2, card3, button, egg],
        spacing=10,
        height=page.window_height - 70 - heightMinus,
    )
    
    page.add(lv, navBar)

def removeGraph():
    try:
        # Удалем все файлы в папке data
        for file in listdir("data"):
            remove("data\\" + file)

    except FileNotFoundError:
        pass

# Удаляем файл с графиком
removeGraph()

# Запускаем приложение
app(target=main)

removeGraph()
