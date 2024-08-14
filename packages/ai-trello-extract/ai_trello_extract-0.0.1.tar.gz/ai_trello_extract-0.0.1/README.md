# AI Trello Extract

Trello Extract is a Python project that uses the py-trello library and python-dotenv to authenticate with the Trello API and fetch details from Trello boards, lists, and cards. This project demonstrates how to securely manage API credentials and interact with Trello's API to retrieve project data for further processing.

## Features

- Authenticate with the Trello API using OAuth.
- Fetch details of all accessible Trello boards.
- Retrieve lists and cards from a specified Trello board.
- Securely manage API credentials using environment variables.

## Install through PyPI

```bash
pip install ai-trello-extract
```

For more details, visit the [PyPI project page](https://pypi.org/project/ai-trello-extract/).

## Setup

### 1: Register for Trello API Access

1. **Sign Up for a Trello Account**:

   - If you don't have a Trello account, sign up at [Trello](https://trello.com/).

2. **Get API Key and Token**:
   - Go to the [Trello Developer Portal](https://trello.com/app-key).
   - Copy your API Key.
   - Click on the "Token" link to generate a token. This token will be used for authentication in your API requests.

### 2. Clone the repository:

```bash
git clone https://github.com/DEV3L/ai-trello-extract
cd ai-trello-extract
```

Copy the env.local file to a new file named .env and replace `TRELLO_API_KEY` with your actual Trello API key:

```bash
cp env.local .env
```

### 3. Setup a virtual environment with dependencies and activate it:

```bash
brew install hatch
hatch env create
hatch shell
```

### 4. Extract the Trello data:

```bash
python trello_integration.py
```

#### Usage

The `trello_integration.py` script will:

1. Authenticate with the Trello API using the credentials provided in the `.env` file.
2. Fetch and print the details of all accessible Trello boards.
3. Fetch and print the lists and cards from the first Trello board in the list.

## Environment Variables

The following environment variables can be configured in the `.env` file:

- `TRELLO_API_KEY`: The Trello API key
- `TRELLO_API_TOKEN`: The Trello API token
- `TRELLO_BOARD_NAME`: The Trello board name

## Testing

### End to End Test

```bash
hatch run e2e
```

### Unit Tests

```bash
hatch run test
```

### Coverage Gutters:

```bash
Command + Shift + P => Coverage Gutters: Watch
```

## Example

## Example Program

```

```

### Example Output

```
# TODO

## Title

Title 1

## List Name

Task 1

## Labels

- bug
- urgent

## Due Date

2024-05-01 00:00:00

## Description

Description of task 1

## Comments

Comment 1
```

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Ensure all tests pass.
5. Submit a pull request with a detailed description of your changes.

## Code of Conduct

We expect all contributors to adhere to our Code of Conduct:

- Be respectful and considerate.
- Avoid discriminatory or offensive language.
- Report any unacceptable behavior to the project maintainers.

By participating in this project, you agree to abide by these guidelines.
