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

""" 
    Utility classes for running command contexts to completion in parallel.
"""
import logging
import uuid
from functools import partial
from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

from voxos.services.agents import AgentService
from voxos.services.transcription import TranscriptionService
from voxos.ui.text_editor import TextEditor
from voxos.utils.constants import Constants
from voxos.utils.cursor import Cursor
from voxos.utils.prompts import Prompts

logger = logging.getLogger(__name__)


class Runner(QThread):
    """Handles the context runner.

    Attributes:
        agent: The agent service to use when processing the command.
        clipboard_content: The clipboard context.
        started_signal: The signal emitted when the runner starts.
        stopped_signal: The signal emitted when the runner stops.

    Args:
        agent: The agent service to use when processing the command.
        clipboard_content: The clipboard content when the runner was started.
    """

    started_signal = pyqtSignal()
    calculated_name = pyqtSignal(str, str)
    stopped_signal = pyqtSignal(QThread)

    def __init__(
        self,
        agent: AgentService,
        cursor: Cursor,
        clipboard_content: str = "",
        name: str = "",
    ) -> None:
        """Initializes the runner instance.

        Sets up the transcriber instance that will be used to proceed with the command.
        """

        QThread.__init__(self)
        self.agent = agent
        self.cursor = cursor
        self.clipboard_content = clipboard_content
        self.transcription_service = TranscriptionService()
        self.transcription_service.transcription_ready_signal.connect(
            self.process_transcript, QtCore.Qt.DirectConnection
        )
        self.audio_filename = None
        self.audio_delete_callback = None
        self.id = str(uuid.uuid4())
        self.short_id = self.id[:4]
        self.name = name if name else f"Generating name... ({self.short_id})"

        self.context_menu_callback = None

        logger.debug("Runner %s initialized.", self.id)

    def kill(self) -> None:
        """Kills the runner."""
        logger.debug("Runner %s - Killing...", self.id)
        self.terminate()
        self.stopped_signal.emit(self)

    def run(self) -> None:
        """Determines whether to transcribe provided audio or process clipboard content immediately."""
        if self.clipboard_content and not self.audio_filename:
            self.process_transcript(self.clipboard_content)
            return
        self.transcription_service.transcribe_file(
            self.audio_filename, self.audio_delete_callback
        )

    def set_name(self, prompt: str) -> None:
        """Sets the name of the runner based on the provided prompt."""
        runner_naming_model = Constants.RUNNER_NAMING_AGENT_MODEL
        runner_naming_agent = AgentService(
            model=runner_naming_model,
            system_prompt=Prompts.RUNNER_NAMING_PROMPT,
            name="Runner Naming Agent",
            summarization_type="naive",
        )
        self.name = runner_naming_agent.get_completion(prompt).replace('"', "")
        self.name = f"""{self.name}"""
        self.calculated_name.emit(self.name, self.short_id)

    def set_audio_parameters(self, filename: Path, delete_callback: callable) -> None:
        """Sets the audio parameters for the runner to take over transcription."""
        self.audio_filename = filename
        self.audio_delete_callback = delete_callback

    @pyqtSlot(str)
    def process_transcript(self, command: str) -> None:
        """Writes the transcript to the active window."""
        logger.info("Runner (%s) - Transcribed voice command: %s", self.id, command)

        context = "" if not command.strip() else f"{command}\n" + self.clipboard_content

        self.set_name(context)

        result = self.agent.get_completion(context)

        TextEditor().open_text_in_system_editor(result)

        self.stopped_signal.emit(self)
        logger.debug("Runner (%s) - Finished processing context.", self.id)


class RunnersManager(QObject):
    """Manages the active runners.

    Attributes:
        runners: The list of runners.
        number_of_runners_updated_signal: The signal emitted when the number of runners changes.
    """

    number_of_runners_updated_signal = pyqtSignal(int)

    def __init__(
        self,
    ) -> None:
        """Initializes the runner manager instance."""

        super().__init__()
        self.runners = []

    def add_runner(self, runner: Runner) -> None:
        """Adds a new runner to the manager."""
        logger.debug("Manager adding new runner...")
        runner.stopped_signal.connect(partial(self.remove_runner, runner))
        self.runners.append(runner)
        self.number_of_runners_updated_signal.emit(len(self.runners))

    @pyqtSlot(Runner)
    def remove_runner(self, runner: Runner) -> None:
        """Removes a runner from the manager."""
        logger.debug("Manager removing runner %s...", runner.id)
        self.runners.remove(runner)
        self.number_of_runners_updated_signal.emit(len(self.runners))
