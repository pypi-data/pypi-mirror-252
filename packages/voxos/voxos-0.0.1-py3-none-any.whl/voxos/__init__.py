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

import keyboard

from voxos.services.agents import AgentService
from voxos.ui.context_menu import ContextMenu
from voxos.ui.hud import HeadsUpDisplay
from voxos.ui.system_tray import SystemTrayIcon
from voxos.utils.audio_recorder import AudioRecorder
from voxos.utils.cursor import Cursor
from voxos.utils.hotkeys import Hotkeys
from voxos.utils.runner import Runner, RunnersManager
from voxos.utils.volume import VolumeController
from voxos.version import __version__

logger = logging.getLogger(__name__)

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class Voxos(QObject):
    """Handles primary Voxos application logic."""

    transcribe_only_mode = True
    processing_started_signal = pyqtSignal()
    processing_stopped_signal = pyqtSignal()

    def __init__(
        self,
        audio_recorder: AudioRecorder,
        system_tray: SystemTrayIcon,
        hotkeys: Hotkeys,
        agent_service: AgentService,
        hud: HeadsUpDisplay,
        cursor: Cursor,
        context_menu: ContextMenu,
        volume_controller: VolumeController,
    ):
        super().__init__()

        # Dependencies
        self.audio_recorder = audio_recorder
        self.system_tray = system_tray
        self.hotkeys = hotkeys
        self.agent_service = agent_service
        self.hud = hud
        self.cursor = cursor
        self.context_menu = context_menu
        self.volume_controller = volume_controller

        # Utils configuration
        try:
            self.cursor.clear_clipboard()
        except Exception as e:  # for headless test runs pylint: disable=broad-except
            logger.warning(e)
        self.runner_manager = RunnersManager()
        self.runner_manager.number_of_runners_updated_signal.connect(
            self.hud.set_runners_bubble_int, QtCore.Qt.DirectConnection
        )

        # UI setup
        self.context_menu.speaker_mute_toggled.connect(
            self.volume_controller.set_active
        )
        self.context_menu.set_speaker_mute_indicator_state(
            self.volume_controller.will_mute()
        )
        self.context_menu.set_voxos_response_detail_state(
            self.agent_service.get_response_detail_level()
        )
        self.context_menu.set_voxos_memory_state(
            self.agent_service.get_memory_enabled_state()
        )
        self.hud.set_context_menu(self.context_menu)
        self.system_tray.set_context_menu(self.context_menu)
        self.system_tray.show_running_notification(__version__)
        self.setup_hotkeys()

        # Agent setup
        self.context_menu.response_details_changed_signal.connect(
            self.agent_service.response_level_detail_changed
        )

    def setup_hotkeys(self) -> None:
        """Sets up the hotkeys."""
        self.setup_listening_hotkey(self.hotkeys.listening_toggle_hotkey)
        self.hotkeys.print_config()

    def setup_signals(self) -> None:
        """Sets up various application signals and slots on initialization."""

        # Audio recording slots/signal connections
        self.audio_recorder.recording_started_signal.connect(
            self.hud.show_recording, QtCore.Qt.DirectConnection
        )
        self.audio_recorder.recording_started_signal.connect(
            self.volume_controller.set_off, QtCore.Qt.DirectConnection
        )
        self.audio_recorder.recording_started_signal.connect(
            self.cursor.store_copied_text, QtCore.Qt.DirectConnection
        )
        self.audio_recorder.recording_empty_signal.connect(
            self.received_empty_voice_command_handler, QtCore.Qt.DirectConnection
        )
        self.audio_recorder.recording_stopped_signal.connect(
            self.hud.display_idle, QtCore.Qt.DirectConnection
        )
        self.audio_recorder.recording_stopped_signal.connect(
            self.volume_controller.set_to_stored, QtCore.Qt.DirectConnection
        )
        self.audio_recorder.recorded_file_ready_signal.connect(
            self.received_voice_command_handler, QtCore.Qt.DirectConnection
        )

        # Context Menu slots/signal connections
        self.context_menu.toggle_hud_action_signal.connect(
            self.hud.toggle_visibility, QtCore.Qt.DirectConnection
        )
        self.context_menu.exit_action_signal.connect(
            QtWidgets.qApp.quit, QtCore.Qt.DirectConnection
        )
        self.context_menu.runner_memory_action_signal.connect(
            self.agent_service.set_memory
        )

        # HUD slots/signal connections
        self.processing_stopped_signal.connect(
            self.hud.display_idle, QtCore.Qt.DirectConnection
        )
        self.hud.click_and_lift_signal.connect(self.audio_recorder.toggle_recording)

    def setup_listening_hotkey(self, hotkey: str) -> None:
        """Sets up the hotkey to toggle recording."""
        try:
            keyboard.add_hotkey(hotkey, self.audio_recorder.toggle_recording)
        except Exception as e:  # for headless test runs pylint: disable=broad-except
            logger.warning(e)

    @pyqtSlot(bool, bool, Path)
    def process_file_modification(
        self, is_modified: bool, is_temp: bool, file_path: Path
    ) -> None:
        """Processes the file modification."""
        logging.debug(
            "File modification detected: %s, %s, %s",
            is_modified,
            is_temp,
            str(file_path),
        )

    def start_context_runner(
        self, filename: Path = None, delete_callback: callable = None
    ) -> None:
        """
        Starts the context runner, with setup dependent on whether audio was captured, as well as clipboard state.
        """

        if (
            not self.cursor.copied_text.strip()
            and filename is None
            and delete_callback is None
        ):
            logger.info("No context to process. No runner will be started.")
            return

        logger.debug("Starting new context runner.")
        runner = Runner(
            agent=self.agent_service,
            clipboard_content=self.cursor.copied_text,
            cursor=self.cursor,
        )

        # Add the runner to the manager and context menus
        self.runner_manager.add_runner(runner)
        self.context_menu.add_runner(runner)

        # Set up signals and slots to allow the runner to rename itself
        runner.calculated_name.connect(self.context_menu.update_runner_name)

        if filename is not None and delete_callback is not None:
            runner.set_audio_parameters(filename, delete_callback)

        runner.start()

        # Clear the clipboard to setup for the next context
        self.cursor.clear_clipboard()

    @pyqtSlot()
    def received_empty_voice_command_handler(self) -> None:
        """Handles the empty voice command."""
        logger.debug("Received empty voice command.")
        self.start_context_runner()

    @pyqtSlot(str, object)
    def received_voice_command_handler(
        self, filename: Path, delete_callback: callable
    ) -> None:
        """
        Starts the context runner, giving it the recorded audio file and delete callback.
        """
        logger.debug("Received voice command.")
        self.start_context_runner(filename, delete_callback)
