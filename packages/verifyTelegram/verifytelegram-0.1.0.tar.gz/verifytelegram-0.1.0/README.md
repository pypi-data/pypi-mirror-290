# Data Validation and User Extraction Module

This Python module is designed to handle the validation and extraction of user data from a URL-encoded string. It uses HMAC and SHA-256 hashing to ensure data integrity and security. The module provides a simple way to validate input data and parse it into a structured `User` object.

## Requirements

This module requires Python 3.6+ and uses the following standard libraries:

- `hmac`
- `hashlib`
- `urllib`
- `json`
- `dataclasses`

## Installation

No external libraries are required for this module. Simply include the code in your Python project.

## Usage

### User Class

The `User` class is a data class that holds the following information about a user:

- `id`: The user's unique identifier (integer).
- `first_name`: The user's first name (string).
- `last_name`: The user's last name (string).
- `username`: The user's username (string).
- `language_code`: The language code of the user (string).
- `is_premium`: A boolean indicating if the user has a premium account.
- `allows_write_to_pm`: A boolean indicating if the user allows writing to private messages.

### Data Class

The `Data` class is responsible for validating input data and extracting user information from a URL-encoded string.

#### Initialization

To create an instance of the `Data` class, you need to provide a bot token:

```python
data_instance = Data(BOT_TOKEN="your_bot_token_here")
```

#### is_valid_data Method

This method checks if the provided data is valid by comparing the generated hash with the initial data hash.

```python
is_valid = data_instance.is_valid_data(INIT_DATA_HASH="your_init_data_hash", DATA_CHECK_STRING="your_data_check_string")
```

#### GetData Method

This static method extracts user data from the data check string and returns a `User` object.

```python
user = Data.GetData(DATA_CHECK_STRING="your_data_check_string")
```

### Example

Here's an example of how to use the module:

```python
BOT_TOKEN = "1231212:sdsadasdsadasd231ec"
INIT_DATA_HASH = "90677c2f2e1326cdb4d5cd781905c375f5397b8f6dbee501487385aa3faf3e0e"
DATA_CHECK_STRING = "auth_date=1721578504&chat_instance=-5432073769796079823&chat_type=private&user=%7B%22id%22%3A6195030789%2C%22first_name%22%3A%22._.%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22ksdaskdnc2w%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D"

data_instance = Data(BOT_TOKEN)
if data_instance.is_valid_data(INIT_DATA_HASH, DATA_CHECK_STRING):
    user = Data.GetData(DATA_CHECK_STRING)
    print(f"User {user.first_name} ({user.username}) is authenticated.")
else:
    print("Invalid data provided.")
```

## License

This module is licensed under the MIT License. Feel free to use and modify it as needed.

