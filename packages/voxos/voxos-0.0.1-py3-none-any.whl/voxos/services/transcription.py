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

import datetime
import logging
from typing import Callable

import openai
from PyQt5.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)


class TranscriptionService(QObject):
    """Handles audio transcription using OpenAI's Whisper model.

    Attributes:
        WHISPER_MODEL_VERSION (str): The version of the Whisper model to use.
        transcription_ready_signal (pyqtSignal): Signal emitted when transcription is ready.

    """

    WHISPER_MODEL_VERSION = "whisper-1"
    transcription_ready_signal = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

    def transcribe_file(
        self, audio_file_path: str, delete_callback: Callable[[], None]
    ) -> None:
        """Transcribe the given audio file and emit signal when done.

        Args:
            audio_file_path: Path to the audio file.
            delete_callback: A callback function to be called after transcription.
        """
        try:
            transcript = self.transcribe(audio_file_path)
            delete_callback()
            self.transcription_ready_signal.emit(
                transcript if transcript is not None else ""
            )
        except Exception as e:
            logger.error("Error during transcription: %s", e)

    def transcribe(self, audio_file_path: str) -> str:
        """Transcribe the given audio file.

        Args:
            audio_file_path: Path to the audio file.

        Returns:
            The transcribed text as a string, or an empty string if an error occurs.
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = openai.audio.transcriptions.create(
                    file=audio_file, model=self.WHISPER_MODEL_VERSION
                )
                logger.debug(
                    "Received local transcript at %s. Transcript: %s",
                    datetime.datetime.now(),
                    transcript,
                )
                return transcript.text
        except FileNotFoundError as e:
            logger.error("File not found during local transcription: %s", e)
            return ""
        except openai.OpenAIError as e:
            logger.error("OpenAI error during local transcription: %s", e)
            return ""
