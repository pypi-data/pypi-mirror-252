# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


## NOTE: This file is auto generated by the swagger code generator program.
## Do not edit the file manually.

import pprint
import re  # noqa: F401
import six

import enum

class ProviderType(str, enum.Enum):
    LOCAL = "local"
    STATIC = "static"
    AWS = "aws"
    AZURE = "azure"
    GC = "gc"
    S3_COMPAT = "s3_compat"
    EXCHANGE = "exchange"
