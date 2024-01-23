"""
AgentOps events.

Classes:
    Event: Represents discrete events to be recorded.
"""
from .helpers import get_ISO_time, Models
from typing import Optional, List, Dict, Any
from pydantic import Field


class Event:
    """
    Represents a discrete event to be recorded.

    Args:
        event_type (str): Type of the event, e.g., "API Call". Required.
        params (Optional[Dict[str, Any]], optional): The parameters passed to the operation.
        returns (str, optional): The output of the operation.
        result (str, optional): Result of the operation, e.g., "Success", "Fail", "Indeterminate". Defaults to "Indeterminate".
        action_type (str, optional): Type of action of the event e.g. 'action', 'llm', 'api', 'screenshot'. Defaults to 'action'.
        model (Models, optional): The model used during the event if an LLM is used (i.e. GPT-4).
                For models, see the types available in the Models enum. 
                If a model is set but an action_type is not, the action_type will be coerced to 'llm'. 
                Defaults to None.
        prompt (str, optional): The input prompt for an LLM call when an LLM is being used. Defaults to None.
        tags (List[str], optional): Tags that can be used for grouping or sorting later. e.g. ["my_tag"]. Defaults to None.
        init_timestamp (str, optional): The timestamp for when the event was initiated, as a string in ISO 8601 format.
                Defaults to the end timestamp.
        end_timestamp (str, optional): The timestamp for when the event ended, as a string in ISO 8601 format.
        screenshot (str, optional): A screenshot of the webpage at the time of the event. Base64 string or URL. Defaults to None.

    Attributes:
        event_type (str): Type of the event.
        params (Optional[Dict[str, Any]], optional): The parameters passed to the operation.
        returns (str, optional): The output of the operation.
        result (Result): Result of the operation as Enum Result.
        action_type (str): Type of action of the event.
        model (Models, optional): The model used during the event.
        prompt (str, optional): The input prompt for an LLM call.
        tags (List[str], optional): Tags associated with the event.
        end_timestamp (str): The timestamp for when the event ended, as a string in ISO 8601 format.
        init_timestamp (str): The timestamp for when the event was initiated, as a string in ISO 8601 format.
        prompt_tokens (int, optional): The number of tokens in the prompt if the event is an LLM call
        completion_tokens (int, optional): The number of tokens in the completion if the event is an LLM call
    """

    def __init__(self, event_type: str,
                 params: Optional[Dict[str, Any]] = None,
                 returns: Optional[Dict[str, Any]] = None,
                 result: str = Field("Indeterminate",
                                     description="Result of the operation",
                                     pattern="^(Success|Fail|Indeterminate)$"),
                 action_type: Optional[str] = Field("action",
                                                    description="Type of action that the user is recording",
                                                    pattern="^(action|api|llm|screenshot)$"),
                 model: Optional[Models] = None,
                 prompt: Optional[str] = None,
                 tags: Optional[List[str]] = None,
                 init_timestamp: Optional[str] = None,
                 screenshot: Optional[str] = None,
                 prompt_tokens: Optional[int] = None,
                 completion_tokens: Optional[int] = None
                 ):
        self.event_type = event_type
        self.params = params
        self.returns = returns
        self.result = result
        self.tags = tags
        self.action_type = action_type
        self.model = model
        self.prompt = prompt
        self.end_timestamp = get_ISO_time()
        self.init_timestamp = init_timestamp if init_timestamp else self.end_timestamp
        self.screenshot = screenshot
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens

    def __str__(self):
        return str({
            "event_type": self.event_type,
            "params": self.params,
            "returns": self.returns,
            "action_type": self.action_type,
            "result": self.result,
            "model": self.model,
            "prompt": self.prompt,
            "tags": self.tags,
            "init_timestamp": self.init_timestamp,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
        })
