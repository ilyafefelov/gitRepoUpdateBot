# GitHub Repository Update Notifier

## Overview
This project is a GitHub Repository Update Notifier that uses FastAPI to monitor GitHub repositories and sends notifications via Telegram when new commits are made to the main branch. It's designed to help developers and teams stay updated with changes without needing to constantly check GitHub.

## Features
- Monitor multiple GitHub repositories.
- Receive Telegram notifications for new commits.
- Easy subscription management through a REST API.

## Technology Stack
- **FastAPI**: Asynchronous web framework for building APIs.
- **HTTPX**: HTTP client for making asynchronous requests.
- **APScheduler**: Task scheduler for Python applications.
- **python-dotenv**: Reads key-value pairs from a `.env` file and can set them as environment variables.
- **Telegram Bot API**: Used for sending notifications.

## Requirements
- Python 3.7+
- FastAPI
- httpx
- APScheduler
- python-dotenv
- A Telegram bot token and chat IDs

## Setup and Installation

1. **Clone the repository:**
git clone https://github.com/your-username/your-repository.git
```cd your-repository```

2. **Install dependencies:**
```poetry install```

3. **Set up the environment variables:**
Create a `.env` file in the root directory and fill in your Telegram bot token and any other necessary configuration.
```TELEGRAM_TOKEN=your_telegram_bot_token_here```

4. **Start the FastAPI server:**
```poetry run uvicorn main:app --reload```

## Usage

### Subscribing to Repository Updates

Send a POST request to `/subscribe/` with the following JSON payload:

```json
{
"repo": "username/repository",
"chat_id": "your_telegram_chat_id"
}
```

This will subscribe you to updates for the specified repository, and you'll receive notifications via Telegram when new commits are pushed to the main branch.

Checking Subscriptions
The current subscriptions are stored in-memory and can be viewed by inspecting the server logs or by adding an endpoint to list subscriptions.

Contributing
Contributions are welcome! Please fork the repository and submit pull requests with any enhancements.

License
MIT License

Contact
For any further queries, please reach out via GitHub or Telegram.
