from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot as Slot, pyqtProperty as Property


# https://www.geeksforgeeks.org/pyqt5-create-a-digital-clock/

# #107C10 - Windows green


class _Toggle(QtWidgets.QCheckBox):
    _transparent_pen = QtGui.QPen(Qt.transparent)
    _light_grey_pen = QtGui.QPen(Qt.lightGray)

    def __init__(self,
                 bar_color=Qt.gray,
                 checked_color='#00B0FF',
                 handle_color=Qt.white,
                 *args, **kwargs):
        super(_Toggle, self).__init__(*args, **kwargs)

        # Save our properties on the object via self, so we can access them later
        # in the paintEvent.
        barPen = QtGui.QPen(bar_color, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self._bar_brush = QtGui.QBrush(bar_color)
        self._bar_pen = barPen
        self._bar_checked_brush = QtGui.QBrush(QtGui.QColor(checked_color).lighter())
        barPen.setColor(QtGui.QColor(checked_color).lighter())
        self._bar_checked_pen = barPen

        self._handle_brush = QtGui.QBrush(handle_color)
        self._handle_checked_brush = QtGui.QBrush(QtGui.QColor(checked_color))

        # Setup the rest of the widget.
        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0

        self.stateChanged.connect(self.handle_state_changed)

    def sizeHint(self):
        return QtCore.QSize(58, 38)

    def hitButton(self, pos: QtCore.QPoint) -> bool:
        return self.contentsRect().contains(pos)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        containerRect = self.contentsRect()
        handleRadius = round(0.18 * containerRect.height())  # handle size

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.setPen(self._transparent_pen)
        barRect = QtCore.QRectF(
            0, 0,
            containerRect.width(),
            (handleRadius * 2) + 5
        )

        barRect.moveCenter(containerRect.center())
        rounding = barRect.height() / 2
        barRectPath = QtGui.QPainterPath()
        barRectPath.addRoundedRect(barRect, rounding, rounding)


        # the handle will move along this line
        trailLength = (containerRect.width() - 2 * handleRadius) - 6
        xPos = containerRect.x() + handleRadius + 2 + trailLength * self._handle_position



        # Draw Line
        if self.isChecked():
            painter.setBrush(self._bar_checked_brush)
            # painter.drawRoundedRect(barRect, rounding, rounding)
            painter.setPen(self._bar_checked_pen)
            painter.drawPath(barRectPath)
            painter.setBrush(self._handle_checked_brush)

        else:
            painter.setBrush(self._bar_brush)
            # painter.drawRoundedRect(barRect, rounding, rounding)
            painter.setPen(self._bar_pen)
            painter.drawPath(barRectPath)
            painter.setPen(self._light_grey_pen)
            painter.setBrush(self._handle_brush)

        # Draw handle
        painter.drawEllipse(
            QtCore.QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        painter.end()

    @Slot(int)
    def handle_state_changed(self, value):
        self._handle_position = 1 if value else 0

    @Property(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we're doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self._handle_position = pos
        self.update()

    @Property(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()


class _DowIcon(QtWidgets.QWidget):
    def __init__(self, day, enabled, *args, **kwargs):
        super(_DowIcon, self).__init__(*args, **kwargs)

        self._day = day
        self._enabled = enabled

        self._antialiased = False

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(300, 100)

    def setAntialiased(self, antialiased):
        self._antialiased = antialiased
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)

        width = painter.device().width() - 2
        height = painter.device().height() - 2

        rect = QtCore.QRect(1, 1, width, height)
        # print(painter.device().width(), painter.device().height())

        # Modify Brush
        brush = QtGui.QBrush()

        painter.setBrush(brush)
        # Modify pen
        pen = painter.pen()
        if self._enabled:
            pen.setColor(QtGui.QColor('white'))
        # pen.setColor(QtGui.QColor('red'))
        painter.setPen(pen)

        if self._antialiased:
            painter.setRenderHint(painter.Antialiasing, True)

        # Get Font
        font = painter.font()

        # Draw Shape
        painter.drawEllipse(rect)

        # Draw text
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, self._day)

        painter.end()


class _Time(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(_Time, self).__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )
        self._time = '00:00'
        self._timePeriod = 'am'

        self.getTimeUntilText()

        self._backgroundColor = QtGui.QColor('#2B2B2B')
        self._textColor = QtGui.QColor('#808080')

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(300, 100)

    def _trigger_refresh(self):
        self.update()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)

        brush = QtGui.QBrush()
        # brush.setColor(QtGui.QColor('transparent'))
        # brush.setColor(self._backgroundColor)
        # brush.setStyle(Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        pen = painter.pen()
        # pen.setColor(self._textColor)
        painter.setPen(pen)

        font = painter.font()
        # font.setFamily('Times')

        time_y = 2
        time_start = 2

        font.setPointSize(50)
        timeFontMetric = QtGui.QFontMetrics(font)
        timeWidth = timeFontMetric.width(self._time)
        time_y = time_y + timeFontMetric.height() - 30
        painter.setFont(font)
        painter.drawText(time_start, time_y, self._time)

        font.setPointSize(12)
        painter.setFont(font)

        painter.drawText(time_start + timeWidth, time_y, self._timePeriod.upper())

        timeUntil = self.getTimeUntilText()
        timeUntilFontMetric = QtGui.QFontMetrics(font)
        timeUntilHeight = timeUntilFontMetric.height()
        painter.drawText(time_start, time_y + timeUntilHeight + 5, timeUntil)

        # print(time_y + timeUntilHeight + 5)
        # print(time_start+ timeUntilFontMetric.width(timeUntil))
        painter.end()

    def getTimeUntilText(self):
        current_time = QtCore.QTime.currentTime()
        format = 'hh:mmap'
        if len(self._time) < 5:
            format = 'h:mmap'
        alarm_time = QtCore.QTime.fromString(f'{self._time}{self._timePeriod}', format)

        secs_until = current_time.secsTo(alarm_time)

        if secs_until < 0:
            secs_until = 86400 + secs_until

        minutes, seconds = divmod(secs_until, 60)
        hours, minutes = divmod(minutes, 60)

        hours_text = f'{hours} hours'
        if hours == 1:
            hours_text = f'1 hour'

        minutes_text = f'{minutes} minutes'
        if minutes == 1:
            minutes_text = f'1 minute'

        return f'⏰ in {hours_text}, {minutes_text}'


class AlarmWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(AlarmWidget, self).__init__(*args, **kwargs)
        # Variables
        self.message = 'Good morning'
        self.timeLabel = '7:00'
        self.timePeriod = 'am'

        self._backgroundColor = QtGui.QColor('#2B2B2B')
        self._textColor = QtGui.QColor('#808080')

        # Set Colors
        palette = self.palette()
        palette.setColor(self.backgroundRole(), self._backgroundColor)
        palette.setColor(self.foregroundRole(), self._textColor)
        self.setPalette(palette)

        # Layout
        self.generalLayout = QtWidgets.QGridLayout()
        self.generalLayout.setVerticalSpacing(20)

        self._createTimeLabel()
        self._createMessageLabel()
        self._createDowLayout()
        self._createEnableCheckbox()

        self.setLayout(self.generalLayout)

        # Timer
        self._showTime()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._showTime)
        seconds = 1
        self.timer.start(seconds * 1000)

    # def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
    #     painter = QtGui.QPainter(self)
    #
    #     brush = QtGui.QBrush()
    #     # brush.setColor(QtGui.QColor('transparent'))
    #     brush.setColor(self._backgroundColor)
    #     brush.setStyle(Qt.SolidPattern)
    #     rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
    #     painter.fillRect(rect, brush)

    def _createTimeLabel(self):
        self._time = _Time()
        self._time.setFixedHeight(81)
        self._time.setFixedWidth(200)
        # self._time.setFixedSize(50,70)
        self.generalLayout.setColumnStretch(0, 0)
        self.generalLayout.setRowStretch(0, 0)
        self.generalLayout.addWidget(self._time, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

    def _createMessageLabel(self):
        font = QtGui.QFont()
        font.setPointSize(15)
        fontMetrics = QtGui.QFontMetrics(font)
        height = fontMetrics.height()

        self.messageLabel = QtWidgets.QLabel(self.message)
        self.messageLabel.setPalette(self.palette())
        self.messageLabel.setFont(font)
        self.messageLabel.setFixedHeight(height)
        self.generalLayout.setColumnStretch(0, 0)
        self.generalLayout.setRowStretch(1, 0)
        self.generalLayout.addWidget(self.messageLabel, 1, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

    def _showTime(self):
        self._time._time = self.timeLabel
        self._time._timePeriod = self.timePeriod
        self._time.update()

    def _createDowLayout(self):
        dowLayout = QtWidgets.QHBoxLayout()
        dowLayout.setSpacing(10)
        dow = [
            'Su',
            'M',
            'Tu',
            'We',
            'Th',
            'Fri',
            'Sa',
        ]

        for item in dow:
            dowWidget = _DowIcon(item, True)
            dowWidget.setPalette(self.palette())
            dowSize = 28
            dowWidget.setFixedSize(dowSize, dowSize)
            dowWidget.setAntialiased(True)

            dowLayout.addWidget(dowWidget)

        self.generalLayout.addLayout(dowLayout, 2, 0, 2, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

    def _createEnableCheckbox(self):
        self.checkbox = _Toggle()

        self.generalLayout.addWidget(self.checkbox, 0, 1, alignment=Qt.AlignTop | Qt.AlignRight)
