# importing libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import calendar
import datetime


class window(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Delivery Window Selector ")

        # setting geometry
        self.setGeometry(100, 100, 600, 400)

        #creating first label
        self.label_1 = QLabel('The start of your delivery Window will be:', self)
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

        # creating warning label
        self.label_1 = QLabel('', self)
        self.label_1.setFont(QFont('Arial', 12))
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.move(0, 375)
        self.label_1.resize(600, 20)

        # creating the data for the combo boxes
        self.month_list = list(calendar.month_name[1:])
        self.days_list = list()
        for day in range(1, 31):
            self.days_list.append(str(day))
        self.today = datetime.date.today()
        #days = calendar.monthrange(self.today.year, self.today.month)
        self.future = self.today + datetime.timedelta(days=31)
        self.month_list = [self.today.strftime('%B'), self.future.strftime('%B')]

        # creating the label of the current date
        self.label_1 = QLabel(str(self.today.strftime('%B')) + '/' + str(self.today.day) + '/' + str(self.today.year), self)
        self.label_1.setFont(QFont('Arial', 20))
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.move(0, 110)
        self.label_1.resize(600, 30)

        # creating the line of combo boxes
        self.combo_box_month = QComboBox(self)
        self.combo_box_month.setGeometry(35, 230, 290, 50)
        self.combo_box_month.addItems(['<Month>'])
        self.combo_box_month.addItems(self.month_list)

        self.label_1 = QLabel('/', self)
        self.label_1.setFont(QFont('Times New Roman', 50))
        self.label_1.move(335, 230)
        self.label_1.resize(50, 50)

        self.combo_box_day = QComboBox(self)
        self.combo_box_day.setGeometry(360, 230, 120, 50)
        self.combo_box_day.addItems(['<Day>'])

        self.label_1 = QLabel('/', self)
        self.label_1.setFont(QFont('Times New Roman', 50))
        self.label_1.move(490, 230)
        self.label_1.resize(50, 50)

        self.label_1 = QLabel(str(self.today.year), self)
        self.label_1.setFont(QFont('Arial', 20))
        self.label_1.move(510, 240)

        # calling the method
        self.combo_box_month.currentIndexChanged.connect(self.update_ui_components)

        # remove the error message
        self.combo_box_day.currentIndexChanged.connect(lambda x: self.label_1.setText(''))

        # creating a push button
        button = QPushButton("Confirm Date", self)

        # setting geometry of button
        button.setGeometry(250, 320, 100, 40)

        # adding action to a button
        button.clicked.connect(self.clicked_button)

        # creating warning label
        self.label_1 = QLabel('', self)
        self.label_1.setFont(QFont('Arial', 12))
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.move(0, 375)
        self.label_1.resize(600, 20)

        self.dates = list()

        self.show()


    def clicked_button(self):
        self.dates.append(str(self.combo_box_month.currentText()))
        self.dates.append(str(self.combo_box_day.currentText()))
        if not list(filter(lambda x: (x == '<Month>' or x == '<Day>'), self.dates)):
            self.close()
        else:
            self.label_1.setText('Please, select all values')
            self.dates.clear()


    def update_ui_components(self,index):
        data = [self.combo_box_month.itemText(index)]
        intersection = list(set(self.month_list).intersection(data))
        if intersection:
            if intersection[0] == self.month_list[0]:
                day_list = list()
                datetime_object = datetime.datetime.strptime(intersection[0], "%B")
                month_number = datetime_object.month
                days = calendar.monthrange(self.today.year, month_number)
                for day in range(self.today.day + 1, days[1] + 1):
                    day_list.append(str(day))
                self.combo_box_day.clear()
                self.combo_box_day.addItems(['<Day>'])
                self.combo_box_day.addItems(day_list)
                self.label_1.setText('')
            else:
                day_list = list()
                for day in range(1, self.future.day + 1):
                    day_list.append(str(day))
                    self.combo_box_day.clear()
                    self.combo_box_day.addItems(['<Day>'])
                    self.combo_box_day.addItems(day_list)
                    self.label_1.setText('')
        else:
            self.combo_box_day.clear()
            self.combo_box_day.addItems(['<Day>'])
            self.combo_box_month.currentIndexChanged.connect(self.update_ui_components)
            self.label_1.setText('')