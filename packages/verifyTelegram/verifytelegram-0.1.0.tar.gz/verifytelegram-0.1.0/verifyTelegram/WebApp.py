import hmac
from hashlib import sha256
from urllib.parse import unquote
import json
import urllib.parse
from dataclasses import dataclass

@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    username: str
    language_code: str
    is_premium:bool
    allows_write_to_pm: bool

# The Data class handles the validation and extraction of user data
class Data:
    '''
    Imports:
        * - hmac and sha256 are used to create cryptographic hashes for data validation.
        * - unquote and urllib.parse are used to decode and parse URL-encoded strings.
        * - json is used to parse JSON data into Python objects.
        * - dataclasses is used to create the User class for structured data.
    
    User Class:
        * - Represents user information, including attributes like id, first_name, last_name, etc.
    
    Data Class:
        * - Manages the validation of input data and extraction of user information.
        * - Generates a secret_key using the bot token, which is then used to validate data.
        * - The is_valid_data method checks if the provided data is valid by comparing hashes.
        * - The GetData method is a static method that extracts user data from a URL-encoded string and converts it into a User object.

    Example Variables:
        * - BOT_TOKEN, INIT_DATA_HASH, and DATA_CHECK_STRING are sample values provided to test the functionality of the Data class.
    '''
    def __init__(self,BOT_TOKEN:str) -> None:
        '''
            BOT_TOKEN = "5455787892:AAEalcMURBUjeLvTDuy4NHoQ5ZnryQ4zV54"
        '''
        # Generate a secret key using a fixed key ('WebAppData') and the bot token
        self.secret_key =  hmac.new(b'WebAppData', bytes(BOT_TOKEN, encoding='utf-8'), sha256).digest()

    def is_valid_data(self,INIT_DATA_HASH:str,DATA_CHECK_STRING:str) -> bool:
        '''
            INIT_DATA_HASH = "90677c2f2e1326cdb4d5cd781905c375f5397b8f6dbee501487385aa3faf3e0e"
            DATA_CHECK_STRING = "auth_date=1721578504&chat_instance=-5432073769796079823&chat_type=private&user=%7B%22id%22%3A6195030789%2C%22first_name%22%3A%22._.%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22ksdaskdnc2w%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D"
        '''
        # Unquote the data check string and prepare it for hashing
        data_check_string_unquote = unquote(DATA_CHECK_STRING.replace('&', '\n'))
        # Generate a hash from the unquoted data check string using the secret key
        hash = hmac.new(self.secret_key, bytes(data_check_string_unquote, encoding='utf-8'), sha256).hexdigest()
        # Check if the generated hash matches the initial data hash
        return hash == INIT_DATA_HASH

    # Static method to extract user data from the data check string
    @staticmethod
    def GetData(DATA_CHECK_STRING):
        # Internal function to parse the input string into different parameters
        def parse_input_string(input_str: str) -> tuple:
            pairs = input_str.split('&')
            auth_date = None
            chat_instance = None
            chat_type = None
            user_json = None
            # Iterate through key-value pairs and extract relevant information
            for pair in pairs:
                key, value = pair.split('=')
                if key == 'auth_date':
                    auth_date = int(value)
                elif key == 'chat_instance':
                    chat_instance = value
                elif key == 'chat_type':
                    chat_type = value
                elif key == 'user':
                    user_json = urllib.parse.unquote(value)
            return auth_date, chat_instance, chat_type, user_json

        # Internal function to create a User object from JSON data
        def create_user_from_json(user_json: str) -> User:
            user_data = json.loads(user_json)
            return User(
                id=user_data.get('id',None),
                first_name=user_data.get('first_name',None),
                last_name=user_data.get('last_name',None),
                username=user_data.get('username',None),
                language_code=user_data.get('language_code',None),
                is_premium=user_data.get('is_premium',False),
                allows_write_to_pm=user_data.get('allows_write_to_pm',False)
            )
        # Extract parameters from the input string and create a User object
        auth_date, chat_instance, chat_type, user_json = parse_input_string(DATA_CHECK_STRING)
        return create_user_from_json(user_json)
