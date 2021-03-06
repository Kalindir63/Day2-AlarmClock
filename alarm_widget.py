from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot as Slot, pyqtProperty as Property
import qtawesome as qta


# https://www.geeksforgeeks.org/pyqt5-create-a-digital-clock/

# #107C10 - Windows green


class _Toggle(QtWidgets.QCheckBox):
    _transparent_pen = QtGui.QPen(Qt.transparent)
    _light_grey_pen = QtGui.QPen(Qt.lightGray)
    clickedValue = QtCore.pyqtSignal(int)

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
            # painter.setPen(self._bar_checked_pen)
            painter.drawRoundedRect(barRect, rounding, rounding)
            # painter.drawPath(barRectPath)
            # painter.setBrush(self._handle_checked_brush)

        else:
            # painter.setBrush(self._bar_brush)
            painter.setPen(QtGui.QPen(QtGui.QColor('white')))
            painter.drawRoundedRect(barRect, rounding, rounding)
            # painter.drawPath(barRectPath)
            # painter.setPen(self._light_grey_pen)
            # painter.setBrush(self._handle_brush)

        # Draw handle
        painter.setBrush(self._handle_brush)
        painter.setPen(QtGui.QPen(QtGui.QColor('white')))
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

        self._active = False

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
        # if not self._enabled:
        #     pen.setColor(QtGui.QColor('white'))
        # pen.setColor(QtGui.QColor('red'))
        painter.setPen(pen)

        if self._antialiased:
            painter.setRenderHint(painter.Antialiasing, True)

        # Get Font
        font = painter.font()

        if self._active:
            pen.setColor(QtGui.QColor('green'))
            painter.setPen(pen)

        # Draw Shape
        if self._enabled:
            painter.drawEllipse(rect)

        else:
            pen.setColor(QtGui.QColor('grey'))
            painter.setPen(pen)

        # Draw text
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, self._day)

        painter.end()

    def setActive(self, a0: bool) -> None:
        self._active = a0
        self.update()


class _Time(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(_Time, self).__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )
        self._time = '00:00'
        self._timePeriod = 'am'

        self.getTimeUntilText()

        self._backgroundColor = QtGui.QColor('#2B2B2B')
        self._textColor = QtGui.QColor('#808080')

        palette = self.palette()
        palette.setColor(self.backgroundRole(), self._backgroundColor)
        palette.setColor(self.foregroundRole(), self._textColor)
        self.setPalette(palette)

        self._enabled = False

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(200, 85)

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
        # print(rect.size())

        pen = painter.pen()
        pen.setColor(self._textColor)
        painter.setPen(pen)

        font = painter.font()
        # font.setFamily('Times')

        time_y = 2
        time_start = 2

        if self._enabled:
            pen.setColor(QtGui.QColor('white'))
            painter.setPen(pen)

        font.setPointSize(50)
        timeFontMetric = QtGui.QFontMetrics(font)
        timeWidth = timeFontMetric.width(self._time)
        time_y = time_y + timeFontMetric.height() - 30
        painter.setFont(font)
        painter.drawText(time_start, time_y, self._time)

        font.setPointSize(12)
        painter.setFont(font)

        painter.drawText(time_start + timeWidth, time_y, self._timePeriod.upper())

        pen.setColor(self._textColor)
        painter.setPen(pen)

        timeUntil = self.getTimeUntilText()
        timeUntilFontMetric = QtGui.QFontMetrics(font)
        timeUntilHeight = timeUntilFontMetric.height()
        painter.drawText(time_start, time_y + timeUntilHeight + 5, timeUntil)

        painter.end()

    def getTimeUntilText(self):
        current_time = QtCore.QTime.currentTime()
        timeFormat = 'hh:mmap'
        if len(self._time) < 5:
            timeFormat = 'h:mmap'
        alarm_time = QtCore.QTime.fromString(f'{self._time}{self._timePeriod}', timeFormat)

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

        return f'??? in {hours_text}, {minutes_text}'

    def setEnabled(self, a0: bool) -> None:
        self._enabled = a0
        self.update()


