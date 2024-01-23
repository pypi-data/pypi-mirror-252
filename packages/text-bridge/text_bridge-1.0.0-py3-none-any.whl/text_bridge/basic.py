from logging import getLogger
from os import environ
from time import sleep
from typing import Dict, Any, List, Optional, Generator, Union

from anthropic import Client
from huggingface_hub import InferenceApi
from openai import ChatCompletion, Edit, Completion
from openai import Moderation
from openai.error import (
    RateLimitError,
    InvalidRequestError,
    APIError,
    APIConnectionError,
    ServiceUnavailableError
)
from openai.openai_object import OpenAIObject
from urllib3.exceptions import InvalidChunkLength

from .events import dispatch_event
from .templates import render_template, template_config, parameters, transformed_text, render_chat_template, \
    config_value_equals


# from .redis import cache


def complete(
        input_name: str,
        **kwargs
) -> Union[str, Generator[str, None, None]]:
    """Send a request to API to generate completion

    It will use the prompt template that is in `{model_inputs}/{templates_dir}/{input_name}_prompt.jinja2`.

    It will use the config (including the properties sent to LLM) that
    is in `{model_inputs}/{templates_dir}/{input_name}_config.json`.

    Args:
        input_name: name of the prompt to use
        **kwargs: arguments passed to the prompt template

    Returns:
        text generated in the response from OpenAI API
    """
    getLogger("models.basic").debug(f"Complete: {input_name}")
    prompt_ = render_template(input_name + "_prompt", **kwargs)
    prompt_ = prompt_[-22000:]
    template_config_ = template_config(input_name)
    parameters_ = parameters(template_config_, prompt=prompt_, **kwargs)
    try:
        if config_value_equals(parameters_, 'provider', 'hugging_face'):
            response = hugging_face_raw_complete(parameters_)
        elif config_value_equals(parameters_, 'provider', 'anthropic'):
            response = anthropic_raw_complete(parameters_)
        else:
            response = openai_raw_complete(parameters_)
    except RateLimitError:
        getLogger("models.basic").info("Retrying due to rate limit")
        sleep(5)
        return complete(input_name, **kwargs)
    if 'stream' in parameters_ and parameters_['stream']:
        log_streamed_complete_response(prompt_)
        return response
    log_complete_response(prompt_, response)
    return transformed_text(template_config_, prompt_, response)


class HuggingFaceError(Exception):
    pass


def hugging_face_raw_complete(parameters_: Dict[str, Any]) -> Dict[str, Any]:
    if 'provider' in parameters_:
        parameters_.pop('provider')
    try:
        repo_id = parameters_['repo_id']
    except KeyError:
        raise KeyError("Model (`model` property) must be set")
    parameters_.pop('repo_id')
    try:
        token = environ['HUGGING_FACE_TOKEN']
    except KeyError:
        raise KeyError(
            "HUGGING_FACE_TOKEN environment variable must be set"
        )
    inference = InferenceApi(repo_id=repo_id, token=token)
    print(parameters_)
    prompt = parameters_['prompt']
    parameters_.pop('prompt')
    response = inference(prompt, parameters_)
    if 'error' in response:
        raise HuggingFaceError(response['error'])
    result = {'text': response[0]['generated_text']}
    result['text'] = result['text'][len(prompt):]
    result['text'] = result['text'].split(parameters_['early_stopping'], 1)[0]
    getLogger("models.basic").debug("Complete")
    getLogger("models.basic").debug(f"Prompt: {result['text']}")
    return result


def anthropic_raw_complete(parameters_: Dict[str, Any]) -> Dict[str, Any]:
    if 'provider' in parameters_:
        parameters_.pop('provider')
    try:
        client = Client(environ['ANTHROPIC_API_KEY'])
    except KeyError:
        raise KeyError(
            "ANTHROPIC_API_KEY environment variable must be set"
        )
    return {'text': client.completion(**parameters_)['completion']}


