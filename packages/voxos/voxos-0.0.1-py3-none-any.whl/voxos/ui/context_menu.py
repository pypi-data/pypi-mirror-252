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
from datetime import datetime
from functools import partial

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QEvent, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAction, QActionGroup, QMenu, QToolTip

from voxos.utils.runner import Runner

logger = logging.getLogger(__name__)

from voxos.utils.constants import Constants


class ToolTipMenu(QMenu):
    """QMenu override to show tooltips on hover for actions."""

    def event(self, event):
        """Override event handler to show tooltips on hover."""
        if event.type() == QEvent.ToolTip:
            action = self.actionAt(event.pos())
            if action:
                QToolTip.showText(event.globalPos(), action.toolTip())
            else:
                QToolTip.hideText()
            return True
        return super().event(event)


class ResponseDetailAction(QAction):
    """Selector for the response detail level."""

    def __init__(self, parent: object, detail_level_changed_signal: pyqtSignal):
        super().__init__("Response detail level", parent)
        self.setCheckable(True)
        self.setToolTip(
            f"Change the level of detail {Constants.APP_NAME} uses for future responses"
        )
        self.detail_level_changed_signal = detail_level_changed_signal
        self.response_detail_group = QActionGroup(self)

        detail_levels = {
            "Minimal": None,
            "Brief": None,
            "Normal": None,
            "Detailed": None,
            "Extensive": None,
        }

        for level in detail_levels:
            detail_levels[level] = QAction(level, self.response_detail_group)
            detail_levels[level].setCheckable(True)
            detail_levels[level].triggered.connect(
                lambda checked, level=level: self.on_detail_level_selected(level)
            )
            self.response_detail_group.addAction(detail_levels[level])

        self.response_detail_submenu = QMenu("Response detail level")
        for level, action in detail_levels.items():
            self.response_detail_submenu.addAction(action)

        self.setMenu(self.response_detail_submenu)

    def on_detail_level_selected(self, level: str) -> None:
        """Slot for emitting the parent's signal when a detail level is selected."""
        self.detail_level_changed_signal.emit(level)

    def set_current_state(self, level: str) -> None:
        """Sets the current state of the response detail level."""
        for action in self.response_detail_group.actions():
            if action.text() == level:
                action.setChecked(True)
                break


class RunnerMenu(QMenu):
    """Menu for killing the active runners."""

    none_action = None
    kill_runner_prefix = "Force stop: "

    def __init__(self, parent: object):
        super().__init__("Runners", parent)
        self.none_action = KillRunnerAction(name="None", enabled=False, parent=self)
        self.setToolTip(f"Immediately stop the process handling this request.")
        self.addAction(self.none_action)

    def add_runner_action(self, runner: Runner) -> None:
        """Adds a new runner to the 'Runners' menu."""
        new_runner_action = QAction(f"{self.kill_runner_prefix} {runner.name}", self)
        if self.none_action in self.actions():
            self.removeAction(self.none_action)

        new_runner_action.triggered.connect(runner.kill, QtCore.Qt.DirectConnection)
        new_runner_action.triggered.connect(
            partial(self.remove_runner_from_menu, runner)
        )
        self.addAction(new_runner_action)
        runner.stopped_signal.connect(partial(self.remove_runner_from_menu, runner))
        # TODO @Falimonda - Handle case where other process stops or kills the runner

    def remove_runner_from_menu(self, runner: Runner) -> None:
        """Removes a runner from the 'Runners' menu."""
        logger.info("Removing runner %s from context menu", runner.name)
        for action in self.actions():
            if action.text() == f"{self.kill_runner_prefix} {runner.name}":
                logger.info("match found - removing action")
                self.removeAction(action)
                break
        if len(self.actions()) == 0:
            self.addAction(self.none_action)


class MemoryAction(QAction):
    """Action for toggling the agent memory setting."""

    def __init__(self, parent: object):
        super().__init__("Enable memory", parent)
        self.setToolTip(
            f"Toggle whether {Constants.APP_NAME} remembers your previous commands' context.\n\n This will clear past context every time you toggle it."
        )
        self.setCheckable(True)
        self.setChecked(False)


class KillRunnerAction(QAction):
    """Action for killing a runner."""

    def __init__(self, name: str, enabled: bool, parent: object):
        super().__init__(name, parent)
        self.setEnabled(enabled)


class SpeakerMuteToggleAction(QAction):
    """Action for toggling the speaker mute feature."""

    def __init__(self, parent: object):
        super().__init__("Mute speakers on record", parent)
        self.setToolTip(
            f"Toggle whether {Constants.APP_NAME} mutes your speakers when listening to you."
        )
        self.setCheckable(True)


class ToggleHUDAction(QAction):
    """Action for toggling the HUD visibility."""

    def __init__(self, parent: object):
        super().__init__("Toggle HUD visibility", parent)
        self.setToolTip(
            f"Toggle whether {Constants.APP_NAME}'s HUD is visible. You'll need to use the system tray toolbar to show it again."
        )


class AboutAction(QAction):
    """Action for showing the About window."""

    def __init__(self, parent: object):
        super().__init__("About", parent)
        self.setToolTip(f"About {Constants.APP_NAME}")


