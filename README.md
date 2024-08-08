# Project Overview

This project is designed to synchronize the hours recorded in Timing with Paprika. Timing is a time tracking application, while Paprika is a project management and accounting software. The synchronization process ensures that the hours tracked in Timing are accurately reflected in Paprika, facilitating better project management and accounting.

# License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Key Features

- **Timing Integration**: Connects to the Timing API to fetch recorded hours.
- **Paprika Integration**: Sends the fetched hours to Paprika for synchronization.
- **Environment Configuration**: Utilizes environment variables for secure and flexible configuration.

## Environment Variables

The project uses the following environment variables, which should be set in a `.env` file:

- `TIMING_TOKEN`: Authentication token for Timing API.
- `TIMING_URL`: URL for the Timing API.
- `TELEGRAM_CHAT_ID`: Chat ID for Telegram notifications.
- `TELEGRAM_TOKEN`: Token for Telegram bot.
- `PAPRIKA_URL`: URL for the Paprika API.
- `PAPRIKA_USERNAME`: Username for Paprika.
- `PAPRIKA_PASSWORD`: Password for Paprika.
- `PAPRIKA_DB`: Database name for Paprika.
- `SENTRY_DSN`: DSN for Sentry error tracking.
- `REDIS_URL`: URL for Redis instance.

## Getting Started

1. Clone the repository.
2. Create a `.env` file based on the `.env.example` file and fill in the required values.
3. Install the necessary dependencies.
4. Run the synchronization script.

## Dependencies

- Python
- Requests library for API calls
- Redis for caching
- Sentry for error tracking

## Usage

To start the synchronization process, run the main script:

```sh
python main.py