def only_text_wrapper_for_completion(
        response: Generator[Dict[str, Any], None, None]
) -> Generator[str, None, None]:
    for token in response:
        yield token['choices'][0]['text']


def openai_raw_complete(
        parameters_: Dict[str, Any],
        retry_if_not_stop: int = 0,
        delay_: int = 0
) -> Optional[Union[OpenAIObject, Generator[str, None, None]]]:
    if 'provider' in parameters_:
        parameters_.pop('provider')
    response = None
    for i in range(retry_if_not_stop + 1):
        try:
            response = Completion.create(**parameters_)
            if config_value_equals(parameters_, 'stream', True):
                return only_text_wrapper_for_completion(response)
            response = response['choices'][0]
        except RateLimitError:
            delay_ = delay_ * 2 if delay_ else 5
            getLogger("models.basic").info("Retrying due to rate limit")
            delay(delay_)
            return openai_raw_complete(
                parameters_,
                retry_if_not_stop - i,
                delay_
            )
        except (
                APIError,
                APIConnectionError,
                ServiceUnavailableError
        ) as error:
            delay_ = delay_ * 2 if delay_ else 5
            getLogger("models.basic").error(error)
            getLogger("models.basic").info("Retrying due to API error")
            delay(delay_)
            return openai_raw_complete(
                parameters_,
                retry_if_not_stop - i,
                delay_
            )
        if response['finish_reason'] == 'stop':
            break
        if i != retry_if_not_stop:
            getLogger("models.basic").info("Retrying due to finish reason")
    return response


def log_complete_response(prompt_: str, response: OpenAIObject):
    """Log response from API

    Args:
        prompt_: prompt that has been sent
        response: response from API
    """
    getLogger("models.basic").debug("Complete")
    getLogger("models.basic").debug(f"Prompt: {prompt_}")
    getLogger("models.basic").debug(f"Response: {response['text']}")
    if 'finish_reason' in response:
        getLogger("models.basic").debug(
            f"Response: {response['finish_reason']}"
        )


def log_streamed_complete_response(prompt_: str):
    """Log response from API

    Args:
        prompt_: prompt that has been sent
    """
    getLogger("models.basic").debug("Complete (streamed response)")
    getLogger("models.basic").debug(f"Prompt: {prompt_}")


def complete_with_suffix(
        input_name: str,
        retry_if_not_stop: int = 0,
        **kwargs
) -> Union[str, Generator[str, None, None]]:
    """Send a request to OpenAI API to generate completion with suffix

    The model will generate completion in place of '[insert]' from the
    prompt.

    Args:
        input_name: name of the prompt to use
        retry_if_not_stop: if the finish reason is not stop, then it
            will generate once again. This is the maximum number of
            retries.
        **kwargs: arguments passed to the prompt template

    Returns:
        text generated in the response from OpenAI API
    """
    if retry_if_not_stop < 0:
        ValueError("retry_if_not_stop must be at least 0")
    prompt_ = render_template(input_name + "_prompt", **kwargs)
    try:
        prompt_, suffix = prompt_.split('[insert]', 1)
    except ValueError:
        raise ValueError(
            "When using complete_with_suffix prompt must contain '[insert]'."
        )
    template_config_ = template_config(input_name)
    parameters_ = parameters(
        template_config_,
        prompt=prompt_,
        suffix=suffix,
        **kwargs
    )
    response = openai_raw_complete(parameters_, retry_if_not_stop)
    if 'stream' in parameters_ and parameters_['stream']:
        log_streamed_complete_response(prompt_)
        return response
    log_complete_with_suffix_response(prompt_, suffix, response)
    return transformed_text(template_config_, prompt_, response)


