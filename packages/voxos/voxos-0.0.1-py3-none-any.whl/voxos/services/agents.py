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

import json
import logging
from typing import List

import openai
import requests
import tiktoken
from openai import OpenAI
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from voxos.services.models.openai import models as openai_models

logger = logging.getLogger(__name__)


def get_available_models() -> List[str]:
    """Provides the list of available models from OpenAI."""
    headers = {"Authorization": f"Bearer {openai.api_key}"}
    response = requests.get(
        "https://api.openai.com/v1/models", headers=headers, timeout=3
    )
    models = response.json()["data"]
    return [model["id"] for model in models]


class AgentService(QObject):
    """This encapsulates the agent's state and behavior."""

    completion_ready_signal = pyqtSignal(str)

    def __init__(
        self,
        model: str,
        system_prompt: str = None,
        memory: bool = False,
        messages: list = None,
        name: str = None,
        response_detail_level: str = None,
        summarization_type: str = "truncation",
    ) -> None:
        """Initialize the agent.

        Assumes that the first message is the system message.

        Args:
            system_prompt: The system prompt to use.
            memory: Whether or not the agent should remember the conversation.
            messages: The historical messages to use, if any.
            name: The name of the agent.
            model: The LLM model to use.
            response_detail_level: The level of detail to use for responses.

        """
        super().__init__()

        self.openai_client = OpenAI(api_key=openai.api_key)

        self.name = name
        self.logger_name_string = f"({self.name}) " if self.name else ""

        self.system_prompt = system_prompt
        self.response_detail_level = response_detail_level

        self.messages = messages
        self.memory = memory
        if model not in get_available_models():
            raise ValueError(f"Model {model} is not available.")
        self.model = model
        self.max_tokens = next(
            (m["max_tokens"] for m in openai_models if m["id"] == self.model), None
        )
        logger.debug("Max tokens for model %s: %s", self.model, self.max_tokens)

        self.summarization_type = summarization_type

        self.update_response_detail_level(self.response_detail_level)
        self.update_system_message()

        if self.get_system_prompt_token_count() > self.max_tokens:
            raise ValueError(
                f"System prompt token count ({self.get_system_prompt_token_count()}) exceeds max tokens ({self.max_tokens})."
            )

    def update_system_message(self) -> None:
        """Sets the system message, considering prompt and detail level."""
        self.system_message = {
            "role": "system",
            "content": f""" {self.system_prompt if self.system_prompt else ''}
                            {self.response_detail_prompt if self.response_detail_prompt else ''}
                        """,
        }
        if self.messages:
            self.messages[0] = self.system_message
        else:
            self.messages = [self.system_message]

        logger.debug(
            "Updated agent %s system message to %s",
            f"({self.name}) " if self.name else "",
            self.system_message,
        )

    def update_response_detail_level(self, level: str) -> None:
        """Updates the response detail level prompt."""
        logger.debug(
            "Setting agent %sresponse detail level: %s",
            f"({self.name}) " if self.name else "",
            level,
        )
        self.response_detail_prompt = (
            (f"Your must respond with a {level.lower()} level of detail.")
            if level
            else ""
        )

    def response_level_detail_changed(self, level: str) -> None:
        """Slot for handling a change in the response detail level."""
        self.update_response_detail_level(level)
        self.update_system_message()

    def get_response_detail_level(self) -> str:
        """Gets the response detail level prompt."""
        return self.response_detail_level

    def add_response(self, role: str, response: str) -> None:
        """Adds a response to the messages."""
        self.messages.append({"role": role, "content": response})

    def add_assistant_response(self, response: str) -> None:
        """Adds assistant response to the messages."""
        self.add_response("assistant", response)

    def add_user_response(self, response: str) -> None:
        """Adds a user response to the messages."""
        self.add_response("user", response)

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the API call.

        Args:
            prompt: The user's first or next prompt.
        Returns:
            The completion.
        """
        try:
            if not self.memory:
                self.messages = [self.system_message]
            self.add_user_response(prompt)
            self.check_and_summarize_text()

            api_response = self.openai_client.chat.completions.create(
                model=self.model, messages=self.messages, temperature=0.1, stream=False
            )
            completion = api_response.choices[0].message.content
            logger.debug(
                "Agent %scompletion: %s",
                self.logger_name_string,
                completion,
            )
            self.completion_ready_signal.emit(
                completion if completion is not None else ""
            )

            if self.memory:
                self.add_assistant_response(completion)

            return completion
        except openai.AuthenticationError as e:
            logger.error("Authentication error: %s", e)
            return f"Sorry, I'm having trouble connecting to the OpenAI API. Please check your API key and try again. {self.logger_name_string}"

        except openai.InternalServerError as e:
            logger.error("Internal server error: %s", e)
            return f"The request to the OpenAI API resulted in an internal server error. {self.logger_name_string}"

        except openai.PermissionDeniedError as e:
            logger.error("Permission denied error: %s", e)
            return f"Permission denied for the requested OpenAI API operation. {self.logger_name_string}"

        except openai.RateLimitError as e:
            logger.error("Rate limit error: %s", e)
            return f"The rate limit for the OpenAI API has been exceeded. Please try again later. {self.logger_name_string}"

        except openai.APIConnectionError as e:
            logger.error("API connection error: %s", e)
            return f"There was a problem connecting to the OpenAI API. {self.logger_name_string}"

        except openai.APIError as e:
            logger.error("API error: %s", e)
            return f"An error occurred with the OpenAI API. {self.logger_name_string}"

        except openai.OpenAIError as e:
            logger.error("OpenAI error: %s", e)
            return f"An unspecified error occurred with the OpenAI API. {self.logger_name_string}"

    def num_tokens_from_string(self, string: str) -> int:
        """Returns the number of tokens in a text string."""
        model_encoding = tiktoken.encoding_for_model(self.model)
        encoding = tiktoken.get_encoding(model_encoding.name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def check_and_summarize_text(self) -> bool:
        """Reduces the text in the messages based on the reduction type.

        Args:
            summarization_type: The type of reduction to perform.

        Returns:
            None
        """
        if self._count_tokens(self.messages) < self.max_tokens:
            return False
        logger.info(
            "Summarizing agent (%s) messages with policy: %s",
            self.name,
            self.summarization_type,
        )
        if self.summarization_type == "naive":
            self._naive_summary()
        elif self.summarization_type == "naive-reversed":
            self._naive_reversed_summary()
        elif self.summarization_type == "truncation":
            self._truncation_summary()
        else:
            raise ValueError(
                f"Summariaztion type '{self.summarization_type}' is not supported."
            )
        return True

    def _count_tokens(self, messages):
        """Count the total number of tokens in a list of messages including additional fields."""
        return sum(
            self.num_tokens_from_string(json.dumps(msg, separators=(",", ":")))
            for msg in messages
        )

    def get_system_prompt_token_count(self) -> int:
        """Count the number of tokens in the system prompt."""
        for _, msg in enumerate(self.messages):
            if msg["role"] == "system":
                return self._count_tokens([msg])
        return 0

    def _naive_summary(self):
        """Take the first user message, truncate it, clear all other messages, and add the system message."""
        new_messages = [self.system_message]
        for _, msg in enumerate(self.messages):
            if msg["role"] == "user":
                leave_n_tokens = self.max_tokens - self.get_system_prompt_token_count()
                new_messages.append(
                    {
                        "role": "user",
                        "content": msg["content"][:leave_n_tokens],
                    }
                )
                break
        self.messages = new_messages

    def _naive_reversed_summary(self):
        """Take the last user message and truncate it."""
        self.messages.reverse()
        self._naive_summary()

    def _truncation_summary(self):
        """Truncate as many messages and their content as necessary to fit the model."""

        cum_sum = 0
        remaining_messages = []
        message_counts = [self._count_tokens([msg]) for msg in self.messages]
        for i, count in enumerate(message_counts):
            cum_sum += count
            remaining_messages.append(self.messages[i])
            if cum_sum > self.max_tokens:
                while cum_sum > self.max_tokens:
                    remaining_messages[i]["content"] = remaining_messages[i]["content"][
                        :-100
                    ]
                    cum_sum = self._count_tokens(remaining_messages)
                break
        self.messages = remaining_messages

    def clear_message_memory(self) -> None:
        """Clears the message memory."""
        logger.info("Clearing agent %smemory", self.logger_name_string)
        self.messages = [self.system_message]

    def get_memory_enabled_state(self) -> bool:
        """Gets the memory setting."""
        return self.memory

    @pyqtSlot(bool)
    def set_memory(self, memory: bool) -> None:
        """Sets the memory setting."""
        logger.info(
            "Setting agent %smemory to %s",
            self.logger_name_string,
            memory,
        )
        self.memory = memory
        self.clear_message_memory()
