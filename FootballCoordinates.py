import matplotlib.pyplot as plt
import csv
import os

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QTextEdit,
    QFileDialog,
    QHBoxLayout
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.FileName = ''
        self.SaveName = ''
        self.FieldLength = 4000
        self.FieldWidth = 2500

        self.setWindowTitle("Football coordinates")
        # self.setFixedSize(QSize(400, 300))

        self.layout = QVBoxLayout()

        # Field length
        # label
        label = QLabel("Enter the field length(m)")
        font = label.font()
        font.setPointSize(12)
        label.setFont(font)
        self.layout.addWidget(label)

        # spin box
        spinbox_l = QSpinBox()
        spinbox_l.setFixedSize(QSize(100, 20))
        spinbox_l.setValue(40)
        spinbox_l.setRange(1, 100)
        spinbox_l.setSingleStep(1)
        spinbox_l.valueChanged.connect(self.value_changed_length)
        self.layout.addWidget(spinbox_l)

        # Field width
        # label
        label = QLabel("Enter the field width(m)")
        font = label.font()
        font.setPointSize(12)
        label.setFont(font)
        self.layout.addWidget(label)

        # spin box
        spinbox_w = QSpinBox()
        spinbox_w.setFixedSize(QSize(100, 20))
        spinbox_w.setValue(30)
        spinbox_w.setRange(1, 100)
        spinbox_w.setSingleStep(1)
        spinbox_w.valueChanged.connect(self.value_changed_width)
        self.layout.addWidget(spinbox_w)

        # File data path
        # horizontal box
        h_layout = QHBoxLayout()

        # label
        label = QLabel("Choose data table")
        font = label.font()
        font.setPointSize(12)
        label.setFont(font)
        h_layout.addWidget(label)

        # button
        button = QPushButton("Find file")
        button.setCheckable(False)
        button.clicked.connect(self.get_file_name)
        h_layout.addWidget(button)
        self.layout.addLayout(h_layout)

        # text box
        self.myTextBox = QTextEdit(self)
        self.myTextBox.setMaximumSize(QSize(3000, 60))
        self.layout.addWidget(self.myTextBox)

        # File save path
        # horizontal box
        h_layout = QHBoxLayout()

        # label
        label = QLabel("Choose save folder")
        font = label.font()
        font.setPointSize(12)
        label.setFont(font)
        h_layout.addWidget(label)

        # button
        button = QPushButton("Find folder")
        button.setCheckable(False)
        button.clicked.connect(self.get_directory)
        h_layout.addWidget(button)
        self.layout.addLayout(h_layout)

        # text box
        self.my_directory = QTextEdit(self)
        self.my_directory.setMaximumSize(QSize(3000, 60))
        self.layout.addWidget(self.my_directory)

        # Start count
        # button
        start_button = QPushButton("Start")
        start_button.setCheckable(False)
        start_button.clicked.connect(self.start_button_was_clicked)
        start_button.setStyleSheet("background-color:rgb(0,128,255)")
        self.layout.addWidget(start_button)

        # central
        widget = QWidget()
        widget.setLayout(self.layout)

        self.setCentralWidget(widget)

    def start_button_was_clicked(self):
        print()
        print('Started')
        file_table = read_file(self.FileName)
        players_coordinates, players_indexes = create_players_coordinates(file_table)
        self.draw_images(players_coordinates, players_indexes)

    def value_changed_length(self, i):
        self.FieldLength = i * 100

    def value_changed_width(self, i):
        self.FieldWidth = i * 100

    def get_file_name(self):
        file_filter = 'Data file (*.csv)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Data file (*.csv)'
        )
        self.FileName = response[0]
        self.myTextBox.setText(response[0])

    def get_directory(self):
        response = QFileDialog.getExistingDirectory(
            self,
            caption='Select  a folder'
        )
        self.my_directory.setText(response)
        self.SaveName = response

    def draw_images(self, players_coordinates, players_indexes):
        color = ['red', 'green', 'blue', 'yellow', 'magenta']

        for player_index, player in enumerate(players_coordinates):
            # clear plot
            plt.clf()

            player_name = str()
            for key in players_indexes:
                if players_indexes[key] == player_index:
                    player_name = key
            print(player_name + ' processing...')
            for vector_index in range(1, len(player[0])):
                previous_x = player[0][vector_index - 1]
                previous_y = player[1][vector_index - 1]
                current_x = player[0][vector_index]
                current_y = player[1][vector_index]
                current_color = 'black'
                if player_index < len(color):
                    current_color = color[player_index]
                plt.arrow(previous_x, previous_y, current_x - previous_x, current_y - previous_y, color=current_color)
            plt.xlim(0, self.FieldLength)
            plt.ylim(0, self.FieldWidth)
            plt.title(player_name)
            plt.grid()
            plt.draw()

            # Save image
            plt.savefig(self.SaveName + '/' + player_name + '.png', dpi=800)
            # plt.show()

        print('Finished')
        print('(￣▽￣)ノ')


def show_window():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


def create_players_coordinates(table):
    item_name = 2
    item_x = 5
    item_y = 6

    out_array = []
    players_id = dict()

    for index in range(1, len(table)):
        row = table[index]

        if row[item_name] in players_id:  # if player id was already added
            arr_index = players_id[row[item_name]]
            out_array[arr_index][0].append(int(row[item_x]))
            out_array[arr_index][1].append(int(row[item_y]))
        else:  # if player it is first player id
            out_array.append([[int(row[item_x])], [int(row[item_y])]])
            players_id[row[item_name]] = len(out_array) - 1

    return out_array, players_id


def read_file(file_name):
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


if __name__ == '__main__':
    show_window()
