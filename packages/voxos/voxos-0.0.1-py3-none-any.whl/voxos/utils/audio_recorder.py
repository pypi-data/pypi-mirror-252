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
    A utlitity class for audio recording.
"""
import logging
import os
import tempfile
import threading
import time
import wave
from functools import partial
from pathlib import Path

import numpy as np
import pyaudio
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from voxos.utils.common import print_log
from voxos.utils.constants import Constants

logger = logging.getLogger(__name__)


class AudioRecorder(QObject):
    """Handles the recording of audio to a file.

    Attributes:
        recorded_file_ready_signal (pyqtSignal): Signal emitted when the recorded file is ready.
        recording_started_signal (pyqtSignal): Signal emitted when recording starts.
        recording_stopped_signal (pyqtSignal): Signal emitted when recording stops.
        DEBOUNCE_INTERVAL (float): The minimum time between toggles. This is critical to keeping seg faults from happening.
    """

    recorded_file_ready_signal = pyqtSignal(str, object)
    recording_started_signal = pyqtSignal()
    recording_stopped_signal = pyqtSignal()
    recording_empty_signal = pyqtSignal()

    DEBOUNCE_INTERVAL = 0.5  # seconds
    MINIMUM_RMS_ENERGY = 15

    def __init__(self) -> None:
        """Initializes the audio recorder."""
        super().__init__()
        self.is_recording = False
        self.frames = []
        self.stream = None
        self.pyaudio_instance = pyaudio.PyAudio()
        self.lock = threading.Lock()
        self.last_toggle_timestamp = 0  # Timestamp for last toggle

    def _start_recording(self) -> None:
        """Starts the recording of audio with a lock."""
        with self.lock:
            if self.is_recording:
                return
            self.is_recording = True

        print_log("Started listening...")
        self.recording_started_signal.emit()
        self.frames = []
        self.stream = self.pyaudio_instance.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024,
        )

        while True:
            with self.lock:
                if not self.is_recording:
                    break
            try:
                data = self.stream.read(1024)
                self.frames.append(data)
            except Exception as e:
                logger.error(f"Error during recording: {e}")
                break

        self._finalize_recording()

    def _finalize_recording(self) -> None:
        """Finalizes the recording process and signals that the recorded file is ready."""
        print_log("Stopped listening...")
        self.recording_stopped_signal.emit()

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        temp_filename = os.path.join(
            tempfile.gettempdir(), os.urandom(24).hex() + ".wav"
        )

        logger.debug("Frames recorded: %s", len(self.frames))
        if not self.frames:
            self.recording_empty_signal.emit()
            return

        frames_int = [np.frombuffer(frame, np.int16) for frame in self.frames]
        frames_concat = np.concatenate(frames_int)
        energy = np.sqrt(np.mean(frames_concat**2))

        logger.debug("Recording RMS energy: %s", energy)
        if energy < self.MINIMUM_RMS_ENERGY:
            print_log(
                f"I was listening but didn't hear you say anything... If you believe this is an error, please open a ticket at: {Constants.APP_SUPPORT_LINK}",
            )
            self.recording_empty_signal.emit()
            return

        with wave.open(temp_filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.pyaudio_instance.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b"".join(self.frames))

        logger.info("Emitting recorded file: %s", temp_filename)
        self.recorded_file_ready_signal.emit(
            temp_filename, partial(self.delete_callback, temp_filename)
        )

    def _stop_recording(self) -> None:
        """Stops the recording of audio."""
        with self.lock:
            if not self.is_recording:
                return
            self.is_recording = False

    def delete_callback(self, filename: Path) -> None:
        """Deletes the temporary file.

        Args:
            filename (str): The filename to delete.
        """
        logger.debug("Deleting temporary file: %s", str(filename))
        os.remove(filename)

    def start_recording(self) -> None:
        """Starts the audio recording thread."""
        logger.debug("Starting recording thread...")
        threading.Thread(target=self._start_recording, daemon=True).start()

    def stop_recording(self) -> None:
        """Stops the audio recording thread."""
        logger.debug("Stopping recording thread...")
        threading.Thread(target=self._stop_recording, daemon=True).start()

    @pyqtSlot()
    def toggle_recording(self):
        """Toggles the recording of audio."""
        current_time = time.time()
        if current_time - self.last_toggle_timestamp < self.DEBOUNCE_INTERVAL:
            logger.debug("Toggle recording called too soon, ignoring.")
            return

        self.last_toggle_timestamp = current_time
        logger.debug("Toggling recording...")

        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def __del__(self):
        self.pyaudio_instance.terminate()