def log_complete_with_suffix_response(
        prompt_: str,
        suffix: str,
        response: OpenAIObject
):
    """Log response from API

    Args:
        prompt_: prompt that has been sent
        suffix: suffix that has been sent
        response: response from API
    """
    getLogger("models.basic").debug("Complete with suffix")
    getLogger("models.basic").debug(f"Prompt: {prompt_}")
    getLogger("models.basic").debug(f"Suffix: {suffix}")
    getLogger("models.basic").debug(f"Response: {response['text']}")
    getLogger("models.basic").debug(f"Response: {response['finish_reason']}")


class CouldNotEditError(Exception):
    pass


def edit(input_name: str, **kwargs) -> str:
    """Send a request to OpenAI API to generate edition

    Args:
        input_name: name of the prompt to use
        **kwargs: arguments passed to the prompt template

    Returns:
        text generated in the response from OpenAI API
    """
    input_ = render_template(input_name + "_input", **kwargs)
    instruction = render_template(input_name + "_instruction", **kwargs)
    template_config_ = template_config(input_name)
    additional_parameters = {
        'input': input_,
        'instruction': instruction,
        **kwargs
    }
    parameters_ = parameters(
        template_config_,
        **additional_parameters
    )
    try:
        response = Edit.create(**parameters_)['choices'][0]
    except RateLimitError:
        getLogger("models.basic").info("Retrying due to rate limit")
        sleep(5)
        return edit(input_name, **kwargs)
    except (APIError, APIConnectionError, ServiceUnavailableError):
        getLogger("models.basic").info("Retrying due to API error")
        sleep(5)
        return edit(input_name, **kwargs)
    except InvalidRequestError as error:
        if str(error).startswith("Could not edit text"):
            getLogger("models.basic").debug("Could not edit")
            raise CouldNotEditError
        raise error
    log_edit_response(input_, instruction, response)
    return response["text"]


def log_edit_response(input_: str, instruction: str, response: OpenAIObject):
    """Log edit response from API

    Args:
        input_: input passed to API
        instruction: instruction passed to API
        response: response from API
    """
    getLogger("models.basic").debug("Edit")
    getLogger("models.basic").debug(f"Input: {input_}")
    getLogger("models.basic").debug(f"Instruction: {instruction}")
    getLogger("models.basic").debug(f"Response: {response['text']}")


def flagged(input_: str, delay_: int = 0) -> bool:
    try:
        response = Moderation.create(input_)
    except RateLimitError:
        delay_ = delay_ * 2 if delay_ else 5
        getLogger("models.basic").info("Retrying due to rate limit")
        delay(delay_)
        return flagged(input_, delay_)
    except (APIError, APIConnectionError, ServiceUnavailableError) as error:
        getLogger("models.basic").error(error, exc_info=True)
        getLogger("models.basic").info("Retrying due to api error")
        delay_ = delay_ * 2 if delay_ else 5
        delay(delay_)
        return flagged(input_, delay_)
    log_flagged_response(input_, response)
    return response["results"][0]["flagged"]


def log_flagged_response(input_: str, response: OpenAIObject):
    """Log flagged response from API

    Args:
        input_: input passed to API
        response: response from API
    """
    getLogger("models.basic").debug("Flagged")
    getLogger("models.basic").debug(f"Input: {input_}")
    getLogger("models.basic").debug(
        f"Response: {response['results'][0]['flagged']}"
    )


def chat_complete(
        input_name: str,
        **kwargs
) -> Union[str, Generator[str, None, None]]:
    """Send a request to API to generate chat completion.

    It will use the prompt template that is in
    `{model_inputs}/{templates_dir}/{input_name}_messages.jinja2`.

    The prompt template is in the following form (it's an example):

    ```
    system:
    First system message

    -----

    user:
    Second message

    -----

    assistant:
    Third message
    ```

    Jinja2 library will be used to render the template. It will use the
    arguments passed to this function as the arguments for the template.
    If the argument is a correct name of one of the properties that can
    be passed as an argument to the request (like for example
    "max_tokens"), then it will be passed as an argument to the request.

    It will use config (including the properties sent to LLM) that is
    in `{model_inputs}/{templates_dir}/{input_name}_config.json`.

    Args:
        input_name: name of the prompt to use
        **kwargs: arguments passed to the prompt template

    Returns:
        text generated in the response from OpenAI API
    """
    getLogger("models.basic").debug(f"Chat complete: {input_name}")
    messages = render_chat_template(input_name + "_messages", **kwargs)
    template_config_ = template_config(input_name)
    parameters_ = parameters(template_config_, messages=messages, **kwargs)
    response = openai_raw_chat_complete(parameters_)
    if 'stream' in parameters_ and parameters_['stream']:
        log_streamed_chat_complete_response(messages)
        return response
    log_chat_complete_response(messages, response)
    return response


