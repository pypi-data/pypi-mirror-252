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
from typing import Optional

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

from voxos.ui.context_menu import ContextMenu
from voxos.utils.constants import Constants

logger = logging.getLogger(__name__)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """Handles the system tray icon functionality for a PyQt5 application.

    Provides the capability to manage and display a system tray icon,
    including changing icons, showing notifications, and managing a context menu.

    Attributes:
        DEFAULT_NOTIFICATION_DURATION (int): Default duration in milliseconds for
            displaying notifications.
        enable_taskbar_notifications (bool): Flag to enable or disable taskbar notifications.
        menu (Optional[QtWidgets.QMenu]): The context menu for the system tray icon.

    Args:
        parent (Optional[QtWidgets.QWidget]): The parent widget of the system tray icon.
        enable_taskbar_notifications (bool): If set to True, enables notifications on
            the taskbar. Defaults to True.
    """

    DEFAULT_NOTIFICATION_DURATION = 500  # milliseconds
    enable_taskbar_notifications = True
    menu = None

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None,
        enable_taskbar_notifications: bool = True,
    ) -> None:
        """Initializes the system tray icon with a specified parent and notification setting."""
        icon = QIcon(QPixmap(Constants.APP_ICON_PNG_PATH))
        super().__init__(icon, parent)
        self.setToolTip(f"{Constants.APP_NAME}")
        self.enable_taskbar_notifications = enable_taskbar_notifications

        self.context_menu = None

        self.setup_ui()
        self.show()

    def setup_ui(self) -> None:
        """Sets up the user interface components of the system tray icon.

        Initializes the context menu with an 'Exit' action and sets the
        default and recording icons.
        """
        self.default_icon = self.icon()

    def set_context_menu(self, context_menu: ContextMenu) -> None:
        """Sets up the context menu for the system tray icon."""
        self.context_menu = context_menu
        self.setContextMenu(self.context_menu)

    def show_recording_icon(self) -> None:
        """Switches the tray icon to indicate that recording is in progress.

        Changes the icon in the system tray to a recording-specific icon
        and updates the tooltip to reflect the recording status.
        """
        self.setIcon(self.recording_icon)
        self.setToolTip(f"{Constants.APP_NAME} Listening...")

    def show_default_icon(self) -> None:
        """Reverts the tray icon back to its default state.

        Changes the icon in the system tray back to the default icon and
        updates the tooltip accordingly.
        """
        self.setIcon(self.default_icon)
        self.setToolTip(f"{Constants.APP_NAME}")

    def show_notification(
        self, message: str, duration: int = DEFAULT_NOTIFICATION_DURATION
    ) -> None:
        """Displays a notification with a custom message and duration.

        Args:
            message (str): The message to be displayed in the notification.
            duration (int): The duration in milliseconds for which the notification
                is displayed. Defaults to DEFAULT_NOTIFICATION_DURATION.
        """
        if self.enable_taskbar_notifications:
            self.showMessage(
                Constants.APP_NAME,
                message,
                QtWidgets.QSystemTrayIcon.Information,
                duration,
            )

    def show_running_notification(self, version: str) -> None:
        """Displays a notification indicating that Voxos is running."""
        self.show_notification(f"{Constants.APP_NAME} (v{version}) has launched.")
