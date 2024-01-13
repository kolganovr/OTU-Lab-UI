import flet
from flet import ElevatedButton, Page, Text, TextField, icons

def main(page: Page):
    page.title = "Лабораторная работа №1"
    page.window_width = 500
    page.window_height = 850

    # Функция отправки введенный данных для вычисления
    def sendData(e):
        t.value = (
            f"Textboxes values are: Order = {modelOrder.value}, a0 = {a0.value}, a1 = {a1.value}, a2 = {a2.value}, a3 = {a3.value}, x0 = {x0.value}, x_0 = {x_0.value}, x__0 = {x__0.value}"
        )
        page.update()
    
    def orderChanged(e):
        aFields = [a0, a1, a2, a3]
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
    
    title1 = Text("Вариатны параметров модели", weight="bold", size=30)
    t = Text()
    modelOrder = TextField(label="Порядок модели", on_change=orderChanged)
    a0 = TextField(label="a0", disabled=True)
    a1 = TextField(label="a1", disabled=True)
    a2 = TextField(label="a2", disabled=True)
    a3 = TextField(label="a3", disabled=True)
    b1 = TextField(label="b1")

    title2 = Text("Варианты начальных условий", weight="bold", size=30)
    x0 = TextField(label="x(0)", disabled=True)
    x_0 = TextField(label="x'(0)", disabled=True)
    x__0 = TextField(label="x''(0)", disabled=True)
    sendData = ElevatedButton(text="Отправить", on_click=sendData, icon=icons.SEND)

    # Расставляем элементы на странице
    page.add(title1, modelOrder, a0, a1, a2, a3, b1, title2, x0, x_0, x__0, sendData, t)

# Запускаем приложение
flet.app(target=main)