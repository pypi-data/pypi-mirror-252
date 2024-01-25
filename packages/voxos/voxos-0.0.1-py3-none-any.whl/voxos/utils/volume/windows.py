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

"""This module contains the volume controller for Windows."""

from ctypes import POINTER, cast

import comtypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class SystemVolumeController:
    """Singleton class for controlling the system volume on Windows"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemVolumeController, cls).__new__(cls)
            comtypes.CoInitialize()
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            cls._instance.controller = cast(interface, POINTER(IAudioEndpointVolume))
        return cls._instance.controller

    @classmethod
    def cleanup(cls) -> None:
        """Cleanup the COM interface"""
        if cls._instance:
            comtypes.CoUninitialize()
            cls._instance = None


def get_system_volume_controller() -> SystemVolumeController:
    """Returns the system volume controller singleton"""
    return SystemVolumeController()
