import json
import re
import uuid
import gzip
import zlib
from typing import Any, Dict, Generator, Union

import requests

from webscout.AIutel import Optimizers
from webscout.AIutel import Conversation
from webscout.AIutel import AwesomePrompts
from webscout.AIbase import Provider
from webscout import exceptions

class LiaoBots(Provider):
    """
    A class to interact with the LiaoBots API.
    """

    # List of available models
    AVAILABLE_MODELS = [
        "gpt-4o-mini",
        "gpt-4o-free",
        "gpt-4o-mini-free",
        "gpt-4-turbo-2024-04-09",
        "gpt-4o",
        "gpt-4-0613",
        "claude-3-5-sonnet-20240620",
        "gemini-1.5-pro-latest",
        "gemini-1.5-flash-latest"
    ]

    def __init__(
        self,
        auth_code: str = "G3USRn7M5zsXn",
        cookie: str = "gkp2=pevIjZCYj8wMcrWPEAq6",
        is_conversation: bool = True,
        max_tokens: int = 600,
        timeout: int = 30,
        intro: str = None,
        filepath: str = None,
        update_file: bool = True,
        proxies: dict = {},
        history_offset: int = 10250,
        act: str = None,
        model: str = "claude-3-5-sonnet-20240620",
        system_prompt: str = "You are a helpful assistant."
    ) -> None:
        """
        Initializes the LiaoBots API with given parameters.

        Args:
            auth_code (str): The auth code for authentication.
            cookie (str): The cookie for authentication.
            is_conversation (bool, optional): Flag for chatting conversationally. Defaults to True.
            max_tokens (int, optional): Maximum number of tokens to be generated upon completion. Defaults to 600.
            timeout (int, optional): Http request timeout. Defaults to 30.
            intro (str, optional): Conversation introductory prompt. Defaults to None.
            filepath (str, optional): Path to file containing conversation history. Defaults to None.
            update_file (bool, optional): Add new prompts and responses to the file. Defaults to True.
            proxies (dict, optional): Http request proxies. Defaults to {}.
            history_offset (int, optional): Limit conversation history to this number of last texts. Defaults to 10250.
            act (str|int, optional): Awesome prompt key or index. (Used as intro). Defaults to None.
            model (str, optional): AI model to use for text generation. Defaults to "claude-3-5-sonnet-20240620".
            system_prompt (str, optional): System prompt for LiaoBots. Defaults to "You are a helpful assistant.".
        """

        # Check if the chosen model is available
        if model not in self.AVAILABLE_MODELS:
            raise ValueError(f"Invalid model: {model}. Choose from: {self.AVAILABLE_MODELS}")

        self.auth_code = auth_code
        self.cookie = cookie
        self.api_endpoint = "https://liaobots.work/api/chat"
        self.model = model
        self.system_prompt = system_prompt
        self.session = requests.Session()
        self.is_conversation = is_conversation
        self.max_tokens_to_sample = max_tokens
        self.stream_chunk_size = 64
        self.timeout = timeout
        self.last_response = {}
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
            "content-type": "application/json",
            "cookie": self.cookie,
            "dnt": "1",
            "origin": "https://liaobots.work",
            "priority": "u=1, i",
            "referer": "https://liaobots.work/en",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
            "x-Auth-Code": self.auth_code,
        }
        self.__available_optimizers = (
            method
            for method in dir(Optimizers)
            if callable(getattr(Optimizers, method)) and not method.startswith("__")
        )
        self.session.headers.update(self.headers)
        Conversation.intro = (
            AwesomePrompts().get_act(
                act, raise_not_found=True, default=None, case_insensitive=True
            )
            if act
            else intro or Conversation.intro
        )
        self.conversation = Conversation(
            is_conversation, self.max_tokens_to_sample, filepath, update_file
        )
        self.conversation.history_offset = history_offset
        self.session.proxies = proxies

    def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> Dict[str, Any]:
        """
        Sends a prompt to the LiaoBots API and returns the response.

        Args:
            prompt: The text prompt to generate text from.
            stream (bool, optional): Whether to stream the response. Defaults to False.
            raw (bool, optional): Whether to return the raw response. Defaults to False.
            optimizer (str, optional): The name of the optimizer to use. Defaults to None.
            conversationally (bool, optional): Whether to chat conversationally. Defaults to False.

        Returns:
            The response from the API.
        """
        conversation_prompt = self.conversation.gen_complete_prompt(prompt)
        if optimizer:
            if optimizer in self.__available_optimizers:
                conversation_prompt = getattr(Optimizers, optimizer)(
                    conversation_prompt if conversationally else prompt
                )
            else:
                raise Exception(
                    f"Optimizer is not one of {self.__available_optimizers}"
                )

        payload: Dict[str, any] = {
            "conversationId": str(uuid.uuid4()),
            "model": {
                "id": self.model
            },
            "messages": [
                {
                    "role": "user",
                    "content": conversation_prompt
                }
            ],
            "key": "",
            "prompt": self.system_prompt
        }

        def for_stream():
            response = self.session.post(
                self.api_endpoint, json=payload, headers=self.headers, stream=True, timeout=self.timeout
            )

            if not response.ok:
                raise exceptions.FailedToGenerateResponseError(
                    f"Failed to generate response - ({response.status_code}, {response.reason})"
                )

            streaming_response = ""
            content_encoding = response.headers.get('Content-Encoding')
            # Stream the response
            for chunk in response.iter_content():
                if chunk:
                    try:
                        # Decompress the chunk if necessary
                        if content_encoding == 'gzip':
                            chunk = gzip.decompress(chunk)
                        elif content_encoding == 'deflate':
                            chunk = zlib.decompress(chunk)
                        
                        # Decode the chunk
                        decoded_chunk = chunk.decode('utf-8')
                        streaming_response += decoded_chunk
                    except UnicodeDecodeError:
                        # Handle non-textual data
                        pass
                else:
                    pass
            self.last_response.update(dict(text=streaming_response))
            self.conversation.update_chat_history(
                prompt, self.get_message(self.last_response)
            )

            if stream:
                yield from []  # Yield nothing when streaming, focus on side effects
            else:
                return []  # Return empty list for non-streaming case

        def for_non_stream():
            for _ in for_stream():
                pass
            return self.last_response

        return for_stream() if stream else for_non_stream()

    def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> str:
        """Generate response `str`
        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
        Returns:
            str: Response generated
        """

        def for_stream():
            for response in self.ask(
                prompt, True, optimizer=optimizer, conversationally=conversationally
            ):
                yield self.get_message(response)

        def for_non_stream():
            return self.get_message(
                self.ask(
                    prompt,
                    False,
                    optimizer=optimizer,
                    conversationally=conversationally,
                )
            )

        return for_stream() if stream else for_non_stream()

    def get_message(self, response: dict) -> str:
        """Retrieves message only from response

        Args:
            response (dict): Response generated by `self.ask`

        Returns:
            str: Message extracted
        """
        assert isinstance(response, dict), "Response should be of dict data-type only"
        return response["text"]

if __name__ == '__main__':
    from rich import print
    liaobots = LiaoBots()
    response = liaobots.chat("tell me about india")
    for chunk in response:
        print(chunk, end="", flush=True)