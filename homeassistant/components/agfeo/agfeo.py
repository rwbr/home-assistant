"""Module for the API of the AGFEO SmartHome server.

Copyright 2020 Ralf Weinbrecher <developer@ralfweinbrecher.de>

This code is released under the terms of the GPLv3 license. See the
LICENSE file for more details.
"""

import hashlib

import requests

API_TIMEOUT = 5


def get_devices(host: str, protocol: str, username: str, password: str):
    """Enumerate devices using the AGFEO SmartHome API."""

    API_URL = protocol + "://" + host + "/pbxapi/bas.php/v01/{api}"

    API_AUTH_REQ = API_URL.format(api="authreq")
    API_AUTH_RESP = API_URL.format(api="authresp")
    API_SESSION = API_URL.format(api="session")
    API_DEVICES = API_URL.format(api="objects")
    # API_DEVICES_INDEX = API_URL.format(api="objects/{index}")

    def _authreq(username):
        """Request an authentication challenge from the server."""
        auth_data = {"loginname": username}
        response = requests.post(API_AUTH_REQ, json=auth_data, timeout=API_TIMEOUT)
        try:
            return response.json()["challenge"]
        except KeyError:
            raise (AgfeoException("API authentication failed"))

    def _authresp(username, password, challenge):
        """Send the calculated authentication response back to the server."""
        auth_response = (
            challenge + "-" + hashlib.md5(challenge + "-" + password).hexdigest
        )
        payload = {"loginname": username, "response": auth_response}
        response = requests.get(API_AUTH_RESP, json=payload, timeout=API_TIMEOUT)
        try:
            return response.json()["sid"]
        except KeyError:
            raise (AgfeoException("API authentication failed"))

    def _validate_session(session_id):
        """Validate the current session with the AGFEO SmartHome server."""
        payload = {"sid": session_id}
        response = requests.get(API_SESSION, json=payload, timeout=API_TIMEOUT)
        result = response.json()["sid"]
        return result == session_id

    def _get_devices(session_id):
        """Get the list of all devices."""
        response = requests.get(API_DEVICES, timeout=API_TIMEOUT,)
        return response.json()["objects"]


class AgfeoException(Exception):
    """An error related to the AGFEO SmartHome API occcured."""

    pass


class Agfeo:
    """An Agfeo SmartHome Object."""
