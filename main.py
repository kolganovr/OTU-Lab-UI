import flet
import re
from Equation import LastEquation
from Equation import DifferentialEquationSystem
from flet import ElevatedButton, Page, Text, TextField, icons, Dropdown
import numpy as np


def main(page: Page):
    page.title = "Лабораторная работа №1"
    page.window_width = 900
    page.window_height = 900


    def check_input(e):
        input_value = e.control.value
        pattern = r'^[0-9,.-]+$'
        if(re.search(pattern, input_value) == False):
            e.control.error_text = "input numbers!"
        else:
            e.control.error_text = ""
        page.update()


    # Функция отправки введенный данных для вычисления
    def sendData(e):
        t.value = (
            f"Textboxes values are: Order = {modelOrder.value}, a0 = {a0.value}, a1 = {a1.value}, a2 = {a2.value}, a3 = {a3.value}, b0 = {b0.value}, x0 = {x0.value}, x_0 = {x_0.value}, x__0 = {x__0.value}"
        )
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

    title1 = Text("Ввод порядка модели", weight="bold", size=20)
    t = Text()
    # Проверка на ввод цифр, запятой и точки
    inp_filter = flet.InputFilter(regex_string= r"^-?\d*[\.,]?\d*$",allow= True, replacement_string="")

    modelOrder = Dropdown(label="Порядок модели", options=[
        flet.dropdown.Option("2"),
        flet.dropdown.Option("3")], 
        width=200, on_change=orderChanged)
    
    a0 = TextField(label="a0",disabled=True, keyboard_type=flet.KeyboardType.NUMBER, input_filter= inp_filter)
    a1 = TextField(label="a1", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, input_filter= inp_filter, on_change= check_input)
    a2 = TextField(label="a2", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, input_filter= inp_filter)
    a3 = TextField(label="a3", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, input_filter= inp_filter)
    b0 = TextField(label="b0", disabled=False, keyboard_type=flet.KeyboardType.NUMBER, input_filter= inp_filter)

    title2 = Text("Ввод начальных условий", weight="bold", size=20)

    x0 = TextField(label="x(0)", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, input_filter= inp_filter)
    x_0 = TextField(label="x'(0)", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, input_filter= inp_filter)
    x__0 = TextField(label="x''(0)", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, input_filter= inp_filter)

    title3 = Text("Выбор y(t)", weight="bold", size=20)
    y_dropdown = Dropdown(label="y(t)", options=[
        flet.dropdown.Option("1"),
        flet.dropdown.Option("sin(t)")], width=200)


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


    # if(modelOrder == 3):
    #     last_equation = LastEquation(3, a0, a1, a2, a3, b0)
    # else:
    #     last_equation = LastEquation(2, a0, a1, a2, None, b0)

    # x0 = [x0, x_0, x__0]  # начальные условия
    # t_span = [0, 20]  # интервал интегрирования


    sendData = ElevatedButton(text="Отправить", on_click=sendData, icon=icons.SEND)

    # page.add(
    #     flet.DataTable(
    #         columns = [
    #             flet.DataColumn(title1),
    #             flet.DataColumn(title2),
    #             flet.DataColumn(title3)
    #         ],
    #         rows=[
    #             flet.DataRow(
    #                 cells=[
    #                     flet.DataCell(a0),
    #                     flet.DataCell(x0),
    #                     flet.DataCell(y_dropdown)
    #                 ]
    #             ),
    #             flet.DataRow(
    #                 cells=[
    #                     flet.DataCell(a1),
    #                     flet.DataCell(x_0)
    #                 ]
    #             ),
    #             flet.DataRow(
    #                 cells=[
    #                     flet.DataCell(a2),
    #                     flet.DataCell(x__0)
    #                 ]
    #             ),
    #             flet.DataRow(
    #                 cells=[
    #                     flet.DataCell(a3)
    #                 ]
    #             ),
    #             flet.DataRow(
    #                 cells=[
    #                     flet.DataCell(b0)
    #                 ]
    #             )
    #         ]
    #     ),
    #     sendData
    # )



    # Расставляем элементы на странице
    page.add(title1, modelOrder, a0, a1, a2, a3, b0, title2, x0, x_0, x__0,title3, y_dropdown, sendData, t)

# Запускаем приложение
flet.app(target=main)
