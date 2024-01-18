import flet
import re
from Equation import LastEquation
from Equation import DifferentialEquationSystem
from flet import ElevatedButton, Page, Text, TextField, icons, Dropdown
import numpy as np


def main(page: Page):
    page.title = "Лабораторная работа №1"
    page.window_width = 900
    page.window_height = 970

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

            # Функция для закрытия диалогового окна
            def closeDialog(e):
                page.dialog.open = False
                page.update()
            
            # Создание диалогового окна с ошибкой
            errorDialog = flet.AlertDialog(
                modal=True,
                title=Text("Ошибка ввода данных"),
                content=Text("Заполнены не все необходимые поля"),
                actions=[
                    flet.TextButton("OK", on_click=closeDialog),
                ],
                actions_alignment=flet.MainAxisAlignment.END,
            )

            page.dialog = errorDialog
            errorDialog.open = True
            page.update()
            return

    # Функция отправки введенный данных для вычисления
    def sendData(e):
        # Валидация данных на предмет заполненности полей
        validateData()
        
        text = ''
        for key, value in fields.items():
            if value.value:
                text += f'{key}: {value.value}, '
        t.value = text[:-2]

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
    t = Text()

    # Проверка на ввод цифр, запятой и точки
    inp_filter = flet.InputFilter(regex_string= r"^-?\d*[\.,]?\d*$",allow= True, replacement_string="")

    modelOrder = Dropdown(label="Порядок модели", options=[
        flet.dropdown.Option("2"),
        flet.dropdown.Option("3")], 
        width=200, 
        on_change=orderChanged, 
        on_focus=removeIcon)
    
    a0 = TextField(label="a0", disabled=True,  keyboard_type=flet.KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon)
    a1 = TextField(label="a1", disabled=True,  keyboard_type=flet.KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon)
    a2 = TextField(label="a2", disabled=True,  keyboard_type=flet.KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon)
    a3 = TextField(label="a3", disabled=True,  keyboard_type=flet.KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon)
    b0 = TextField(label="b0", disabled=False, keyboard_type=flet.KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon)

    title2 = Text("Ввод начальных условий", weight="bold", size=20)

    x0   = TextField(label="x(0)"  , disabled=True, keyboard_type=flet.KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon)
    x_0  = TextField(label="x'(0)" , disabled=True, keyboard_type=flet.KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon)
    x__0 = TextField(label="x''(0)", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon)

    title3 = Text("Выбор параметров", weight="bold", size=20)
    y_dropdown = Dropdown(label="y(t)", options=[
        flet.dropdown.Option("1"),
        flet.dropdown.Option("sin(t)")], 
        width=200, 
        on_focus=removeIcon
    )
    interval = TextField(label="Интервал интегрирования", keyboard_type=flet.KeyboardType.NUMBER, input_filter=inp_filter, on_focus=removeIcon)


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

    sendDataButton = ElevatedButton(text="Отправить", on_click=sendData, icon=icons.SEND)

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
    #     sendDataButton
    # )

    # Расставляем элементы на странице
    page.add(title1, modelOrder, a0, a1, a2, a3, b0, title2, x0, x_0, x__0,title3, y_dropdown, interval, sendDataButton, t)

# Запускаем приложение
flet.app(target=main)