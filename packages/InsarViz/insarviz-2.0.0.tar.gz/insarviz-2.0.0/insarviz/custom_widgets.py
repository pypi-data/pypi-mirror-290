#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" custom_widgets

This modules contains custom widgets.

Contains classes:
    * Toggle - round toggle button switching between two positions
    * AnimatedToggle - animates the Toggle switch
    * FileInfoWidget - table-like widget filed with metadata from file

modified from qt-widgets: github.com/pythonguis/python-qtwidgets

"""

from typing import Optional

from PyQt5.QtCore import (
    Qt, QSize, QPoint, QPointF, QRectF,
    QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup,
)

from PyQt5.QtCore import pyqtSlot, pyqtProperty

from PyQt5.QtWidgets import (
    QWidget, QCheckBox, QStyle, QProxyStyle, QStyleOption, QTabBar, QDockWidget, QMainWindow
)

from PyQt5.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter, QIcon


class IconDockStyle(QProxyStyle):

    # adapted from https://stackoverflow.com/a/3482795

    def __init__(self, icon: QIcon, style: Optional[QStyle] = None):
        super().__init__(style)
        self.icon = icon

    def drawControl(self, element: QStyle.ControlElement, option: QStyleOption, painter: QPainter,
                    widget: Optional[QWidget] = None) -> None:
        if element == QStyle.CE_DockWidgetTitle:
            # width of the icon
            width: int = self.pixelMetric(QStyle.PM_TabBarIconSize)
            # margin of title from frame
            margin: int = self.baseStyle().pixelMetric(QStyle.PM_DockWidgetTitleMargin)
            icon_point = QPoint(margin + option.rect.left(),
                                margin + option.rect.center().y() - width//2)
            painter.drawPixmap(icon_point, self.icon.pixmap(width, width))
            option.rect = option.rect.adjusted(width, 0, 0, 0)
        self.baseStyle().drawControl(element, option, painter, widget)


def add_icon_to_tab(window: QMainWindow, tab_name: str, icon: QIcon):
    # adapted from https://stackoverflow.com/a/46623219
    def f(_):
        for tabbar in window.findChildren((QTabBar)):
            for i in range(tabbar.count()):
                if tabbar.tabText(i) == tab_name:
                    tabbar.setTabIcon(i, icon)
    return f


class IconDockWidget(QDockWidget):

    def __init__(self, name: str, parent: QWidget, icon: QIcon):
        assert isinstance(parent, QMainWindow)
        super().__init__(name, parent)
        self.setStyle(IconDockStyle(icon))
        self.visibilityChanged.connect(add_icon_to_tab(parent, name, icon))


class Toggle(QCheckBox):

    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    def __init__(self, parent=None, bar_color: QColor = QColor("gray"),
                 checked_color: QColor = QColor("white"), handle_color: QColor = QColor("white")):
        super().__init__(parent)
        # Save our properties on the object via self, so we can access them
        # later in the paintEvent.
        self._bar_brush = QBrush(bar_color)
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())
        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))
        # Setup the rest of the widget.
        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0
        self.stateChanged.connect(self.handle_state_change)

    def sizeHint(self) -> QSize:
        return QSize(58, 45)

    def hitButton(self, pos: QPoint) -> bool:
        return self.contentsRect().contains(pos)

    def paintEvent(self, e: QPaintEvent) -> None:
        # pylint: disable=missing-function-docstring, invalid-name, unused-argument
        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius
        xPos = (
            contRect.x() + handleRadius + trailLength * self._handle_position
        )

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)

            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()

    @pyqtSlot(int)
    def handle_state_change(self, value: int) -> None:
        self._handle_position = 1 if value else 0

    @pyqtProperty(float)
    def handle_position(self) -> float:
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

    @pyqtProperty(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()


class AnimatedToggle(Toggle):

    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    def __init__(self,
                 *args,
                 pulse_unchecked_color="#44999999",
                 pulse_checked_color="#44999999",
                 **kwargs):

        self._pulse_radius: float = 0

        super().__init__(*args, **kwargs)

        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(200)  # time in ms

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(350)  # time in ms
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(20)

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)

        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_animation = QBrush(QColor(pulse_checked_color))

    @pyqtSlot(int)
    def handle_state_change(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, e: QPaintEvent):

        contRect = self.contentsRect()
        handleRadius = int(round(0.24 * contRect.height()))

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, handleRadius*2
            # 0.25 * contRect.height()
        )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius

        xPos = (
            contRect.x() + handleRadius + trailLength * self._handle_position
        )

        if self.pulse_anim.state() == QPropertyAnimation.Running:
            p.setBrush(
                self._pulse_checked_animation if
                self.isChecked() else self._pulse_unchecked_animation)
            p.drawEllipse(QPointF(xPos, barRect.center().y()),
                          self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.setPen(self._light_grey_pen)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.setPen(self._light_grey_pen)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.setBrush(Qt.black)
        p.drawPie(int(xPos)-handleRadius,
                  int(barRect.center().y())-handleRadius,
                  handleRadius*2,
                  handleRadius*2,
                  90*16,
                  180*16)

        # text under icon:
        # p.setPen(Qt.black)
        # small_font = p.font()
        # small_font.setPointSize(p.font().pointSize()//2)
        # p.setFont(small_font)
        # p.drawText(contRect,
        #            (Qt.AlignCenter | Qt.AlignBottom),
        #            'background \ncolor')

        p.end()
