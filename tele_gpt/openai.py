import openai

from tele_gpt.config import config
from tele_gpt.exceptions import OpenAIError

openai.api_key = config.open_ai.api_key

def get_response(messages: list) -> dict:
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
    except openai.error.OpenAIError as e:
        raise OpenAIError from e
    return completion.choices[0].message.to_dict()
