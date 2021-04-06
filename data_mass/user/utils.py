from base64 import b32encode
import logging

from pyotp import TOTP


def get_cookies(response):
    cookies = {}
    for c in response.cookies:
        cookies[c.name] = c.value
    return cookies


def merge_cookies(cookies1, cookies2):
    cookies = {}
    for key in cookies1.keys():
        cookies[key] = cookies1[key]
    for key in cookies2.keys():
        cookies[key] = cookies2[key]
    return cookies


def get_cookies_header(cookies):
    cookies_header = []
    for key in cookies.keys():
        cookies_header.append("{0}={1}".format(key, cookies[key]))
    return "; ".join(cookies_header)


def generate_otp(otp_secret, otp_interval, email):
    secret = otp_secret + email
    bytes_secret = bytes(secret, "utf8")
    base64_secret = b32encode(bytes_secret)
    totp = TOTP(base64_secret, interval=otp_interval).now()
    logging.debug("OTP generated: {0}".format(totp))
    return totp