class _IconLabel(QtWidgets.QWidget):
    IconSize = QtCore.QSize(16, 16)
    HorizontalSpacing = 2

    def __init__(self, qta_id, text='', final_stretch=True, *args, **kwargs):
        super(_IconLabel, self).__init__(*args, **kwargs)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        icon = QtWidgets.QLabel()
        icon.setPixmap(qta.icon(qta_id).pixmap(self.IconSize))

        layout.addWidget(icon)
        layout.addSpacing(self.HorizontalSpacing)
        layout.addWidget(QtWidgets.QLabel(text))

        if final_stretch:
            layout.addStretch()


class _Edit(QtWidgets.QWidget):
    deleted = QtCore.pyqtSignal(bool)
    cancelled = QtCore.pyqtSignal()
    saved = QtCore.pyqtSignal()

    def __init__(self, newWidget=False, *args, **kwargs):
        super(_Edit, self).__init__(*args, **kwargs)

        # Window Flags
        # self.setWindowFlag(Qt.FramelessWindowHint)

        # General Layout
        self.generalLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.generalLayout)

        # Default color scheme
        self.default_colors = {
            'ActiveText': QtGui.QColor('white'),
            'InActiveText': QtGui.QColor('#808080'),
            'ActivePrimary': QtGui.QColor('#107C10'),
            'Background': QtGui.QColor('#2B2B2B'),
        }

        # Palette
        primaryColor = '#107C10'
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtGui.QColor('#2B2B2B'))
        palette.setColor(self.foregroundRole(), QtGui.QColor('white'))
        self.setPalette(palette)

        # Variables
        self._newWidget = newWidget

        # Create UI
        self._CreateUi()

        # Size policy
        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        self._connectSignals()

    def _connectSignals(self):
        self.cancelBtn.clicked.connect(self._cancelledHandler)
        self.saveBtn.clicked.connect(self._savedHandler)

    def _cancelledHandler(self):
        self.cancelled.emit()

    def _savedHandler(self):
        self.saved.emit()

    def sizeHint(self) -> QtCore.QSize:
        # Width: 321 px | Height: 548 px
        return QtCore.QSize(321, 548)

    def _CreateUi(self):
        self._topTileLayout()

        # time edit layout
        # X: 3503 | Y: 289 | Right: 3782 | Bottom: 368
        # Width: 280 px | Height: 80 px | Area: 22400 px | Perimeter: 720 px
        self._timeLayout()

        self._messageLayout()

        self._repeatLayout()

        self._dowLayout()

        self._soundLayout()

        self._snoozeLayout()

        self._buttonsLayout()
        # Add edit options

        # save button
        # cancel button

    def _topTileLayout(self):
        # top title layout
        topTitleLayout = QtWidgets.QHBoxLayout()
        # title - top left
        if self._newWidget:
            label = QtWidgets.QLabel('Add new alarm')
        else:
            label = QtWidgets.QLabel('Edit alarm')

        font = QtGui.QFont()
        font.setPixelSize(20)
        label.setFont(font)

        topTitleLayout.addWidget(label, alignment=Qt.AlignTop | Qt.AlignLeft)
        # Delete button - top right
        deleteBtn = QtWidgets.QPushButton()

        pixmapi = self.style().SP_TrashIcon
        icon = self.style().standardIcon(pixmapi)
        deleteBtn.setIcon(icon)
        deleteBtn.setStyleSheet("background-color: transparent")
        topTitleLayout.addWidget(deleteBtn, alignment=Qt.AlignTop | Qt.AlignRight)

        deleteBtn.clicked.connect(self._deletedConfirm)

        self.generalLayout.addLayout(topTitleLayout)

    def _timeLayout(self):
        timeLayout = QtWidgets.QVBoxLayout()

        font = self.font()
        font.setPixelSize(70)

        self.timeEdit = QtWidgets.QTimeEdit()
        self.timeEdit.setDisplayFormat('hh:mm ap')
        self.timeEdit.setFont(font)
        self.timeEdit.setButtonSymbols(self.timeEdit.NoButtons)
        self.timeEdit.setWrapping(True)
        self.timeEdit.setStyleSheet(f"background-color: black;"
                                    f"border-color: {self.default_colors['ActivePrimary'].name()};"
                                    f"color: white;")

        timeLayout.addWidget(self.timeEdit)

        # End _timeLayout
        self.generalLayout.addLayout(timeLayout)

    def _messageLayout(self):
        messageLayout = QtWidgets.QHBoxLayout()
        iconlabel = _IconLabel("fa.pencil-square-o")

        messageLayout.addWidget(iconlabel)

        self.generalLayout.addLayout(messageLayout)

    def _repeatLayout(self):
        pass

    def _dowLayout(self):
        pass

    def _soundLayout(self):
        pass

    def _snoozeLayout(self):
        pass

    def _buttonsLayout(self):
        btnLayout = QtWidgets.QHBoxLayout()
        self.saveBtn = QtWidgets.QPushButton('Save')
        self.saveBtn.setStyleSheet(f"background-color: {self.default_colors['ActivePrimary'].name()};"
                                   f"color: {self.default_colors['ActiveText'].name()};")

        btnLayout.addWidget(self.saveBtn)

        self.cancelBtn = QtWidgets.QPushButton('Cancel')
        self.cancelBtn.setStyleSheet(f"background-color: {self.default_colors['Background'].lighter().name()};"
                                     f"color: {self.default_colors['ActiveText'].name()};")

        btnLayout.addWidget(self.cancelBtn)

        self.generalLayout.addLayout(btnLayout)

    def _deletedConfirm(self):
        # Confirm message
        # confirm = QtWidgets.QMessageBox.question(self, 'Title', 'message',
        #                                          QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
        #                                          QtWidgets.QMessageBox.Cancel)
        # print(confirm)
        self.deleted.emit(True)


