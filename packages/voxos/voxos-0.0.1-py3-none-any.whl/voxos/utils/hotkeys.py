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

""" This is the hotkeys module that contains the Hotkeys class. """


class Hotkeys:
    """Manages hotkey configurations for Voxos."""

    DEFAULT_LISTENING_TOGGLE_HOTKEY = "ctrl+alt+z"

    def __init__(self):
        """Initializes the hotkeys with default settings."""
        self.configure_default_hotkeys()

    def configure_default_hotkeys(self) -> None:
        """Configures the default hotkey settings."""
        self.listening_toggle_hotkey = self.DEFAULT_LISTENING_TOGGLE_HOTKEY

    def set_listening_hotkey(self, key_combo: str) -> None:
        """Sets the recording hotkey."""
        self.listening_toggle_hotkey = key_combo

    def print_config(self) -> None:
        """Logs the current hotkey configuration.

        This uses print on purpose.
        """
        print("Current hotkey configuration:")
        print(f"\tListening Toggle Hotkey: {self.listening_toggle_hotkey}\n")