class AboutWindow(QtWidgets.QMessageBox):
    """'About' window class providing details about the application."""

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("About")
        self.setTextFormat(Qt.RichText)
        beta_release = "[Beta Release] " if int(Constants.APP_VERSION[0]) < 1 else ""
        self.setText(
            f"{Constants.APP_NAME} {beta_release}- v{Constants.APP_VERSION}<br/>"
            f"<br/>"
            f"Copyright © 2023-{datetime.now().year} {Constants.APP_AUTHOR}<br/>"
            f"Licensed under {Constants.APP_LICENSE}<br/>"
            f"<br/>"
            f"For notable updates, <a href='{Constants.APP_SUBSCRIBE_LINK}'>subscribe here</a><br/><br/>"
            f"For more information, "
            f"<a href='{Constants.APP_SITE_LINK}'>visit our website</a><br/><br/>"
            f"For support, "
            f"<a href='{Constants.APP_SUPPORT_LINK}'>create a ticket</a><br/>"
        )
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setIconPixmap(
            QPixmap(Constants.APP_ICON_PNG_PATH).scaled(100, 100, Qt.KeepAspectRatio)
        )


class ExitAction(QAction):
    """Action for exiting Voxos."""

    def __init__(self, parent: object):
        super().__init__("Exit", parent)
        self.setToolTip(f"Exit {Constants.APP_NAME} and stop all runners immediately.")


class ContextMenu(QtWidgets.QMenu):
    """Provides a context menu for the system tray icon and HUD."""

    new_runner_added_signal = pyqtSignal(object)
    runner_name_updated_signal = pyqtSignal(str, str)
    response_details_changed_signal = pyqtSignal(str)
    speaker_mute_toggled = pyqtSignal(bool)
    runner_killed_signal = pyqtSignal(str)
    runner_memory_action_signal = pyqtSignal(bool)
    toggle_hud_action_signal = pyqtSignal()
    exit_action_signal = pyqtSignal()

    runners_menu = None

    def __init__(self, parent: object = None):
        super().__init__()
        self.parent = parent

        # For controlling runners
        self.runners_menu = RunnerMenu(self)
        self.new_runner_added_signal.connect(
            self.add_runner_to_menu, QtCore.Qt.QueuedConnection
        )
        self.runner_name_updated_signal.connect(
            self.update_runner_name_in_menu, QtCore.Qt.QueuedConnection
        )
        self.addMenu(self.runners_menu)

        # For settings
        self.settings = ToolTipMenu(self)
        self.settings.setTitle("Settings")
        self.addMenu(self.settings)

        ## Agent memory setting
        self.memory_action = MemoryAction(self)
        self.memory_action.triggered.connect(self.runner_memory_action_signal)
        self.settings.addAction(self.memory_action)

        # Response detail setting
        self.response_detail_action = ResponseDetailAction(
            self, self.response_details_changed_signal
        )
        self.settings.addAction(self.response_detail_action)

        # For toggling the speaker mute indicator
        self.speaker_mute_toggle_action = SpeakerMuteToggleAction(self)
        self.speaker_mute_toggle_action.triggered.connect(
            self.signal_speaker_mute_changed
        )
        self.settings.addAction(self.speaker_mute_toggle_action)

        # For toggling the HUD visibility
        toggle_hud_action = ToggleHUDAction(self)
        toggle_hud_action.triggered.connect(self.toggle_hud)
        self.settings.addAction(toggle_hud_action)

        # For showing the About window
        about_action = AboutAction(self)
        about_action.triggered.connect(self.show_about_window)
        self.addAction(about_action)

        # For exiting Voxos
        exit_action = ExitAction(self)
        exit_action.triggered.connect(self.exit_application)
        self.addAction(exit_action)

    # State setters for syncing to initial state
    def set_speaker_mute_indicator_state(self, checked: bool) -> None:
        """Set the speaker mute indicator."""
        self.speaker_mute_toggle_action.setChecked(checked)

    def set_voxos_response_detail_state(self, level: str) -> None:
        """Set the response detail level state."""
        self.response_detail_action.set_current_state(level)

    def set_voxos_memory_state(self, memory: bool) -> None:
        """Set the memory state."""
        self.memory_action.setChecked(memory)

    # Emitters
    def add_runner(self, runner):
        """Emits the signal to add runners to the 'Runners' menu."""
        self.new_runner_added_signal.emit(runner)

    def update_runner_name(self, name: str, short_id: str) -> None:
        """Slot to update the name of the existing runner in the 'Runners' menu."""
        self.runner_name_updated_signal.emit(name, short_id)

    def signal_speaker_mute_changed(self) -> None:
        """Emits the signal that the speaker mute indicator has changed."""
        self.speaker_mute_toggled.emit(self.speaker_mute_toggle_action.isChecked())

    def toggle_hud(self) -> None:
        """Emits the signal to toggle the HUD visibility."""
        self.toggle_hud_action_signal.emit()

    def exit_application(self) -> None:
        """Emits the signal to exit the application."""
        self.exit_action_signal.emit()

    # Slots
    @pyqtSlot(object)
    def add_runner_to_menu(self, runner: Runner) -> None:
        """Slot to dynamically add runners to the 'Runners' menu."""
        logger.info("Adding runner %s to context menu", runner.name)
        self.runners_menu.add_runner_action(runner)

    @pyqtSlot(str, str)
    def update_runner_name_in_menu(self, name: str, short_id: str) -> None:
        """Slot to dynamically update the name of the existing runner in the 'Runners' menu."""
        for action in self.runners_menu.actions():
            if short_id in action.text():
                action.setText(f"{self.runners_menu.kill_runner_prefix} {name}")
                break

    @pyqtSlot(bool)
    def show_about_window(self, _: bool) -> None:
        """Shows the About window."""
        about_window = AboutWindow()
        about_window.exec_()
