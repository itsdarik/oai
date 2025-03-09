#!/usr/bin/env python3
#
# Copyright 2025 Darik Harter
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
# file except in compliance with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied.  See the License for the specific language
# governing permissions and limitations under the License.

from .providers.chat import Chat
from .providers.provider import get_providers

import argparse
import json
import readline
from dataclasses import dataclass
from pathlib import Path
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

SAVE_DIR = Path.home() / ".chai"

CLI_PROMPT = ">>> "
MULTI_LINE_INPUT = '"""'


@dataclass(frozen=True)
class Settings:
    pretty: bool


def send(chat: Chat, user_input: str, settings: Settings) -> str:
    response = chat.send(user_input)
    if settings.pretty:
        full_response = ""
        with Live(console=Console(), refresh_per_second=8) as live:
            for chunk in response:
                if chunk:
                    full_response += chunk
                    live.update(Markdown(full_response))
    else:
        for chunk in response:
            if chunk:
                print(chunk)
        print()


def get_user_input() -> str:
    user_input = input(CLI_PROMPT).strip()

    # Handle multi-line input.
    if user_input.startswith(MULTI_LINE_INPUT):
        lines = [user_input[len(MULTI_LINE_INPUT) :]]
        while True:
            line = input().rstrip()
            if line.endswith(MULTI_LINE_INPUT):
                lines.append(line[: -len(MULTI_LINE_INPUT)])
                break
            lines.append(line)
        user_input = "\n".join(lines).strip()

    return user_input.strip()


def print_help() -> None:
    print(
        "Available Commands:\n"
        "  /clear            Clear session context\n"
        "  /save <file>      Save conversation to a file\n"
        "  /load <file>      Load conversation from a file\n"
        "  /bye              Exit\n"
        "  /?, /help         Print available commands\n"
        "\n"
        f"Use {MULTI_LINE_INPUT} to begin a multi-line message."
    )


def save_conversation(user_input: str, chat: Chat) -> None:
    parts = user_input.split()
    if len(parts) != 2:
        print("Usage:\n  /save <file>")
        return

    if not chat.history:
        print("No conversation to save.")
        return

    filename = parts[1]
    if "/" in filename or "\\" in filename:
        print("Invalid filename.")
        return
    if not filename.endswith(".json"):
        filename += ".json"

    path = SAVE_DIR / filename
    if (
        path.exists()
        and input(f"File '{path}' already exists. Overwrite? (y/n) ").strip().lower()
        != "y"
    ):
        return

    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as save_file:
        conversation = [message.dict() for message in chat.history]
        json.dump(conversation, save_file, indent=4)
    print(f"\nSaved conversation to '{path}'.")


def load_conversation(user_input: str, chat: Chat, settings: Settings) -> None:
    parts = user_input.split()
    if len(parts) != 2:
        print("Usage:\n  /load <file>")
        return

    filename = parts[1]
    if not filename.endswith(".json"):
        filename += ".json"

    path = SAVE_DIR / filename
    if not path.exists():
        print(f"File '{path}' does not exist.")
        return

    if (
        chat.history
        and input("Overwrite current conversation? (y/n) ").strip().lower() != "y"
    ):
        return

    with open(path) as save_file:
        saved_conversation = json.load(save_file)

    chat.clear()
    chat.history.extend(saved_conversation)
    print_conversation(chat, settings)


def print_conversation(chat: Chat, settings: Settings) -> None:
    if not chat.history:
        return

    for message in chat.history:
        # TODO: abstract "user" in each specific chat class.
        if message.role == "user":
            print(f"\n{CLI_PROMPT}{message.content}")
        else:
            if settings.pretty:
                Console().print(Markdown(message.content))
            else:
                print(message.content)


def handle_command(user_input: str, chat: Chat, settings: Settings) -> None:
    command = user_input.split()[0]

    if command == "/bye":
        raise EOFError
    elif command == "/clear":
        chat.clear()
        print("Cleared conversation.")
    elif command == "/load":
        load_conversation(user_input, chat, settings)
    elif command == "/save":
        save_conversation(user_input, chat)
    elif command == "/?" or command == "/help":
        print_help()
    else:
        print(f"Unknown command: '{command}'. Type /? for help.")

    print()


def input_loop(chat: Chat, settings: Settings) -> None:
    readline.parse_and_bind("set editing-mode emacs")

    while True:
        try:
            user_input = get_user_input().strip()
            if not user_input:
                continue

            if user_input.startswith("/"):
                handle_command(user_input, chat, settings)
                continue

        except EOFError:
            break

        try:
            send(chat, user_input, settings)
        except Exception as e:
            print(f"Error: {e}")

        print()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Chat with OpenAI LLMs in the terminal",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--model", default="gpt-4o-mini", help="the OpenAI model to use"
    )
    parser.add_argument("--pretty", action="store_true", help="pretty print responses")
    return parser.parse_args()


@dataclass(frozen=True)
class Args:
    model: str
    pretty: bool


def get_args() -> Args:
    args = parse_arguments()
    return Args(model=args.model, pretty=args.pretty)


def main() -> None:
    args = get_args()
    # TODO: fix this logic.
    providers = get_providers()
    chat = providers[0].create_chat(args.model)
    settings = Settings(pretty=args.pretty)
    input_loop(chat, settings)


if __name__ == "__main__":
    main()