def openai_raw_chat_complete(
        parameters_: Dict[str, Any],
        retry_if_not_stop: int = 0,
        delay_: int = 0
) -> Union[str, Generator[str, None, None]]:
    response = None
    for i in range(retry_if_not_stop + 1):
        try:
            response = ChatCompletion.create(**parameters_)
            if 'stream' in parameters_ and parameters_['stream']:
                return only_text_wrapper_for_chat_completion(
                    response
                )
            response = response['choices'][0]
        except RateLimitError:
            delay_ = delay_ * 2 if delay_ else 5
            getLogger("models.basic").info("Retrying due to rate limit")
            delay(delay_)
            return openai_raw_chat_complete(
                parameters_,
                retry_if_not_stop - i,
                delay_
            )
        except (
                APIError,
                APIConnectionError,
                ServiceUnavailableError
        ) as error:
            getLogger("models.basic").error(error, exc_info=True)
            getLogger("models.basic").info("Retrying due to API error")
            delay_ = delay_ * 2 if delay_ else 5
            delay(delay_)
            return openai_raw_chat_complete(
                parameters_,
                retry_if_not_stop - i,
                delay_
            )
        if response['finish_reason'] == 'stop':
            break
        if i != retry_if_not_stop:
            getLogger("models.basic").info("Retrying due to finish reason")
    return response['message']['content']


def only_text_wrapper_for_chat_completion(
        response: Generator[Dict[str, Any], None, None]
) -> Generator[str, None, None]:
    try:
        for chunk in response:
            delta = chunk['choices'][0]['delta']
            if 'content' not in delta:
                continue
            yield delta['content']
    except InvalidChunkLength as error:
        getLogger("models.basic").error(error, exc_info=True)
        getLogger("models.basic").info(
            "Ending completion due to InvalidChunkLength error"
        )
        return


def delay(time: int, step: int = 5):
    getLogger("models.basic").info(f"Delay: {str(time)}")
    dispatch_event("delay")
    for i in range(0, time, step):
        sleep(step)
        dispatch_event("delay_step")


def log_streamed_chat_complete_response(messages: List[Dict[str, str]]):
    getLogger("models.basic").debug("Chat complete (streamed response)")
    readable = readable_raw_messages(messages)
    getLogger("models.basic").debug(f"Messages: {readable}")
    getLogger("models.basic").debug(
        f"Messages length: {len(str(messages))} characters"
    )


def log_chat_complete_response(messages: List[Dict[str, str]], response: str):
    getLogger("models.basic").debug("Chat complete")
    readable = readable_raw_messages(messages)
    getLogger("models.basic").debug(f"Messages: {readable}")
    getLogger("models.basic").debug(
        f"Messages length: {len(str(messages))} characters"
    )
    getLogger("models.basic").debug(f"Response: {response}")
    getLogger("models.basic").debug(
        f"Response length: {len(str(response))} characters"
    )
    
    
def readable_raw_messages(messages: List[Dict[str, str]]) -> str:
    messages_as_strings = []
    for message in messages:
        content = message['content']
        header = message
        header.pop('content', None)
        header = str(header)
        messages_as_strings.append(f"{header}\n\n{content}")
    return "\n-----\n".join(messages_as_strings)
