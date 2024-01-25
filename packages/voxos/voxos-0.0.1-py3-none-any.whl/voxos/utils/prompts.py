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

""" A class for Voxos static prompts. """


class Prompts:
    """Class containing Voxos static prompts.

    This class is not meant to be instantiated but used to access
    application-wide static prompts.

    Attributes:
        VOXOS_AGENT_SYSTEM_PROMPT (str): System prompt for the primary Voxos agent.
        VOXOS_TASK_GENERATOR_SYSTEM_PROMPT (str): System prompt for the Voxos task generator agent.
    """

    VOXOS_AGENT_SYSTEM_PROMPT = """
        You are an operating system assistant that helps people with their daily tasks while working on their computer.
    """

    TASK_GENERATOR_SYSTEM_PROMPT = """
        You are an operating system assistant that helps people with their daily tasks while working on their computer.
        Respond only with the bare minimum to comply with the user's request unless asked to elaborate.
        Err on the side of listing things step-by-step.
    """

    RUNNER_NAMING_PROMPT = """
        Provide a two to three word title that captures the spirit of the provided text.
        Do not respond with more than 2-3 words. The title should be placed within double quotes.
    """

    def __init__(self):
        """Prevent instantiation of this class."""
        raise NotImplementedError("This class is not meant to be instantiated.")
