import os

from dotenv import load_dotenv

from fastapi_auth_toolkit.app import BaseFastapiAuthToolkitConfig
from fastapi_auth_toolkit.app.exception.response import NotFoundException

env_file = ".env"

# Check if the .env file exists
if not os.path.exists(env_file):
    raise NotFoundException(f"Could not find .env at {env_file}")

# Load environment variables from the .env file
load_dotenv(env_file)

FastapiAuthToolkitConfig = BaseFastapiAuthToolkitConfig
