# OpenAI Python bindings.
#
# Originally forked from the MIT-licensed Stripe Python bindings.

import os
import sys
from typing import TYPE_CHECKING, Optional, Union, Callable
import openai

from SpryngtimeOpenAI.ChatCompletion import ChatCompletion

openai.api_key = str(os.getenv("AZURE_OPENAI_KEY"))
openai.api_base = str(os.getenv("AZURE_OPENAI_ENDPOINT")) # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2023-05-15' # this might change in the future

from openai.api_resources import (
    Audio,
    Completion,
    Customer,
    Deployment,
    Edit,
    Embedding,
    Engine,
    ErrorObject,
    File,
    FineTune,
    FineTuningJob,
    Image,
    Model,
    Moderation,
)
from openai.error import APIError, InvalidRequestError, OpenAIError
from openai.version import VERSION


__version__ = VERSION
__all__ = [
    "APIError",
    "Audio",
    "ChatCompletion",
    "Completion",
    "Customer",
    "Edit",
    "Image",
    "Deployment",
    "Embedding",
    "Engine",
    "ErrorObject",
    "File",
    "FineTune",
    "FineTuningJob",
    "InvalidRequestError",
    "Model",
    "Moderation",
    "OpenAIError",
    "api_base",
    "api_key",
    "api_type",
    "api_version"
]
