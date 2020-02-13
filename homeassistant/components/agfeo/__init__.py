"""Support for Agfeo SmartHome interface."""
import logging

import voluptuous as vol

from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "agfeo"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_HOST): cv.string,
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


def setup(hass, config):
    """Set up for the Asterisk Voicemail box."""
    conf = config.get(DOMAIN)

    host = conf.get(CONF_HOST)
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)

    hass.data[DOMAIN] = AgfeoData(hass, host, username, password, config)

    return True


class AgfeoData:
    """Store Agfeo SmartHome data."""

    def __init__(self, hass, host, username, password, config):
        """Init the Agfeo SmartHome data object."""

        self.hass = hass
        self.config = config
