# Copyright (C) 2023-2024, Filippo Alimonda (Voxos.ai Inc.)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtCore import (
    QObject,
    QPoint,
    QRect,
    Qt,
    QThread,
    QTimer,
    pyqtSignal,
    pyqtSlot,
)
from PyQt5.QtGui import QColor, QFont, QMouseEvent, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget

from voxos.ui.context_menu import ContextMenu
from voxos.utils.constants import Constants

logger = logging.getLogger(__name__)


class Worker(QObject):
    """Handles the HUD bubble integer updates in a separate thread."""

    # Qt signals need to be declared as class attributes
    update_bubble_int_signal = pyqtSignal(int)

    @pyqtSlot(int)
    def do_work(self, value):
        """Emits the signal to update the bubble integer."""
        self.update_bubble_int_signal.emit(value)


class BubbleWidget(QWidget):
    """Displays a bubble with the number of runners currently running."""

    def __init__(self, parent: object = None, bubble_num: int = 0):
        super(BubbleWidget, self).__init__(parent)
        self.bubble_num = bubble_num
        if bubble_num == 0:
            self.hide()
        else:
            self.show()
        self.initUI()

    def initUI(self) -> None:  # pylint: disable=invalid-name
        """Initializes the bubble widget."""
        self.setGeometry(50, 50, 300, 300)

    def paintEvent(self, _) -> None:  # pylint: disable=invalid-name
        """Paints the bubble widget."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set color based on bubble_num
        if self.bubble_num == 0:
            painter.setBrush(Qt.white)
            pen = QPen(Qt.black)
        else:
            painter.setBrush(QColor(12, 102, 228))
            pen = QPen(Qt.white)

        pen.setWidth(1)
        painter.setPen(pen)

        # Draw circle at bottom left of label
        radius = 15
        center = QPoint(radius, self.height() - radius)
        painter.drawEllipse(center, radius, radius)

        # Draw bubble integer
        painter.setFont(QFont("Arial", 12))
        rect = QRect(center.x() - radius, center.y() - radius, 2 * radius, 2 * radius)
        txt = str(self.bubble_num)
        painter.drawText(rect, Qt.AlignCenter, txt)

    @pyqtSlot(int)
    def set_bubble_int(self, value: int) -> None:
        """Sets the bubble integer."""
        self.bubble_num = value
        if value == 0:
            self.hide()
        else:
            self.show()
        self.update()


class HeadsUpDisplay(QWidget):
    """Manages the HUD (Heads Up Display) for the Voxos.

    Attributes:
        context_menu (ContextMenu): The context menu for the HUD.
        draggable (bool): Whether or not the HUD is draggable.
        bubble_widget (BubbleWidget): A bubble showing the total number of active runners.
        click_and_lift_signal (pyqtSignal): Emitted by the HUD when user clicked and lifted.
    Args:
        display_on_init (bool): Whether or not to display the HUD on init.

    """

    click_and_lift_signal = pyqtSignal()

    def __init__(self, display_on_init=True):
        super().__init__()

        self.context_menu = None
        self.draggable = True
        self.mouse_press_pos = None
        self.mouse_move_pos = None

        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(100, 100)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.state_label = QLabel(self)
        self.default_pixmap = self.get_pixmap(
            Constants.APP_ICON_PNG_PATH, self.width(), self.height()
        )
        self.recording_pixmap = self.get_pixmap(
            Constants.RECORDING_ICON_PNG_PATH, self.width(), self.height()
        )

        self.state_label.setPixmap(self.default_pixmap)
        self.state_label.lower()

        self.bubble_widget = BubbleWidget(self, 0)
        self.bubble_widget.move(0, self.height() - self.bubble_widget.height())

        self.worker = Worker()
        self.thread = QThread()
        self.worker.update_bubble_int_signal.connect(
            self.bubble_widget.set_bubble_int, QtCore.Qt.DirectConnection
        )
        self.worker.moveToThread(self.thread)
        self.thread.start()

        screen_geometry = QApplication.desktop().screenGeometry()
        self.move(
            screen_geometry.width() - self.width(),
            self.height(),
        )

        self.timer = QTimer()
        self.timer.setSingleShot(True)

        if display_on_init:
            self.show()
        else:
            self.hide()

    def get_runners_bubble_int(self) -> int:
        """Gets the runners bubble integer."""
        return self.runners_bubble_int

    def get_pixmap(self, path: Path, width: int, height: int) -> QPixmap:
        """Returns a pixmap from a given path."""
        return QPixmap(path).scaled(width, height, Qt.KeepAspectRatio)

    def set_pixmap(self, pixmap: QPixmap) -> None:
        """Sets the pixmap of the HUD state label."""
        self.state_label.setPixmap(pixmap)
        self.state_label.resize(self.width(), self.height())

    def set_context_menu(self, context_menu: ContextMenu) -> None:
        """Sets the context menu for the HUD."""
        self.context_menu = context_menu

    def display(self) -> None:
        """Displays the HUD."""
        self.show()

    @pyqtSlot()
    def toggle_visibility(self) -> None:
        """Toggles the visibility of the HUD."""
        if self.isVisible():
            self.hide()
        else:
            self.show()

    @pyqtSlot()
    def show_recording(self) -> None:
        """Displays the recording image."""
        self.state_label.setPixmap(self.recording_pixmap)

    @pyqtSlot()
    def display_idle(self) -> None:
        """Resets the HUD to the default image."""
        self.state_label.setPixmap(self.default_pixmap)

    @pyqtSlot(int)
    def set_runners_bubble_int(self, value: int) -> None:
        """Sets the runners bubble integer."""
        self.bubble_widget.set_bubble_int(value)
        self.update()

    def mousePressEvent(  # pylint: disable=invalid-name
        self, event: QMouseEvent
    ) -> None:
        """Collect the event and position data when the mouse button is pressed"""
        if event.button() == Qt.LeftButton:
            self.mouse_press_pos = event.globalPos()
            self.mouse_move_pos = event.globalPos() - self.pos()
            self.timer.start(500)  # 500 ms

    def mouseMoveEvent(  # pylint: disable=invalid-name
        self, event: QMouseEvent
    ) -> None:
        """Move the widget as the user drags the mouse pointer on the screen and
        snap it to the closest edge."""

        if event.buttons() == Qt.LeftButton:
            global_pos = event.globalPos()
            moved = global_pos - self.mouse_move_pos
            self.move(moved)
            self.mouse_move_pos = global_pos - self.pos()

            screen = QApplication.desktop().availableGeometry()
            right_gap = screen.right() - self.geometry().right()
            left_gap = self.geometry().left() - screen.left()
            top_gap = self.geometry().top() - screen.top()
            bottom_gap = screen.bottom() - self.geometry().bottom()

            locations = [right_gap, left_gap, top_gap, bottom_gap]
            nearest = min(locations)

            if nearest == right_gap:
                self.move(screen.right() - self.geometry().width(), self.pos().y())
            elif nearest == left_gap:
                self.move(screen.left(), self.pos().y())
            elif nearest == top_gap:
                self.move(self.pos().x(), screen.top())
            elif nearest == bottom_gap:
                self.move(self.pos().x(), screen.bottom() - self.geometry().height())

    def mouseReleaseEvent(  # pylint: disable=invalid-name
        self, event: QMouseEvent
    ) -> None:
        """Stop the timer when the mouse button is released."""
        if event.button() == Qt.LeftButton and self.timer.isActive():
            self.timer.stop()
            self.click_and_lift_signal.emit()

    def contextMenuEvent(  # pylint: disable=invalid-name
        self, event: QMouseEvent
    ) -> None:
        """Creates a context menu when the user right clicks on the HUD."""
        self.context_menu.exec_(self.mapToGlobal(event.pos()))
