from openai import OpenAI
import openai
from copy import deepcopy
from box import Box

MODEL_PRICE = {
    "gpt-3.5-turbo-0125": [0.5 / 1000000, 1.5 / 1000000],
    "gpt-3.5-turbo-0301": [1.5 / 1000000, 2 / 1000000],
    # "gpt-3.5-turbo-0613": [0.5 / 1000000, 1.5 / 1000000],
    # "gpt-4-0314": [30 / 1000000, 60 / 1000000],
    # "gpt-4-0613": [30 / 1000000, 60 / 1000000],
    # "gpt-4-2024-03-12": [30 / 1000000, 60 / 1000000],
    "gpt-4": [30 / 1000000, 60 / 1000000],
    "gpt-4-0125-preview": [10 / 1000000, 30 / 1000000],
    "gpt-4o": [5 / 1000000, 15 / 1000000],
    "gpt-4o-2024-05-13": [5 / 1000000, 15 / 1000000],
    "gpt-4o-2024-08-06": [2.5 / 1000000, 10 / 1000000],
    "gpt-4o-mini": [0.15 / 1000000, 0.6 / 1000000],
    "gpt-4o-mini-2024-07-18": [0.15 / 1000000, 0.6 / 1000000],
    # "gpt-3.5-turbo-instruct": [0.5 / 1000000, 1.5 / 1000000],
    # "gpt-3.5-turbo-instruct-2024-01-20": [0.4 / 1000000, 1.2 / 1000000],
    # "gpt-4-instruct": [28 / 1000000, 55 / 1000000],
    # "gpt-4-instruct-2024-01-20": [25 / 1000000, 50 / 1000000],
    # "gpt-4-instruct-2024-07-14": [20 / 1000000, 45 / 1000000],
    # "gpt-4o-instruct": [4 / 1000000, 12 / 1000000],
    # "gpt-4o-instruct-2024-06-01": [3 / 1000000, 9 / 1000000],
}


def convert_stream_completion(stream_output, verbose):
    collected_messages = []
    full_response = []
    usage_info = None
    model = None
    created = None
    for chunk in stream_output:
        full_response.append(chunk)
        if chunk.choices:
            chunk_message = chunk.choices[0].delta.content
            if chunk_message:
                collected_messages.append(chunk_message)
                if verbose:
                    print(chunk_message, end="", flush=True)
        else:
            usage_info = chunk.usage
            model = chunk.model
            created = chunk.created

    full_message = "".join(collected_messages)

    complete_response = {
        "id": full_response[0].id,
        "object": full_response[0].object,
        "created": created,
        "model": model,
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": full_message,
                },
                "finish_reason": "stop",
                "index": 0,
            }
        ],
        "usage": usage_info,
    }
    return Box(complete_response)


class GPT:
    def __init__(self, api_key, model) -> None:
        self.client = OpenAI(api_key=api_key)
        self.instruction = None
        self.model = model
        self.model_emb = "text-embedding-3-large"
        openai.api_key = api_key
        self.params = {
            "response_format": {"type": "json_object"},
            "max_tokens": 200,
            "temperature": 0.9,
            "seed": 0,
        }

    def set_param(self, **kwargs):
        self.params.update(kwargs)
        print(f"Now gpt_params : {self.params}")

    def set_instruction(self, instruction):
        self.instruction = instruction
        print("Instruction is set")

    def set_model(self, model_name):
        self.model = model_name
        print("Model is set to ", self.model)

    def chat(self, comment, return_all=False):
        messages = [{"role": "user", "content": comment}]
        if self.instruction:
            messages.insert(0, {"role": "system", "content": self.instruction})

        completion = self.client.chat.completions.create(
            model=self.model, messages=messages, **self.params
        )
        if not return_all:
            return completion.choices[0].message.content
        else:
            return completion

    def stream(self, comment, verbose=True, return_all=False):
        messages = [{"role": "user", "content": comment}]
        if self.instruction:
            messages.insert(0, {"role": "system", "content": self.instruction})
        stream_params = deepcopy(self.params)
        stream_params.update({"stream_options": {"include_usage": True}})
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            **stream_params,
        )
        completion = convert_stream_completion(stream, verbose)

        if not return_all:
            return completion.choices[0].message.content
        else:
            return completion

    def embed(self, texts, return_all=False):
        if isinstance(texts, str):
            texts = [texts]
        # response = self.client.embeddings.create(model=self.model, input=texts)
        response = openai.embeddings.create(input=texts, model=self.model_emb)
        if not return_all:
            return [r.embedding for r in response.data]
        else:
            return response

    @staticmethod
    def cal_price(completion, model_name, exchange_rate=1400):
        if model_name in MODEL_PRICE:
            token_prices = MODEL_PRICE[model_name]
            return exchange_rate * (
                completion.usage.prompt_tokens * token_prices[0]
                + completion.usage.completion_tokens * token_prices[1]
            )
        print(f"{model_name} not in price dict")
        return 0

    # def list_models(self):
    #     models = self.client.models.list()
    #     return [model["id"] for model in models["data"]]

    # def summarize(self, text):
    #     summary_instruction = "Please provide a concise summary of the following text."
    #     completion = self.client.chat.completions.create(
    #         model=self.model,
    #         messages=[
    #             {"role": "system", "content": summary_instruction},
    #             {"role": "user", "content": text},
    #         ],
    #     )
    #     return completion.choices[0].message.content
