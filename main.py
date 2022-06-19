#!/usr/bin/env python3

# Filename: pycalc.py

"""PyAlarm"""
import random
import sys
import pandas as pd

from functools import partial

# Import QApplication and required widgets from PyQt5.QtWidgets
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QStyle, QMessageBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

from alarm_widget import AlarmWidget
from power_bar import PowerBar

__version__ = "0.1"
__author__ = "Bradley"

ERROR_MSG = 'ERROR'
ApplicationName = 'PyAlarm'

"""
    TODO List
    0.5: accept time, message, dow select with class
    1: Add new Alarms with message and settings
    2: Save alarm (with pos)
    3: Edit alarm
    4: Delete Alarm
    5: Actual Alarm notifications and sound
    6:
    7:
    ..
    97: Bug-Fix - Time until alarm using dow
    98: Bonus - Global timer to reduce number of timers
    99: Bonus - Move Alarms around grid
"""


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


class KeyPressWidget(QWidget):
    keyPressed = QtCore.pyqtSignal(int)

    def keyPressEvent(self, event):
        super(KeyPressWidget, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())


# class AlarmWidget(QWidget):
#     def __init__(self):


# class PyAppUi(QMainWindow):
#     """PyApp's View (GUI)."""
#
#     def __init__(self):
#         """View initializer."""
#         super().__init__()
#         # Set some main window's properties
#         self.setWindowTitle(ApplicationName)
#         # self.setFixedSize(235, 235)
#         # Set the central widget and the general layout
#         self.generalLayout = QVBoxLayout()
#         self._centralWidget = QWidget(self)
#         self.setCentralWidget(self._centralWidget)
#         self._centralWidget.setLayout(self.generalLayout)
#         # Create the display and the buttons
#         self._createKeyDetect()
#         self._createDisplay()
#         self._createButtons()
#
#     def _createKeyDetect(self):
#         self.keyWidget = KeyPressWidget()
#         self.generalLayout.addWidget(self.keyWidget)
#         self.keyWidget.setFocus()
#
#     def _createDisplay(self):
#         """Create the display."""
#
#         self.labelLength = QLabel('Length')
#         self.displayLength = QLineEdit()
#         self.displayLength.setFixedSize(35, 35)
#         self.displayLength.setReadOnly(True)
#
#         self.statsLayout = QHBoxLayout()
#         self.statsLayout.addWidget(self.labelLength)
#         self.statsLayout.addWidget(self.displayLength)
#
#         self.generalLayout.addLayout(self.statsLayout)
#
#     def _createButtons(self):
#         """Create the buttons."""
#         # self.buttons = {}
#         # buttonsLayout = QGridLayout()
#         # # Button text | position on the QGridLayout
#         # buttons = ['a',
#         #            'b',
#         #            'c',
#         #            'd',
#         #            'e',
#         #            'f',
#         #            'g',
#         #            'h',
#         #            'i',
#         #            'j',
#         #            'k',
#         #            'l',
#         #            'm',
#         #            'n',
#         #            'o',
#         #            'p',
#         #            'q',
#         #            'r',
#         #            's',
#         #            't',
#         #            'u',
#         #            'v',
#         #            'w',
#         #            'x',
#         #            'y',
#         #            'z',
#         #            ]
#         # # Create the buttons and add them to the grid layout
#         # row = 0
#         # index = 0
#         # space = 0
#         # while index < 25:
#         #     # check number of remaining buttons
#         #     if 25 - index < 10:
#         #         rem = 25 - index
#         #         space = int(rem / 2)
#         #
#         #     for column in range(0, 10):
#         #         if index >= 26:
#         #             break
#         #         btnText = buttons[index]
#         #         self.buttons[btnText] = QPushButton(btnText.upper())
#         #         self.buttons[btnText].setFixedSize(40, 40)
#         #         buttonsLayout.addWidget(self.buttons[btnText], row, column + space)
#         #         index += 1
#         #
#         #     row += 1
#         #
#         # # Add buttonsLayout to the general layout
#         # self.generalLayout.addLayout(buttonsLayout)
#         #
#         # self.resetButton = QPushButton('Reset')
#         # self.resetButton.setFixedSize(50, 35)
#         # self.generalLayout.addWidget(self.resetButton, alignment=Qt.AlignCenter)
#
#     def setDisplayText(self, text):
#         self.displayLength.setText(text)
#
#     def getDisplayText(self):
#         return self.displayLength.text()
#
#     def displayWin(self):
#         self.gameOver = True
#         self.displayPopup('Congratulations!!\nYou have won!')
#
#     def displayPopup(self, message):
#         message += f'\n\nThe answer was: '
#         QMessageBox.question(self, 'Hangman', message, QMessageBox.Reset)
#
#     def reset(self):
#         self.keyWidget.setFocus()


# Create a Controller class to connect the GUI and the model
# class PyAppCtrl:
#     """PyCalc Controller class."""
#
#     def __init__(self, model, view):
#         """Controller initializer."""
#         self._evaluate = model
#         self._view = view
#         # Connect signals and slots
#         self._connectSignals()
#
#     def _checkWin(self):
#         for item in self._view.answers:
#             if not item['found']:
#                 return
#         self._view.displayWin()
#
#     def _checkKeyPress(self, key):
#         self._view.keyWidget.setFocus()
#         key = QKeySequence(key).toString()
#         if len(key) == 1 and key.isalpha():
#             print(key)
#
#     def _connectSignals(self):
#         """Connect signals and slots."""
#         # self._view.keyWidget.keyPressed.connect(self._checkKeyPress)
#         # self._view.resetButton.clicked.connect(self._view.resetGame)
#
#         # for btnText, btn in self._view.buttons.items():
#         #     if btnText not in {'='}:
#         #         btn.clicked.connect(partial(self._checkLetter, btnText))
#
#
# # Create a Model to handle the calculator's operation
# def evaluateExpression(expression):
#     """Evaluate an expression"""
#     try:
#         print(expression)
#         result = str(eval(expression, {}, {}))
#     except Exception:
#         result = ERROR_MSG
#
#     return result

class PyAppUi(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(PyAppUi, self).__init__(*args, **kwargs)

        self.setWindowTitle(ApplicationName)
        #         # self.setFixedSize(235, 235)
        #         # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.generalLayout.addWidget(AlarmWidget())
        self.generalLayout.addWidget(AlarmWidget())
        self.generalLayout.addWidget(AlarmWidget())

        self.show()


# Client code
def main():
    """Main function."""
    # Create an instance of QApplication
    app = QApplication(sys.argv)
    # Show the calculator's GUI
    # view = PyAppUi()
    # bar = PowerBar(["#49006a", "#7a0177", "#ae017e", "#dd3497", "#f768a1", "#fa9fb5", "#fcc5c0", "#fde0dd", "#fff7f3"])
    # bar.setBarPadding(2)
    # bar.setBarSolidPercent(0.9)
    # bar.setBackgroundColor('gray')
    # bar.show()

    # alarm = AlarmWidget()
    # alarm.show()

    view = PyAppUi()

    # Create instances of the model and the controller
    # model = evaluateExpression
    # PyAppCtrl(model=model, view=view)
    # Execute the calculator's main loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
