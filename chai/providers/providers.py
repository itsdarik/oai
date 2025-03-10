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

from .anthropic import AnthropicProvider
from .mistral import MistralProvider
from .openai import OpenAIProvider
from .provider import Provider
from .xai import XAIProvider


def get_providers() -> list[Provider]:
    """Return a list of available providers."""
    return [
        AnthropicProvider(),
        MistralProvider(),
        OpenAIProvider(),
        XAIProvider(),
    ]
