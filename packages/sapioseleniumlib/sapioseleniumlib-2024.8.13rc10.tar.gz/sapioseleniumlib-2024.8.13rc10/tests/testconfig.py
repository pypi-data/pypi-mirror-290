import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

_host = os.getenv("SAPIO_SEL_HOST", "localhost")
_port = os.getenv("SAPIO_SEL_PORT", 443)
_guid = os.getenv("SAPIO_SEL_GUID", "")
headless = os.getenv("SAPIO_SEL_HEADLESS", "False").lower() == "true"
username = os.getenv("SAPIO_SEL_USERNAME", "user@example.com")
password = os.getenv("SAPIO_SEL_PASSWORD", "password")

HOMEPAGE_URL = "https://" + _host + ":" + str(_port) + "/veloxClient"
if _guid:
    HOMEPAGE_URL += "/VeloxClient.html?app=" + _guid
else:
    HOMEPAGE_URL += "/localauth"
