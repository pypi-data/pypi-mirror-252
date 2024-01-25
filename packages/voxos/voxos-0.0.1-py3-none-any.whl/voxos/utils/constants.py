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

""" A class for Voxos constants. """
from voxos.version import __version__


class Constants:
    """Class containing application constants.

    This class is not meant to be instantiated but used to access
    application-wide constants.

    Attributes:
        APP_NAME (str): Name of the application.
        APP_VERSION (str): Current version of Voxos.
        APP_AUTHOR (str): Author of Voxos.
        APP_HOSTED_SERVICES_URL (str): URL to Voxos's hosted services.
        APP_ICON_PNG_PATH (str): Path to the application icon.
        APP_CONTACT_LINK (str): Path to application contact form.
        RECORDING_ICON_PNG_PATH (str): Path to the recording icon.
        PROCESSING_ICON_PNG_PATH (str): Path to the processing icon.
        VOXOS_AGENT_NAME (str): Name of the Voxos agent.

    """

    APP_NAME: str = "Voxos"
    APP_VERSION: str = __version__
    APP_AUTHOR: str = "Voxos.ai Inc."
    APP_SUPPORT_LINK: str = (
        "https://gitlab.com/voxos.ai/voxos-desktop-client/-/issues/new"
    )
    APP_CONTACT_LINK: str = "https://www.voxos.ai/?contact"
    APP_SITE_LINK: str = "https://www.voxos.ai"
    APP_SUBSCRIBE_LINK: str = f"{APP_SITE_LINK}/?subscribe=true"
    APP_LICENSE: str = "GNU GPLv3"
    APP_ICON_PNG_PATH = "icons/icon-mini.png"
    RECORDING_ICON_PNG_PATH = "icons/icon-mini-red.png"
    PROCESSING_ICON_PNG_PATH = "icons/icon-mini-blue.png"

    VOXOS_AGENT_NAME = "Voxos"
    VOXOS_AGENT_MODEL = "gpt-4"  # "gpt-4-1106-preview"
    RUNNER_NAMING_AGENT_MODEL = "gpt-3.5-turbo"

    def __init__(self):
        """Prevent instantiation of this class."""
        raise NotImplementedError("This class is not meant to be instantiated.")
