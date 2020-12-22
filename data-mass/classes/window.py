# importing libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import calendar
import datetime


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Delivery Window Selector ")

        # setting geometry
        self.setGeometry(100, 100, 600, 400)

        #creating first label
        self.label_1 = QLabel('Select the start date of the delivery window:', self)
        # setting font and size
        self.label_1.setFont(QFont('Arial', 15))
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.move(0, 50)
        self.label_1.resize(600, 20)

        # creating second label
        self.label_1 = QLabel('Select the end date of the delivery window:', self)
        # setting font and size
        self.label_1.setFont(QFont('Arial', 15))
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.move(0, 190)
        self.label_1.resize(600, 20)

        # creating label
        self.label_1 = QLabel('', self)
        self.label_1.setFont(QFont('Arial', 12))
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.move(0, 375)
        self.label_1.resize(600, 20)

        #creating the first line of comboboxes
        year_list = list()
        today = datetime.date.today()
        current_year = today.year
        year_list.append('<Year>')
        for y in range(11):
            year_list.append(str(current_year + y))
        self.combo_box_year = QComboBox(self)
        self.combo_box_year.setGeometry(10, 90, 325, 50)
        self.combo_box_year.addItems(year_list)

        self.combo_box_month = QComboBox(self)
        self.combo_box_month.setGeometry(360, 90, 120, 50)
        self.combo_box_month.addItems(['<Month>'])

        self.combo_box_day = QComboBox(self)
        self.combo_box_day.setGeometry(505, 90, 80, 50)
        self.combo_box_day.addItems(['<Day>'])

        #creating second line of comboboxes
        year_list = list()
        self.combo_box_year_second = QComboBox(self)
        self.combo_box_year_second.addItems(['<Year>'])
        self.combo_box_year_second.setGeometry(10, 230, 325, 50)
        self.combo_box_year_second.addItems(year_list)

        self.combo_box_month_second = QComboBox(self)
        self.combo_box_month_second.setGeometry(360, 230, 120, 50)
        self.combo_box_month_second.addItems(['<Month>'])

        self.combo_box_day_second = QComboBox(self)
        self.combo_box_day_second.setGeometry(505, 230, 80, 50)
        self.combo_box_day_second.addItems(['<Day>'])

        # calling method
        self.combo_box_year.currentIndexChanged.connect(self.UiUpdateComponents_year)

        # remove the error message
        self.combo_box_day_second.currentIndexChanged.connect(lambda x: self.label_1.setText(''))

        # creating a push button
        button = QPushButton("Confirm Dates", self)

        # setting geometry of button
        button.setGeometry(250, 320, 100, 40)

        # adding action to a button
        button.clicked.connect(self.clicked_button)

        self.dates = list()

        self.show()

    def clicked_button(self):
        self.dates.append(str(self.combo_box_year.currentText()))
        self.dates.append(str(self.combo_box_month.currentText()))
        self.dates.append(str(self.combo_box_day.currentText()))
        self.dates.append(str(self.combo_box_year_second.currentText()))
        self.dates.append(str(self.combo_box_month_second.currentText()))
        self.dates.append(str(self.combo_box_day_second.currentText()))
        if not list(filter(lambda x: (x == '<Year>' or x == '<Month>' or x == '<Day>'), self.dates)):
            self.close()
        else:
            self.label_1.setText('Please, select all values')
            self.dates.clear()


    def UiUpdateComponents_year(self, index):
        # populating a combo box widget
        month_list = list()
        today = datetime.date.today()
        current_year = today.year
        data = self.combo_box_year.itemText(index)
        months_list = list(calendar.month_name[1:])
        if str(data) != '<Year>':
            if int(data) == current_year:
                current_month = today.month
                for month in range(current_month, 13):
                    month_list.append(calendar.month_name[month])
                self.combo_box_month.clear()
                self.combo_box_month.addItems(['<Month>'])
                self.combo_box_month.addItems(month_list)
                self.combo_box_day.clear()
                self.combo_box_day.addItems(['<Day>'])
                self.combo_box_month.currentIndexChanged.connect(self.UiUpdateComponents_month)
                self.label_1.setText('')
            elif int(data) > current_year:
                self.combo_box_month.clear()
                self.combo_box_month.addItems(['<Month>'])
                self.combo_box_month.addItems(months_list)
                self.combo_box_day.clear()
                self.combo_box_day.addItems(['<Day>'])
                self.combo_box_month.currentIndexChanged.connect(self.UiUpdateComponents_month)
                self.label_1.setText('')
        else:
            self.combo_box_month.clear()
            self.combo_box_month.addItems(['<Month>'])
            self.combo_box_day.clear()
            self.combo_box_day.addItems(['<Day>'])
            self.combo_box_month_second.clear()
            self.combo_box_month_second.addItems(['<Month>'])
            self.combo_box_day_second.clear()
            self.combo_box_day_second.addItems(['<Day>'])
            self.combo_box_year_second.clear()
            self.combo_box_year_second.addItems(['<Year>'])
            self.combo_box_year.currentIndexChanged.connect(self.UiUpdateComponents_year)


    def UiUpdateComponents_month(self, index):
        month_list = list()
        month_list.append(str(self.combo_box_month.itemText(index)))
        months_list = list(calendar.month_name[1:])
        intersection = list(set(months_list).intersection(month_list))
        if intersection:
            datetime_object = datetime.datetime.strptime(intersection[0], "%B")
            month_number = datetime_object.month
            day_list = list()
            today = datetime.date.today()
            current_year = today.year
            current_month = calendar.month_name[today.month]
            current_day = today.day
            year = str(self.combo_box_year.currentText())
            if intersection[0] == 'February':
                datetime_object = datetime.datetime.strptime(intersection[0], "%B")
                month_number = datetime_object.month
                days = calendar.monthrange(int(year), month_number)
                for day in range(1, days[1] + 1):
                    day_list.append(str(day))
                self.combo_box_day.clear()
                self.combo_box_day.addItems(['<Day>'])
                self.combo_box_day.addItems(day_list)
                self.combo_box_day.currentIndexChanged.connect(self.UiUpdateComponents_year_second)
                self.label_1.setText('')
            elif intersection[0] == current_month or (intersection[0] == current_month and year == current_year):
                datetime_object = datetime.datetime.strptime(intersection[0], "%B")
                month_number = datetime_object.month
                days = calendar.monthrange(current_year, month_number)
                for day in range(current_day, days[1] + 1):
                    day_list.append(str(day))
                self.combo_box_day.clear()
                self.combo_box_day.addItems(['<Day>'])
                self.combo_box_day.addItems(day_list)
                self.combo_box_day.currentIndexChanged.connect(self.UiUpdateComponents_year_second)
                self.label_1.setText('')
            else:
                year = str(self.combo_box_year.currentText())
                days = calendar.monthrange(int(year), month_number)
                for day in range(1, days[1] + 1):
                    day_list.append(str(day))
                self.combo_box_day.clear()
                self.combo_box_day.addItems(['<Day>'])
                self.combo_box_day.addItems(day_list)
                self.combo_box_day.currentIndexChanged.connect(self.UiUpdateComponents_year_second)
                self.label_1.setText('')
        else:
            self.combo_box_month.currentIndexChanged.connect(self.UiUpdateComponents_month)


    def UiUpdateComponents_year_second(self):
        data = str(self.combo_box_year.currentText())
        year_list = list()
        today = datetime.date.today()
        current_year = today.year
        year_list.append('<Year>')
        if data != '<Year>' and str(self.combo_box_month.currentText()) != '<Month>' and str(self.combo_box_day.currentText()) != '<Day>':
            for y in range(11):
                if str(self.combo_box_month.currentText()) == 'December' and int(self.combo_box_day.currentText()) > 26:
                    if int(data) < (current_year + y):
                        year_list.append(str(current_year + y))
                else:
                    if int(data) <= (current_year + y):
                        year_list.append(str(current_year + y))
            self.combo_box_year_second.clear()
            self.combo_box_year_second.addItems(year_list)
            self.combo_box_year_second.currentIndexChanged.connect(self.UiUpdateComponents_month_second)
            self.label_1.setText('')
        else:
            self.combo_box_year.currentIndexChanged.connect(self.UiUpdateComponents_year)



    def UiUpdateComponents_month_second(self, index):
        data = self.combo_box_year_second.itemText(index)
        if str(data) != str(self.combo_box_year_second.itemText(0)):
            month_list = list()
            selected_year = int(self.combo_box_year.currentText())
            months_list = list(calendar.month_name[1:])
            if int(data) == selected_year:
                selected_month = self.combo_box_month.currentText()
                datetime_object = datetime.datetime.strptime(selected_month, "%B")
                month_number = datetime_object.month
                selected_day = int(self.combo_box_day.currentText())
                days = calendar.monthrange(int(selected_year), month_number)
                if (selected_day + 5) < days[1]:
                    for month in range(month_number, 13):
                        month_list.append(calendar.month_name[month])
                    self.combo_box_month_second.clear()
                    self.combo_box_month_second.addItems(['<Month>'])
                    self.combo_box_month_second.addItems(month_list)
                    self.combo_box_day_second.clear()
                    self.combo_box_day_second.addItems(['<Day>'])
                    self.combo_box_month_second.currentIndexChanged.connect(self.UiUpdateComponents_day_second)
                    self.label_1.setText('')
                else:
                    for month in range(month_number + 1, 13):
                        month_list.append(calendar.month_name[month])
                    self.combo_box_month_second.clear()
                    self.combo_box_month_second.addItems(['<Month>'])
                    self.combo_box_month_second.addItems(month_list)
                    self.combo_box_day_second.clear()
                    self.combo_box_day_second.addItems(['<Day>'])
                    self.combo_box_month_second.currentIndexChanged.connect(self.UiUpdateComponents_day_second)
                    self.label_1.setText('')
            elif int(data) > selected_year:
                self.combo_box_month_second.clear()
                self.combo_box_month_second.addItems(['<Month>'])
                self.combo_box_month_second.addItems(months_list)
                self.combo_box_day_second.clear()
                self.combo_box_day_second.addItems(['<Day>'])
                self.combo_box_month_second.currentIndexChanged.connect(self.UiUpdateComponents_day_second)
                self.label_1.setText('')
        else:
            self.combo_box_year_second.currentIndexChanged.connect(self.UiUpdateComponents_month_second)


    def UiUpdateComponents_day_second(self, index):
        month_list = list()
        month_list.append(self.combo_box_month_second.itemText(index))
        months_list = list(calendar.month_name[1:])
        intersection = list(set(months_list).intersection(month_list))
        if intersection:
            datetime_object = datetime.datetime.strptime(intersection[0], "%B")
            month_number = datetime_object.month
            day_list = list()
            selected_year = self.combo_box_year.currentText()
            selected_month = str(self.combo_box_month.currentText())
            datetime_object_selected = datetime.datetime.strptime(selected_month, "%B")
            month_number_selected = datetime_object_selected.month
            selected_day = int(self.combo_box_day.currentText())
            days = calendar.monthrange(int(selected_year), month_number_selected)
            if str(month_number) == str((month_number_selected + 1) and selected_day > (days[1]-5)) or (intersection[0] == 'January' and selected_month == 'December' and int(selected_year) == (int(self.combo_box_year_second.currentText()) - 1)):
                for day in range(6 - (days[1] - selected_day), days[1] + 1):
                    day_list.append(str(day))
                self.combo_box_day_second.clear()
                self.combo_box_day_second.addItems(['<Day>'])
                self.combo_box_day_second.addItems(day_list)
                self.label_1.setText('')
            elif str(intersection[0]) == selected_month and str(self.combo_box_year.currentText()) == str(self.combo_box_year_second.currentText()):
                for day in range(selected_day + 5, days[1] + 1):
                    day_list.append(str(day))
                self.combo_box_day_second.clear()
                self.combo_box_day_second.addItems(['<Day>'])
                self.combo_box_day_second.addItems(day_list)
                self.label_1.setText('')
            elif intersection[0] == 'February':
                datetime_object = datetime.datetime.strptime(intersection[0], "%B")
                month_number = datetime_object.month
                year = str(self.combo_box_year_second.currentText())
                days = calendar.monthrange(int(year), month_number)
                for day in range(1, days[1] + 1):
                    day_list.append(str(day))
                self.combo_box_day_second.clear()
                self.combo_box_day_second.addItems(['<Day>'])
                self.combo_box_day_second.addItems(day_list)
                self.label_1.setText('')
            else:
                year = str(self.combo_box_year_second.currentText())
                days = calendar.monthrange(int(year), month_number)
                for day in range(1, days[1] + 1):
                    day_list.append(str(day))
                self.combo_box_day_second.clear()
                self.combo_box_day_second.addItems(['<Day>'])
                self.combo_box_day_second.addItems(day_list)
                self.label_1.setText('')
        else:
            self.combo_box_month_second.currentIndexChanged.connect(self.UiUpdateComponents_day_second)