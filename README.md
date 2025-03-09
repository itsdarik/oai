# chai

Chat with AI in the terminal.

`chai` supports the following providers:
- Anthropic
- Gemini
- Mistral
- OpenAI
- xAI

## Installation

```sh
pip install chai-cli
```

## Usage

```sh
chai -h
```

Set your API key(s):

```sh
export ANTHROPIC_API_KEY='your-anthropic-api-key'
export GEMINI_API_KEY='your-gemini-api-key'
export MISTRAL_API_KEY='your-mistral-api-key'
export OPENAI_API_KEY='your-openai-api-key'
export XAI_API_KEY='your-xai-api-key'
```

## Development

1. [Install or update `uv`](https://github.com/astral-sh/uv?tab=readme-ov-file#installation).

2. Install Python:
   ```sh
   uv python install
   ```

3. Run `chai.py`:
   ```sh
   uv run chai.py -h
   ```
