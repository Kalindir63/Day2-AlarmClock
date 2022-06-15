from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

# https://www.geeksforgeeks.org/pyqt5-create-a-digital-clock/

class _Time(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(_Time, self).__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )
        self._time = '00:00'



    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(300, 70)

    def _trigger_refresh(self):
        self.update()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor('grey'))
        brush.setStyle(Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        pen = painter.pen()
        pen.setColor(QtGui.QColor('black'))
        painter.setPen(pen)

        font = painter.font()
        # font.setFamily('Times')

        period = 'AM'
        time_y = 75
        time_start = 0

        font.setPointSize(50)
        painter.setFont(font)
        painter.drawText(time_start, time_y, self._time)

        font.setPointSize(12)
        painter.setFont(font)

        if len(self._time) == 5:
            painter.drawText(time_start+170, time_y, period)
        else:
            painter.drawText(time_start+135, time_y, period)

        painter.end()




class AlarmWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(AlarmWidget, self).__init__(*args, **kwargs)

        self.generalLayout = QtWidgets.QGridLayout()
        self._time = _Time()
        # self._time.setFixedSize(50,70)
        self.generalLayout.addWidget(self._time, 0, 0)

        self.setLayout(self.generalLayout)
        # self.generalLayout.setColumnMinimumWidth(0, 50)
        # self.generalLayout.setRowMinimumHeight(0, 40)

        # self._createTimeLayout()
        # self._createTimeUntil()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._showTime)
        self.timer.start(1000)

    def _showTime(self):
        # getting current time
        current_time = QtCore.QTime.currentTime()

        # converting QTime object to string
        label_time = current_time.toString('hh:mm')

        self._time._time = label_time
        self._time.update()

    def _createTimeLayout(self):
        timeLayout = QtWidgets.QHBoxLayout()
        fixed_height = 70

        timeFont = QtGui.QFont()
        timeFont.setPointSize(50)
        timeFont.setWeight(5)
        self._timeLabel = QtWidgets.QLabel('7:00')
        self._timeLabel.setAlignment(Qt.AlignBottom)
        self._timeLabel.setFont(timeFont)
        self._timeLabel.setFixedHeight(fixed_height)

        timePeriodFont = QtGui.QFont()
        timePeriodFont.setPointSize(15)
        timePeriodFont.setWeight(10)
        self._timePeriodLabel = QtWidgets.QLabel('AM')
        self._timePeriodLabel.setAlignment(Qt.AlignBottom)
        self._timePeriodLabel.setFont(timePeriodFont)
        self._timePeriodLabel.setFixedHeight(fixed_height)

        # layout.addWidget(self._timeLabel, row, col)
        timeLayout.addWidget(self._timeLabel)
        timeLayout.addWidget(self._timePeriodLabel)
        self.generalLayout.addLayout(timeLayout, 0, 0)

    def _createTimeUntil(self):
        hours = 17
        minutes = 14
        hours_text = f'{hours} hours'
        if hours == 1:
            hours_text = f'1 hour'

        minutes_text = f'{minutes} minutes'
        if minutes == 1:
            minutes_text = f'1 minute'

        font = QtGui.QFont()
        font.setPixelSize(20)
        self.timeUntilLabel = QtWidgets.QLabel(f'⏰ in {hours_text}, {minutes_text}')
        self.timeUntilLabel.setFont(font)

        self.generalLayout.addWidget(self.timeUntilLabel, 1, 0)
