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
import platform

logger = logging.getLogger(__name__)

if platform.system() == "Windows":
    from voxos.utils.volume.windows import get_system_volume_controller
elif platform.system() == "Linux":
    from voxos.utils.volume.linux import get_system_volume_controller
elif platform.system() == "Darwin":
    from voxos.utils.volume.darwin import get_system_volume_controller
else:
    raise NotImplementedError("Unsupported platform: " + platform.system())


class VolumeController:
    """Manages the system volume.

    Attributes:
        active: Whether or not the volume controller will mute during recording.
        stored_volume: The master volume before it was set to off.
    """

    def __init__(self, no_mute: bool = False) -> None:
        """Initialize the volume class."""
        self.no_mute = no_mute
        self.stored_volume = None

    def set_active(self, active: bool) -> None:
        """Set whether or not the volume controller will mute during recording."""
        logger.debug("Setting volume controller active: %s", active)
        self.no_mute = not active

    def will_mute(self) -> bool:
        """Whether or not the volume controller will mute during recording."""
        return not self.no_mute

    def get_minimum_volume(self) -> float:
        """Get the minimum volume for the current system."""
        system_volume_controller = get_system_volume_controller()
        min_volume, _, _ = system_volume_controller.GetVolumeRange()
        return min_volume

    def sample_current_volume(self) -> float:
        """Get the current system volume."""
        system_volume_controller = get_system_volume_controller()
        return system_volume_controller.GetMasterVolumeLevel()

    def set_volume(self, volume) -> None:
        """Set the system volume."""
        if self.no_mute:
            return None
        get_system_volume_controller().SetMasterVolumeLevel(volume, None)

    def set_off(self) -> None:
        """Set the volume to off."""
        self.stored_volume = self.sample_current_volume()
        self.set_volume(self.get_minimum_volume())

    def set_to_stored(self) -> None:
        """Set the volume to the stored volume."""
        self.set_volume(self.stored_volume)
