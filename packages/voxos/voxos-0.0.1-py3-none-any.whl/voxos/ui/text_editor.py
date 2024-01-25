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
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class TextEditor(QWidget):
    """Provides access to a text editor."""

    supported_editors = {
        "Sublime Text": "subl",
        "Atom": "atom",
        "Visual Studio Code": "code",
        "Notepad": "notepad",
        "Notepad++": "notepad++",
        "Vim": "vim",
        "Emacs": "emacs",
        "Brackets": "brackets",
        "TextMate": "mate",
        "gedit": "gedit",
        "Nano": "nano",
    }

    preferred_editor = "notepad"  # default

    def __init__(self, preferred_editor: str = None):
        super().__init__()
        if preferred_editor is not None:
            self.set_preferred_editor(preferred_editor)

    def set_preferred_editor(self, editor_name: str):
        """Sets the preferred editor if it is supported.

        Args:
            editor_name: The name of the preferred editor.

        Raises:
            ValueError: If the editor is not supported.
        """
        if editor_name in self.supported_editors.values():
            self.__class__.preferred_editor = editor_name
        else:
            raise ValueError(
                f"Unsupported editor: {editor_name}. Please choose from the following: {', '.join(self.supported_editors.values())}"
            )

    def open_text_in_system_editor(self, text: str) -> None:
        """Opens the text in the system editor.

        Args:
            text: The text to open.

        """

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".txt", mode="w+", encoding="utf-8"
        ) as tmp_file:
            tmp_file.write(text)
            tmp_file_path = tmp_file.name

        editor = self.__class__.preferred_editor

        try:
            if sys.platform == "win32":
                editor_command = [editor, tmp_file_path]
            elif sys.platform == "darwin":
                editor_command = ["open", "-e", tmp_file_path]
            else:  # Assuming Linux or similar
                editor_command = ["xdg-open", tmp_file_path]

            subprocess.Popen(editor_command)
        except FileNotFoundError:
            logger.warning(
                f"Could not find `{editor}` editor on your system. It is either not installed on your system or not in your PATH."
            )

    @pyqtSlot()
    def check_editor_closed(self):
        """Checks if the editor has been closed."""
        if self.editor_process.poll() is not None:
            # The editor has been closed
            self.editor_timer.stop()
            self.text_editor_closed()

    def text_editor_closed(self):
        """Handles the text editor being closed."""
        with open(self.opened_file.name, "r", encoding="utf-8") as file:
            content = file.read()

        self.file_modified_signal.emit(
            content.strip() != self.original_content,
            self.is_temp_file,
            self.opened_file.name,
        )

        if self.is_temp_file and not self.opened_file.closed:
            os.remove(self.opened_file.name)
