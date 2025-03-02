# oai

Chat with OpenAI LLMs in the terminal.

## Usage

### Initial Usage

1. [Install or update `uv`](https://github.com/astral-sh/uv?tab=readme-ov-file#installation).

2. Install Python:
   ```sh
   uv python install
   ```

3. Setup a virtual environment:

   1. Clone this repo and `cd` to it.

   2. Create a virtual environment:
      ```sh
      uv venv
      ```

   3. Activate the virtual environment.

4. Install requirements:
   ```sh
   uv pip install -r requirements.txt
   ```

5. Set environment variables:

   * Set `OPENAI_API_KEY` to your OpenAI API key.

   * Add the directory containing `oai` to your `PATH`.

6. Run `oai`.

### Subsequent Usage

1. Activate the virtual environment.

2. Run `oai`.

## Pricing

| Model       | Input | Cached Input | Output | Cost vs GPT-4o mini |
|-------------|-------|--------------|--------|---------------------|
| GPT-4o      | $2.50 | $1.25        | $10.00 | 16.67x              |
| GPT-4o mini | $0.15 | $0.075       | $0.60  | 1x                  |
| o1-mini     | $1.10 | $0.55        | $4.40  | 7.33x               |

Per 1M tokens. As of March 2, 2025.
