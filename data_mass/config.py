from functools import lru_cache
import re
import pandas
from pydantic import BaseSettings, validator
from pydantic.error_wrappers import ValidationError

from pandas import Series
from data_mass.classes.text import text

FILE_CONFIGURATION_ERROR = \
""" # noqa
Apparently your .env configuration file is not populated
with the essential information (vendorId, client_id and client_secret)
to run US region features. If you have any questions, please check our
user guide (doc/USER_GUIDE.md in our repository).
"""
EMAIL_CONFIGURATION_ERROR = \
"""

Please verify your email address on .env

Any doubts check the README.MD or ctrl/cmd + click the following link:

https://ab-inbev.atlassian.net/wiki/spaces/PKB/pages/2874278739/Add+email+to+environment

"""


class Settings(BaseSettings):
    vendor_id: str
    client_id: str
    client_secret: str


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

        return vendor_id

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

        return client_id

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

        return client_secret
        
    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"
        case_sensitive: bool = False


class EmailSetting(BaseSettings):
    user_email: str        

    @validator("user_email")
    def validate_user_email(cls, user_email):
        """
        Validate `USER_EMAIL` field.

        Parameters
        ----------
        USER_EMAIL : str

        Raises
        ------
        ValueError
            Whenever the field `USER_EMAIL` is empty.
        """
        if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', user_email):
            get_dot = pandas.Series(user_email)
            get_dot = int(get_dot.str.count('\.'))
            if get_dot == 2:
                return True
            else:
                raise ValueError("Your email is incorrect.")

        else:
            raise ValueError("Your email is incorrect.")


    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"
        case_sensitive: bool = False


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


@lru_cache()
def get_email():
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
        settings = EmailSetting(_env_file=".env", _env_file_encoding="utf-8")
        return settings.user_email
    except ValidationError as e:
        print(e)

        print(f"{text.Red}{EMAIL_CONFIGURATION_ERROR}{text.Default}")
        exit()