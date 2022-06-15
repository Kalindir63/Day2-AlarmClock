#!/usr/bin/env python3

# Filename: pycalc.py

"""PyCalc is a simple calculator build using Python and PyQt5"""
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

__version__ = "0.1"
__author__ = "Bradley"

ERROR_MSG = 'ERROR'
ApplicationName = 'PyHangman'


# words_to_guess = ["january", "border", "image", "film", "promise", "kids", "lungs", "doll", "rhyme", "damage",
#                   "plants", "hangman"]


def getWordsToGuess():
    p = 0.05
    filename = 'words-main/data/oxford-5k.csv'
    words = pd.read_csv(
        filename,
        header=0,
        skiprows=lambda i: i > 0 and random.random() > p,
        usecols=[0]
    ).T.values[0]
    # print(list(words))
    return list(words)


words_to_guess = getWordsToGuess()


def getHangingManImage(level):
    hangingMan = ["   _____ \n" +
                  "  |      \n" +
                  "  |      \n" +
                  "  |      \n" +
                  "  |      \n" +
                  "  |      \n" +
                  "  |      \n" +
                  "__|__\n",
                  "   _____ \n" +
                  "  |     |\n" +
                  "  |      \n" +
                  "  |      \n" +
                  "  |      \n" +
                  "  |      \n" +
                  "  |      \n" +
                  "__|__\n",
                  "   _____ \n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |      \n" +
                  "  |      \n" +
                  "  |      \n" +
                  "  |      \n" +
                  "__|__\n",
                  "   _____ \n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |      \n" +
                  "  |      \n" +
                  "  |      \n" +
                  "__|__\n",
                  "   _____ \n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |     O\n" +
                  "  |      \n" +
                  "  |      \n" +
                  "__|__\n",
                  "   _____ \n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |     O\n" +
                  "  |     |\n" +
                  "  |      \n" +
                  "__|__\n",
                  "   _____ \n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |     O\n" +
                  "  |    /|\n" +
                  "  |      \n" +
                  "__|__\n",
                  "   _____ \n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |     O\n" +
                  "  |    /|\\\n" +
                  "  |      \n" +
                  "__|__\n",
                  "   _____ \n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |     O\n" +
                  "  |    /|\\\n" +
                  "  |    / \n" +
                  "__|__\n",
                  "   _____ \n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |     |\n" +
                  "  |     O\n" +
                  "  |    /|\\\n" +
                  "  |    / \\\n" +
                  "__|__\n"
                  ]
    if level >= len(hangingMan):
        return hangingMan[len(hangingMan) - 1]
    return hangingMan[level]


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


