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
from .providers.factory import get_providers
from .providers.provider import Provider

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

from dataclasses import dataclass

import argparse
import readline

CLI_PROMPT = ">>> "
MULTI_LINE_INPUT = '"""'


@dataclass(frozen=True)
class Args:
    command: str
    plain: bool


@dataclass(frozen=True)
class ChatArgs(Args):
    model: str


def send(chat: Chat, user_input: str, args: ChatArgs) -> None:
    response = chat.send(user_input)
    if args.plain:
        for chunk in response:
            if chunk:
                print(chunk, end="", flush=True)
        print()
    else:
        full_response = ""
        with Live(console=Console()) as live:
            for chunk in response:
                if chunk:
                    full_response += chunk
                    live.update(Markdown(full_response))


def save_chat(user_input: str, chat: Chat) -> None:
    from .persistence import get_save_file_path, save_chat, save_file_exists

    parts = user_input.split()
    if len(parts) != 2:
        print("Usage:\n  /save <file>")
        return

    if not chat.history:
        print("No chat history to save.")
        return

    filename = parts[1]
    if "/" in filename or "\\" in filename:
        print("Invalid filename.")
        return

    path = get_save_file_path(filename)
    if (
        save_file_exists(filename)
        and input(f"File '{path}' already exists. Overwrite? (y/n) ").strip().lower()
        != "y"
    ):
        return

    try:
        path = save_chat(chat, filename)
        print(f"\nSaved chat to '{path}'.")
    except Exception as e:
        print(f"Error saving chat: {e}")


def load_chat(user_input: str, chat: Chat, args: ChatArgs) -> None:
    from .persistence import load_chat

    parts = user_input.split()
    if len(parts) != 2:
        print("Usage:\n  /load <file>")
        return

    filename = parts[1]

    if (
        chat.history
        and input("Overwrite current conversation? (y/n) ").strip().lower() != "y"
    ):
        return

    try:
        load_chat(filename, chat)
        print_conversation(chat, args)
    except Exception as e:
        print(f"Error loading chat: {e}")


def print_conversation(chat: Chat, args: ChatArgs) -> None:
    if not chat.history:
        return

    for message in chat.history:
        if message.from_user():
            print(f"\n{CLI_PROMPT}{message.content}")
        else:
            if args.plain:
                print(message.content)
            else:
                Console().print(Markdown(message.content))


def print_help() -> None:
    print(
        "Available Commands:\n"
        "  /clear            Clear chat history\n"
        "  /save <file>      Save chat to a file\n"
        "  /load <file>      Load chat from a file\n"
        "  /bye              Exit\n"
        "  /?, /help         Print available commands\n"
        "\n"
        f"Use {MULTI_LINE_INPUT} to begin a multi-line message."
    )


def handle_command(user_input: str, chat: Chat, args: ChatArgs) -> None:
    command = user_input.split()[0]

    if command == "/bye":
        raise EOFError
    elif command == "/clear":
        chat.clear()
        print("Cleared chat history.")
    elif command == "/load":
        load_chat(user_input, chat, args)
    elif command == "/save":
        save_chat(user_input, chat)
    elif command == "/?" or command == "/help":
        print_help()
    else:
        print(f"Unknown command: '{command}'. Type /? for help.")

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


def input_loop(chat: Chat, args: ChatArgs) -> None:
    # Enable better line editing.
    readline.parse_and_bind("set editing-mode emacs")

    while True:
        try:
            user_input = get_user_input().strip()
            if not user_input:
                continue

            if user_input.startswith("/"):
                handle_command(user_input, chat, args)
                continue

        except EOFError:
            break

        try:
            send(chat, user_input, args)
        except Exception as e:
            print(f"Error: {e}")

        print()


def get_provider(model: str) -> Provider:
    providers = get_providers()
    if not providers:
        raise RuntimeError("No providers available")

    for provider in providers:
        if model in provider.models:
            return provider

    raise ValueError(f"Invalid model: {model}")


# chat command
def chat(args: ChatArgs) -> None:
    input_loop(get_provider(args.model).create_chat(args.model), args)


def print_markdown(markdown: str, args: Args) -> None:
    if args.plain:
        print(markdown)
    else:
        Console().print(Markdown(markdown))


def get_providers_models_list() -> str:
    providers = get_providers()
    if not providers:
        raise RuntimeError("No providers available")

    markdown = "# Available Models"

    for provider in sorted(providers, key=lambda p: p.name):
        markdown += f"\n\n## {provider.name}"

        if provider.api_key is None:
            markdown += (
                f"\n\nAPI key environment variable ({provider.api_key_name}) not set."
            )
            continue

        models = provider.models
        if not models:
            markdown += "\n\nNo models available."
            continue
        for model in sorted(models):
            markdown += f"\n* {model}"

    return markdown


# list command
def list_models(args: Args) -> None:
    print_markdown(get_providers_models_list(), args)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Chat with AI in the terminal",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--plain", action="store_true", help="plain text output")

    subparsers = parser.add_subparsers(dest="command", help="commands")

    chat_parser = subparsers.add_parser("chat", help="chat with a model")
    chat_parser.add_argument("model", help="the model to use")

    subparsers.add_parser("list", help="list available models")

    return parser.parse_args()


def get_args() -> ChatArgs | Args:
    args = parse_arguments()
    if args.command == "chat":
        return ChatArgs(args.command, args.plain, args.model)
    if args.command == "list":
        return Args(args.command, args.plain)
    raise ValueError(f"Unknown command: {args.command}")


def main() -> None:
    args = get_args()
    if isinstance(args, ChatArgs):
        chat(args)
    elif args.command == "list":
        list_models(args)
    else:
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
