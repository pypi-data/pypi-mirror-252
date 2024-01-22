import os

from openai import OpenAI


class Normalization:
    """
    Takes in text as string.
    Convert to TTS input form or how it would be spoken out loud using gpt
    Clean and return the output.
    """

    def __init__(self, openai_api_key):
        self.base_messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. You will be given text in quotes. Change all the numbers and letter combos into how you'd say them out loud in normal conversation.",
            },
            {"role": "user", "content": '"My BMW 330i has a 1440p resolution."'},
            {
                "role": "assistant",
                "content": "My B M W three thirty i has a fourteen forty P resolution",
            },
            {
                "role": "user",
                "content": '"NASA flies space shuttles , the NBA makes a lot of profit."',
            },
            {
                "role": "assistant",
                "content": "NASA flies space shuttles , the N B A makes a lot of profit.",
            },
            {"role": "user", "content": '"The file is 375MB."'},
            {"role": "assistant", "content": "The file is three seventy five M B."},
            {"role": "user", "content": '"My GPA is 3.8."'},
            {"role": "assistant", "content": "My G P A is three point eight."},
            {"role": "user", "content": '"I want to buy 125 bananas."'},
            {"role": "assistant", "content": "I want to buy one twenty five bananas."},
        ]
        self.client = OpenAI(api_key=openai_api_key)

    def _get_gpt_4_response(self, model, messages, temperature):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content

    def _create_message(self, text):
        return self.base_messages + [{"role": "user", "content": '"' + text + '"'}]

    def _clean_text(self, gpt_response):
        return gpt_response.replace("-", " ")

    def normalize_text(self, text, model="gpt-4-1106-preview", temperature=0.1):
        gpt_messages = self._create_message(text)
        gpt_response = self._get_gpt_4_response(model, gpt_messages, temperature)
        return self._clean_text(gpt_response)