class AlarmWidget(QtWidgets.QWidget):
    clicked = QtCore.pyqtSignal(bool)
    deleted = QtCore.pyqtSignal(QtWidgets.QWidget)
    cancelled = QtCore.pyqtSignal(QtWidgets.QWidget)
    saved = QtCore.pyqtSignal(QtWidgets.QWidget)

    def __init__(self, dow='', time='00:00am', message='Alarm', enabled=False, position=(0, 0), newWidget=False, *args,
                 **kwargs):
        super(AlarmWidget, self).__init__(*args, **kwargs)
        # Variables
        self.message = message
        self.time = time
        self.dow = dow
        self._position = position
        self._newWidget = newWidget

        self.default_colors = {
            'ActiveText': QtGui.QColor('white'),
            'InActiveText': QtGui.QColor('#808080'),
            'ActivePrimary': QtGui.QColor('#107C10'),
            'Background': QtGui.QColor('#2B2B2B'),
        }

        self._backgroundColor = self.default_colors['Background']
        self._textColor = self.default_colors['InActiveText']

        self._enabled = enabled

        self.editPopup = None

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

        # painter = QtGui.QPainter(self)
        # print(painter.device().width(), painter.device().height())
        # self.generalLayout.setGeometry(QtCore.QRect(0,0,640,480))

        # Timer
        self._showTime()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._showTime)
        seconds = 1
        self.timer.start(seconds * 1000)

        # Size policy
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )

        self._toggleElements()

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(286, 201)

    def _createTimeLabel(self):
        self._time = _Time()
        self._time.setFixedHeight(85)
        self._time.setFixedWidth(200)
        # self._time.setFixedSize(50,70)
        self.generalLayout.setColumnStretch(0, 1)
        self.generalLayout.setRowStretch(0, 1)
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
        self.generalLayout.setColumnStretch(0, 1)
        self.generalLayout.setRowStretch(1, 1)
        self.generalLayout.addWidget(self.messageLabel, 1, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

    def update(self) -> None:
        super(AlarmWidget, self).update()
        self._showTime()

    def _showTime(self):
        timeFormat = 'hh:mmap'
        if len(self.time) < 7:
            timeFormat = 'h:mmap'
        alarm_time = QtCore.QTime.fromString(self.time, timeFormat)
        alarm_time_str = alarm_time.toString(timeFormat)

        self._time._time = alarm_time_str[:-2]
        self._time._timePeriod = alarm_time_str[-2:]
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
        self._dowWidgets = {}

        dowSet = self.dow.ljust(7, '0')
        for item in enumerate(dow):
            self._dowWidgets[item[1]] = _DowIcon(item[1], dowSet[item[0]] == '1')
            self._dowWidgets[item[1]].setPalette(self.palette())
            dowSize = 28
            self._dowWidgets[item[1]].setFixedSize(dowSize, dowSize)
            self._dowWidgets[item[1]].setAntialiased(True)

            dowLayout.addWidget(self._dowWidgets[item[1]])

        self.generalLayout.setRowStretch(2, 2)
        self.generalLayout.setColumnStretch(0, 1)
        self.generalLayout.addLayout(dowLayout, 2, 0, 2, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

    def _createEnableCheckbox(self):
        self.checkbox = _Toggle(checked_color=self.default_colors['ActivePrimary'].name())
        self.checkbox.setChecked(self._enabled)

        self.generalLayout.setRowStretch(0, 1)
        self.generalLayout.setColumnStretch(1, 1)
        self.generalLayout.addWidget(self.checkbox, 0, 1, alignment=Qt.AlignTop | Qt.AlignRight)

        self.checkbox.clicked.connect(self._state_changed)

    def _state_changed(self):
        if self.checkbox.isChecked():
            self._enabled = True
        else:
            self._enabled = False

        self._toggleElements()

    def _toggleElements(self):
        self._time.setEnabled(self._enabled)
        for dowName, dowWidget in self._dowWidgets.items():
            dowWidget.setActive(self._enabled)

        palette = self.palette()

        if self._enabled:
            palette.setColor(self.foregroundRole(), self.default_colors['ActiveText'])

        else:
            palette.setColor(self.foregroundRole(), self.default_colors['InActiveText'])

        self.messageLabel.setPalette(palette)
        # self._time.setPalette(palette)

    def Save(self):
        self._newWidget = False
        return {
            'time': self.time,
            'dow': self.dow,
            'message': self.message,
            'enabled': self._enabled,
            'position': self._position
        }

    def Edit(self):
        # popup simple edit screen
        if self.editPopup is None:
            # self.editPopup = _Edit(parent=self.parent().parent())
            self.editPopup = _Edit(self._newWidget)
            self.editPopup.deleted.connect(self._deleteWidget)
            self.editPopup.cancelled.connect(self._cancelledHandler)
            self.editPopup.saved.connect(self._saveHandler)
            self.editPopup.show()
        else:
            self.editPopup.close()
            self.editPopup = None

    def IsNewWidget(self):
        return self._newWidget

    def _saveHandler(self):
        self.Edit()
        self.saved.emit(self)

    def _deleteWidget(self):
        self.Edit()
        self.deleted.emit(self)

    def _cancelledHandler(self):
        self.Edit()
        self.cancelled.emit(self)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # if event.button() == Qt.LeftButton:
        #     self.pressPos = event.pos()
        self.Edit()
        self.clicked.emit(True)

        # widget = self.childAt(event.pos())
        # print(widget)

# void MainWindow::mousePressEvent(QMouseEvent *event)
# {
#     QWidget * const widget = childAt(event->pos());
#     qDebug() << "child widget" << widget;
#     if (widget) {
#         const QLabel * const label = qobject_cast<QLabel *>(widget);
#         if (label) {
#             qDebug() << "label" << label->text();
#         }
#
#         const int index = centralWidget()->layout()->indexOf(widget);
#         qDebug() << "layout index" << index;
#         if (index >=0) {
#             const QLayoutItem * const item = centralWidget()->layout()->itemAt(index);
#             qDebug() << "layout item" << item;
#         }
#     }
# }
