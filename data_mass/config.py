from functools import lru_cache

from pydantic import BaseSettings, validator
from pydantic.error_wrappers import ValidationError

from data_mass.classes.text import text

FILE_CONFIGURATION_ERROR = \
""" # noqa
Apparently your .env configuration file is not populated
with the essential information (vendorId, client_id and client_secret)
to run US region features. If you have any questions, please check our
user guide (doc/USER_GUIDE.md in our repository).
"""


class Settings(BaseSettings):
    vendor_id: str
    client_id: str
    client_secret: str

    @classmethod
    @validator("vendor_id")
    def validate_vendor(cls, vendor_id):
        """
        Validate `vendor_id` field.

        Parameters
        ----------
        vendor_id : str

        Raises
        ------
        ValueError
            Whenever the field `vendor_id` is empty.
        """
        if not vendor_id:
            raise ValueError("vendor_id should not be empty.")

    @classmethod
    @validator("client_id")
    def validate_client_id(cls, client_id):
        """
        Validate `client_id` field.

        Parameters
        ----------
        client_id : str

        Raises
        ------
        ValueError
            Whenever the field `client_id` is empty.
        """
        if not client_id:
            raise ValueError("client_id should not be empty.")

    @classmethod
    @validator("client_secret")
    def validate_client_secret(cls, client_secret):
        """
        Validate `client_secret` field.

        Parameters
        ----------
        client_secret : str

        Raises
        ------
        ValueError
            Whenever the field `client_secret` is empty.
        """
        if not client_secret:
            raise ValueError("client_secret should not be empty.")

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


@lru_cache()
def get_settings():
    """
    Get settings class for env management.

    Returns
    -------
    Settings
        The Settings object.

    Notes:
        The `lru_cache` decorator is used for \
        creating `Settings` only once.
    """
    try:
        settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

        return settings
    except ValidationError as e:
        print(e)

        print(f"{text.Red}{FILE_CONFIGURATION_ERROR}{text.Default}")
        exit()
