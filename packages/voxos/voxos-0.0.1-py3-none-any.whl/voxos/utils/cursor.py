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

""" A utlitity class for interfacing with the cursor and clipboard."""

import logging
import time

import pyautogui
import pyperclip
from PyQt5.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)


class Cursor(QObject):
    """Candles the cursor and clipboard."""

    ctrl_c = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.selected_text = None
        self.copied_text = None

    def store_selected_text(self):
        """Stores the selected text in the selected_text attribute."""
        pyperclip.copy("")
        time.sleep(0.1)
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.1)
        self.selected_text = pyperclip.paste()

    def paste_text(self, text) -> None:
        """Pastes the text into the current cursor position."""
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")

    def get_copied_text(self) -> str:
        """Returns the text that is currently copied."""
        return pyperclip.paste()

    def store_copied_text(self):
        """Stores the text that is currently copied."""
        self.copied_text = self.get_copied_text()

    def clear_clipboard(self) -> None:
        """Clears the clipboard."""
        pyperclip.copy("")
