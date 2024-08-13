# coding: utf-8

"""
    Fingerprint Pro Server API

    Fingerprint Pro Server API allows you to get information about visitors and about individual events in a server environment. It can be used for data exports, decision-making, and data analysis scenarios. Server API is intended for server-side usage, it's not intended to be used from the client side, whether it's a browser or a mobile device.   # noqa: E501

    OpenAPI spec version: 3
    Contact: support@fingerprint.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import re  # noqa: F401
from typing import Dict, List, Optional  # noqa: F401
from fingerprint_pro_server_api_sdk.base_model import BaseModel


class ClonedAppResult(BaseModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'result': 'bool'
    }

    attribute_map = {
        'result': 'result'
    }

    def __init__(self, result=None):  # noqa: E501
        """ClonedAppResult - a model defined in Swagger"""  # noqa: E501
        self._result = None
        self.discriminator = None
        self.result = result

    @property
    def result(self) -> bool:
        """Gets the result of this ClonedAppResult.  # noqa: E501

        Android specific cloned application detection. There are 2 values: • `true` - Presence of app cloners work detected (e.g. fully cloned application found or launch of it inside of a not main working profile detected). • `false` - No signs of cloned application detected or the client is not Android.   # noqa: E501

        :return: The result of this ClonedAppResult.  # noqa: E501
        """
        return self._result

    @result.setter
    def result(self, result: bool):
        """Sets the result of this ClonedAppResult.

        Android specific cloned application detection. There are 2 values: • `true` - Presence of app cloners work detected (e.g. fully cloned application found or launch of it inside of a not main working profile detected). • `false` - No signs of cloned application detected or the client is not Android.   # noqa: E501

        :param result: The result of this ClonedAppResult.  # noqa: E501
        """
        if result is None:
            raise ValueError("Invalid value for `result`, must not be `None`")  # noqa: E501

        self._result = result