class PyAppUi(QMainWindow):
    """PyCalc's View (GUI)."""

    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle(ApplicationName)
        self.defaultGuesses = 9
        self.guessesLeft = self.defaultGuesses
        self.guessCount = 0
        self.gameOver = False
        self.answer = ''
        self.answers = []
        # self.setFixedSize(235, 235)
        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create the display and the buttons
        self._createHangingMan()
        self._createAnswerLayout()
        self._createDisplay()
        self._createButtons()
        self.setDisplayLength()

    def _createHangingMan(self):

        # hangingManLayout = QGridLayout()
        # hangingManLayout.columnCount()

        # self.generalLayout.addLayout(hangingManLayout)
        hangmanFont = QFont('Consolas')
        # hangmanFont.setUnderline(True)
        hangmanFont.setPixelSize(20)

        self.labelHangingMan = QLabel(getHangingManImage(self.guessCount))
        self.labelHangingMan.setFont(hangmanFont)
        self.generalLayout.addWidget(self.labelHangingMan, alignment=Qt.AlignCenter)

    def updateHangingMan(self):
        self.labelHangingMan.setText(getHangingManImage(self.guessCount))

    def _createAnswerLayout(self):
        self.answerLayout = QHBoxLayout()
        self.answerLayout.setAlignment(Qt.AlignCenter)

        self._chooseNewAnswer()
        self.setAnswerLayout()
        self.generalLayout.addLayout(self.answerLayout)

    def _chooseNewAnswer(self):
        while True:
            word = random.choice(words_to_guess)
            if word != self.answer or len(words_to_guess) <= 1:
                break
        print(word)
        self.answer = word

    def setAnswerLayout(self):
        answerFont = QFont()
        answerFont.setUnderline(True)
        answerFont.setPixelSize(35)

        clearLayout(self.answerLayout)
        self.answers = []
        for letterIdx in range(0, len(self.answer)):
            # self.buttons[btnText] = QPushButton(btnText.upper())
            # self.answers[letter] = QLabel(letter.upper())
            ans = {'label': QLabel(' ')}

            answerFont.setUnderline(self.answer[letterIdx] != ' ')
            ans['label'].setFont(answerFont)
            ans['label'].setFixedSize(35, 35)

            ans['text'] = self.answer[letterIdx]
            ans['found'] = self.answer[letterIdx] == ' '

            self.answers.append(ans)
            self.answerLayout.addWidget(self.answers[letterIdx]['label'])

    def _createDisplay(self):
        """Create the display."""
        # Create the display widget
        self.keyWidget = KeyPressWidget()
        self.generalLayout.addWidget(self.keyWidget)
        self.keyWidget.setFocus()

        self.labelLength = QLabel('Length')
        self.displayLength = QLineEdit()
        self.displayLength.setFixedSize(35, 35)
        self.displayLength.setReadOnly(True)

        self.labelGuessLeft = QLabel('Guess Left')
        self.displayGuessLeft = QLineEdit(str(self.guessesLeft))
        self.displayGuessLeft.setFixedSize(35, 35)
        self.displayGuessLeft.setReadOnly(True)

        self.labelWrongGuess = QLabel('Wrong Guess')
        self.displayWrongGuess = QLineEdit()
        self.displayWrongGuess.setFixedHeight(35)
        self.displayWrongGuess.setReadOnly(True)

        self.statsLayout = QHBoxLayout()
        self.statsLayout.addWidget(self.labelLength)
        self.statsLayout.addWidget(self.displayLength)

        self.statsLayout.addWidget(self.labelGuessLeft)
        self.statsLayout.addWidget(self.displayGuessLeft)

        self.statsLayout.addWidget(self.labelWrongGuess)
        self.statsLayout.addWidget(self.displayWrongGuess)

        self.generalLayout.addLayout(self.statsLayout)

        # Add the display to the general layout
        # self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = ['a',
                   'b',
                   'c',
                   'd',
                   'e',
                   'f',
                   'g',
                   'h',
                   'i',
                   'j',
                   'k',
                   'l',
                   'm',
                   'n',
                   'o',
                   'p',
                   'q',
                   'r',
                   's',
                   't',
                   'u',
                   'v',
                   'w',
                   'x',
                   'y',
                   'z',
                   ]
        # Create the buttons and add them to the grid layout
        row = 0
        index = 0
        space = 0
        while index < 25:
            # check number of remaining buttons
            if 25 - index < 10:
                rem = 25 - index
                space = int(rem / 2)

            for column in range(0, 10):
                if index >= 26:
                    break
                btnText = buttons[index]
                self.buttons[btnText] = QPushButton(btnText.upper())
                self.buttons[btnText].setFixedSize(40, 40)
                buttonsLayout.addWidget(self.buttons[btnText], row, column + space)
                index += 1

            row += 1

        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)

        self.resetButton = QPushButton('Reset')
        self.resetButton.setFixedSize(50, 35)
        self.generalLayout.addWidget(self.resetButton, alignment=Qt.AlignCenter)

    def setDisplayWrongGuessText(self, text):
        if self.gameOver:
            return
        self.displayWrongGuess.setText(text)
        self.setGuessesLeft()

    def displayWrongGuessText(self):
        return self.displayWrongGuess.text()

    def setGuessesLeft(self):
        if self.guessesLeft <= 0:
            self.displayLoss()
            return
        self.guessesLeft -= 1
        self.guessCount += 1
        self.updateHangingMan()
        self.displayGuessLeft.setText(str(self.guessesLeft))

        if self.guessesLeft <= 0:
            self.displayLoss()
            return

    def displayWin(self):
        self.gameOver = True
        self.displayPopup('Congratulations!!\nYou have won!')

    def displayLoss(self):
        self.gameOver = True
        self.displayPopup('You have lost!')

    def displayPopup(self, message):
        message += f'\n\nThe answer was: {self.answer}'
        choice = QMessageBox.question(self, 'Hangman', message, QMessageBox.Reset)

        self.resetGame()

    def resetGame(self):
        self.gameOver = False

        self.guessesLeft = self.defaultGuesses
        self.displayGuessLeft.setText(str(self.defaultGuesses))
        self.displayWrongGuess.setText('')

        self._chooseNewAnswer()
        self.setAnswerLayout()
        self.setDisplayLength()

        self.guessCount = 0
        self.updateHangingMan()

        self.keyWidget.setFocus()

    def setDisplayLength(self):
        self.displayLength.setText(str(len(self.answer)))


# Create a Controller class to connect the GUI and the model
class PyAppCtrl:
    """PyCalc Controller class."""

    def __init__(self, model, view):
        """Controller initializer."""
        self._evaluate = model
        self._view = view
        # Connect signals and slots
        self._connectSignals()

    def _buildExpression(self, sub_exp):
        """Build expression."""
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()

        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _calculateResult(self):
        """Evaluate expressions."""
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _checkLetter(self, letter):
        self._view.keyWidget.setFocus()
        if self._view.gameOver:
            return
        if letter not in self._view.answer:
            if letter not in self._view.displayWrongGuessText():
                guesses = self._view.displayWrongGuessText()
                self._view.setDisplayWrongGuessText(f'{guesses} {letter},')
            return

        for item in self._view.answers:
            if item['text'] == letter:
                item['label'].setText(letter.upper())
                item['found'] = True

        self._checkWin()

    def _checkWin(self):
        for item in self._view.answers:
            if not item['found']:
                return
        self._view.displayWin()

    def _checkKeyPress(self, key):
        self._view.keyWidget.setFocus()
        # key = keyEvent.value()
        # if key.isalpha():
        # print('key pressed: %i' % key)
        key = QKeySequence(key).toString()
        # print(f'key pressed: {key}')
        if len(key) == 1 and key.isalpha():
            self._checkLetter(key.lower())

    def _connectSignals(self):
        """Connect signals and slots."""
        for btnText, btn in self._view.buttons.items():
            if btnText not in {'='}:
                btn.clicked.connect(partial(self._checkLetter, btnText))

        # self._view.buttons['='].clicked.connect(self._calculateResult)
        # self._view.display.returnPressed.connect(self._calculateResult)
        self._view.resetButton.clicked.connect(self._view.resetGame)
        self._view.keyWidget.keyPressed.connect(self._checkKeyPress)


# Create a Model to handle the calculator's operation
def evaluateExpression(expression):
    """Evaluate an expression"""
    try:
        print(expression)
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG

    return result


# Client code
def main():
    """Main function."""
    # Create an instance of QApplication
    app = QApplication(sys.argv)
    # Show the calculator's GUI
    view = PyAppUi()
    view.show()
    # Create instances of the model and the controller
    model = evaluateExpression
    PyAppCtrl(model=model, view=view)
    # Execute the calculator's main loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
