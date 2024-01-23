from dataclasses import is_dataclass, fields
from json import loads
from os import path
from os.path import join
from typing import Dict, Any, List, Mapping, Set

from jinja2 import FileSystemLoader, Environment
from openai.openai_object import OpenAIObject

from .config import config
from .transformations import (
    include_prompt_last_line,
    strip_last_line_if_too_long,
    strip
)


def render_template(template_name: str, **kwargs) -> str:
    """Render template given template name and template arguments

    Args:
        template_name: template name
        **kwargs: arguments for the template

    Returns:
        constructed prompt
    """
    def sanitize(value: Any) -> str:
        return str(value).replace('-----', '<truncated>')

    templates_path = join(config('inputs_path'), config('templates_dir'))
    template_loader = FileSystemLoader(searchpath=templates_path)
    template_env = Environment(loader=template_loader)
    template_env.finalize = sanitize
    template = template_env.get_template(template_name + ".jinja2")
    return template.render(**kwargs)


def render_chat_template(template_name: str, **kwargs) -> List[Dict[str, str]]:
    """Render a chat template

    Args:
        template_name: template name
        **kwargs: arguments for the template

    Returns:
        constructed messages, given the template
    """
    # parameters_ = sanitize_argument(kwargs)
    parameters_ = kwargs
    raw_messages = render_template(template_name, **parameters_)
    split_messages = raw_messages.split('-----')
    messages = []
    for split_message in split_messages:
        if split_message.strip() == '':
            continue
        try:
            metadata, content = split_message.split(":", 1)
        except ValueError:
            raise ValueError(
                f"The chat template contains an incorrect message (without "
                f"colon): '{split_message}'."
            )
        metadata = metadata.split(',')
        role = metadata[0].strip()
        name = metadata[1].strip() if len(metadata) > 1 else None
        content = content.strip()
        if name is None:
            message = {'role': role, 'content': content}
        else:
            message = {'role': role, 'name': name, 'content': content}
        messages.append(message)
    return messages


def sanitize_argument(argument: Any, seen: Set[int] = None) -> Any:
    if seen is None:
        seen = set()

    argument_id = id(argument)
    if argument_id in seen:
        return argument

    seen.add(argument_id)

    if isinstance(argument, str):
        return argument.replace('-----', '<truncated>')

    if isinstance(argument, Mapping):
        return {
            key: sanitize_argument(value, seen)
            for key, value in argument.items()
        }

    if isinstance(argument, List):
        return [sanitize_argument(value, seen) for value in argument]

    if is_dataclass(argument):
        sanitized_fields = {
            field.name: sanitize_argument(getattr(argument, field.name), seen)
            for field in fields(argument)
            if field.init
        }
        return argument.__class__(**sanitized_fields)

    return argument


def template_config(name: str) -> Dict[str, Any]:
    """Load configuration for a given template

    Args:
        name: the name of the template

    Returns:
        configuration
    """
    inputs_path = config('inputs_path')
    config_dir = config('config_dir')
    file_path = join(inputs_path, config_dir, name + '.json')
    return loads(open(file_path).read()) if path.exists(file_path) else {}


TRANSFORMATIONS = {
    'include_prompt_last_line': include_prompt_last_line,
    'strip_last_line_if_too_long': strip_last_line_if_too_long,
    'strip': strip
}

ALLOWED_PARAMETERS = (
    "model",
    "prompt",
    "suffix",
    "max_tokens",
    "temperature",
    "top_p",
    "n",
    "stream",
    "logprobs",
    "echo",
    "stop",
    "presence_penalty",
    "frequency_penalty",
    "best_of",
    "logit_bias",
    "user",
    "input",
    "instruction",
    "messages",
    "response_format"
)


def parameters(template_config_: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """Construct parameters to send in the request

    Args:
        template_config_: configuration for the template
        template_config_: configuration coming from the template

    Returns:
        parameters to send in the request
    """
    module_config = config('default_parameters')
    additional = {
        key: value
        for key, value in kwargs.items()
        if key in ALLOWED_PARAMETERS
    }
    parameters_ = {**module_config, **template_config_, **additional}
    for transformation in TRANSFORMATIONS:
        if transformation in parameters_:
            parameters_.pop(transformation)
    if config_value_equals(parameters_, 'provider', 'hugging_face'):
        parameters_ = convert_to_huggingface_parameters(parameters_)
    elif config_value_equals(parameters_, 'provider', 'anthropic'):
        parameters_ = convert_to_anthropic_parameters(parameters_)
    return parameters_


HUGGINGFACE_PARAMETERS_MAP = {
    "max_tokens": "max_new_tokens",
    "model": "repo_id",
    "stop": "early_stopping"
}


ANTHROPIC_PARAMETERS_MAP = {
    "max_tokens": "max_tokens_to_sample",
    "stop": "stop_sequences"
}


def convert_to_huggingface_parameters(
        parameters_: Dict[str, Any]
) -> Dict[str, any]:
    result = {}
    for key, value in parameters_.items():
        if key in HUGGINGFACE_PARAMETERS_MAP:
            result[HUGGINGFACE_PARAMETERS_MAP[key]] = value
        else:
            result[key] = value
    return result


def convert_to_anthropic_parameters(
        parameters_: Dict[str, Any]
) -> Dict[str, any]:
    result = {}
    for key, value in parameters_.items():
        if key in ANTHROPIC_PARAMETERS_MAP:
            result[ANTHROPIC_PARAMETERS_MAP[key]] = value
        else:
            result[key] = value
    return result


def config_value_equals(
        config_: Dict[str, Any],
        key: str,
        value: Any
) -> bool:
    """Check if the template config value equals to some value

    Args:
        config_: configuration
        key: key for which we check
        value: value that we want

    Returns:
        True, if configuration contains a key with the given name and
            value.
    """
    return key in config_ and config_[key] == value


def transformed_text(
        template_config_: Dict[str, Any],
        prompt_: str,
        response: OpenAIObject
) -> str:
    """Transform text from the response from OpenAI API

    Args:
        template_config_: config that contains information which
         transformations we should apply
        prompt_: prompt that has been sent to OpenAI API
        response: response from OpenAI API

    Returns:
        transformed text
    """
    text = response['text']
    for transformation in TRANSFORMATIONS:
        if config_value_equals(template_config_, transformation, True):
            text = TRANSFORMATIONS[transformation](prompt_, text, response)
    return text
