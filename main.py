import matplotlib.pyplot as plt
from Solve import Solver, LastEquation
from flet import (
    # Layout controls
    Page, Container, Column, ResponsiveRow, Card,
    # Input controls
    TextField, Dropdown, dropdown, InputFilter, KeyboardType,
    # Button controls
    ElevatedButton, Text, TextButton, icons,
    # Dialogs
    AlertDialog,
    # Other
    app
)
import numpy as np # Нужно импортить только нужное

# Функция для решения системы 2 порядка
def func(t, x, y, last_equation: LastEquation):
    if(y == "1"):
        y_param = 1
    else:
        y_param = math.sin(t)

    if(last_equation.n == 2):
        dxdt = np.zeros(2)
        dxdt[0] = x[1]
        dxdt[1] = (1 / last_equation.a_2) * (last_equation.b_0*y_param - last_equation.a_1*x[1] - last_equation.a_0*x[0])
        return dxdt
    else:
        dxdt = np.zeros(3)
        dxdt[0] = x[1]
        dxdt[1] = x[2]
        dxdt[2] = (1 / last_equation.a_3) * (last_equation.b_0*y_param - last_equation.a_2*x[2] - last_equation.a_1*x[1] - last_equation.a_0*x[0])
        return dxdt

def main(page: Page):
    page.title = "Лабораторная работа №1"
    page.window_width = 900
    page.window_height = 730

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
            fieldsToCheck = ['a0', 'a1', 'a2', 'x0', 'x_0']
            for field in fieldsToCheck:
                if not fields[field].value:
                    problemFields.append(fields[field])

        elif modelOrder.value == "3":
            fieldsToCheck = ['a0', 'a1', 'a2', 'a3', 'b0', 'x0', 'x_0', 'x__0']
            for field in fieldsToCheck:
                if not fields[field].value:
                    problemFields.append(fields[field])

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
            return

    # Функция отправки введенный данных для вычисления
    def sendData(e):
        # Валидация данных на предмет заполненности полей
        validateData()
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
        t_span = [0, int(interval.value)]
        # Составление системы для решения
        system = Solver(func, y0, t_span, y_parametr, lastEquation)
        # Решение системы
        solution = system.solve()
        # Вывод графиков
        if(lastEquation.n == 3):
            plt.plot(solution.t, solution.y[0], label='x(t)')
            plt.plot(solution.t, solution.y[1], label="x'(t)")
            plt.plot(solution.t, solution.y[2], label="x''(t)")
            plt.xlabel('t')
            plt.ylabel('x')
            plt.legend()
            plt.show()
        else:
            plt.plot(solution.t, solution.y[0], label='x(t)')
            plt.plot(solution.t, solution.y[1], label="x'(t)")
            plt.xlabel('t')
            plt.ylabel('x')
            plt.legend()
            plt.show()

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


    def func_3(t, x, y, last_equation: LastEquation):
        dxdt = np.zeros(3)
        dxdt[0] = x[1]
        dxdt[1] = x[2]
        dxdt[2] = (1 / last_equation.a_3) * (last_equation.b_0*y - last_equation.a_2*x[2] - last_equation.a_1*x[1] - last_equation.a_0*x[0])
        return dxdt

    def func_2(t, x, y, last_equation: LastEquation):
        dxdt = np.zeros(2)
        dxdt[0] = x[1]
        dxdt[1] = (1 / last_equation.a_2) * (last_equation.b_0*y - last_equation.a_1*x[1] - last_equation.a_0*x[0])

    sendDataButton = ElevatedButton(text="Отправить", on_click=sendData, icon=icons.SEND, height=50)

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
                sendDataButton
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

    page.add(card1, card2, card3, button, TextButton(on_click=openEgg, icon=icons.INFO_OUTLINE))

# Запускаем приложение
app(target=main)
