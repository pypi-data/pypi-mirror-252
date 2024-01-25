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

import subprocess


class SystemVolumeController:
    """Singleton class for controlling the system volume on macOS"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemVolumeController, cls).__new__(cls)
        return cls._instance

    def set_volume(self, volume):
        """Set the system volume to the given level (0-100)"""
        subprocess.run(["osascript", "-e", f"set volume output volume {volume}"])

    def get_volume(self):
        """Get the current system volume level (0-100)"""
        result = subprocess.run(
            ["osascript", "-e", "output volume of (get volume settings)"],
            capture_output=True,
            text=True,
        )
        return int(result.stdout.strip())


def get_system_volume_controller() -> SystemVolumeController:
    """Returns the system volume controller singleton"""
    return SystemVolumeController()
