# Economics Chatbot

A conversational AI chatbot focused on economics topics, powered by a fine-tuned Phi-2 model from Microsoft.

## Features

- Interactive web interface for chatting with the AI
- Local LLM inference using a fine-tuned Phi-2 model
- Conversation memory for context-aware responses
- FastAPI backend for efficient API handling

## Prerequisites

- Python 3.11 or higher
- Sufficient disk space and RAM for running transformer models

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Fine-tuning (Optional)

If you want to fine-tune the model with your own data:

1. Add your training data to `training_data.jsonl` (one JSON object per line, with a `text` field).
2. Run the fine-tuning script:
   ```bash
   python fine_tune.py
   ```
3. The fine-tuned model will be saved in the `fine_tuned_model` directory.

## Usage

1. Start the FastAPI server:
   ```bash
   python main.py
   ```

2. Open your web browser and navigate to `http://localhost:8000` to interact with the chatbot.

## Configuration

The chatbot uses the following configuration settings (defined in `config.py`):

- `HOST`: The host address for the FastAPI server (default: "0.0.0.0")
- `PORT`: The port for the FastAPI server (default: 8000)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 