"""Kameleoon Configuration"""

from typing import Any, Dict, Optional


class Settings:
    """
    KameleoonConfigurationSettings is used for saving setting's parameters, e.g
    state of real time update for site code and etc
    """

    _CONSENT_TYPE_REQUIRED = "REQUIRED"

    # pylint: disable=R0903
    def __init__(self, configuration: Optional[Dict[str, Any]] = None):
        self.__real_time_update: bool = bool(configuration and configuration.get("realTimeUpdate"))
        self.__is_consent_required = (configuration is not None) and \
            (configuration.get("consentType") == self._CONSENT_TYPE_REQUIRED)

    @property
    def real_time_update(self) -> bool:
        """Returns streaming mode flag state"""
        return self.__real_time_update

    @property
    def is_consent_required(self) -> bool:
        """Returns consent required flag state"""
        return self.__is_consent_required
