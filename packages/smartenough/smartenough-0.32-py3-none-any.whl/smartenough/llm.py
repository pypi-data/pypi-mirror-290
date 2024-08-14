import os
import re
import json
import logging
import time
import math
import random

import requests
import validators
from urlextract import URLExtract
from bs4 import BeautifulSoup

from cachetools import TTLCache
model_cache = TTLCache(maxsize=5, ttl=3600)

import anthropic
import openai
from mistralai import Mistral
import google.generativeai as genai


class UnsupportedProviderException(Exception):
    """Exception raised for unsupported providers."""
    def __init__(self, provider, message="Provider not supported"):
        self.model = provider
        self.message = message
        super().__init__(self.message)


class UnsupportedValidationException(Exception):
    """Exception raised for unsupported validation."""
    def __init__(self, validation, message="Validation type not supported"):
        self.validation = validation
        self.message = message
        super().__init__(self.message)


def find_json(text):
    json_match = re.search(r'({.*})', text, re.DOTALL)

    if json_match:
        json_str = json_match.group(1)
        try:
            return json.loads(json_str)
        except Exception:
            return []
    else:
        return []


def find_urls(text):
    extractor = URLExtract()
    potential_urls = extractor.find_urls(text, check_dns=True)
    valid_urls = []
    for url in potential_urls:
        if url.endswith('.'):
            url = url[:-1]
        if validators.url(url):
            valid_urls.append(url)
    return valid_urls


def find_html(text):
    soup = BeautifulSoup(text, 'html.parser')

    largest_block = None
    largest_size = 0

    for element in soup.children:
        if element.name and len(list(element.descendants)) > largest_size:
            largest_block = element
            largest_size = len(list(element.descendants))

    if largest_block:
        return largest_block.prettify()
    else:
        return ""


def get_openrouter_free_models():
    try:
        free_models = model_cache["free_models"]
    except KeyError:
        endpoint = "https://openrouter.ai/api/v1/models"
        response = requests.get(endpoint, headers={'Authorization': f"Bearer {os.environ.get('OPENROUTER_API_KEY')}"})
        api_result = response.json()
        free_models = [
            model.get("id") for model in api_result.get("data", [])
            if model.get("architecture", {}).get("modality") == "text->text"
            and model.get("pricing", {}).get("prompt") == "0"
            and model.get("pricing", {}).get("completion") == "0"
        ]
        model_cache["free_models"] = free_models

    models = random.sample(free_models, 2)

    return models


def send_to_openrouter(context, instructions, model_list=None):

    if model_list is None:
        model_list = get_openrouter_free_models()

    response = requests.post(
      url="https://openrouter.ai/api/v1/chat/completions",
      headers={
        "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
      },
      data=json.dumps({
        "models": model_list,
        "route": "fallback",
        "messages": [
          {"role": "user", "content": f"{instructions}\n\n{context}"}
        ]
      })
    )
    
    response_data = response.json()
    
    if 'choices' in response_data and len(response_data['choices']) > 0:
        text_response = response_data['choices'][0]\
                .get('message', 'No response text found.')\
                .get('content','No content found.')
    else:
        text_response = 'No response found.'

    return text_response


def send_to_google(context, instructions, model_id):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_id)

    # Prepare the content dictionary
    content = {
        "parts": [
            {"text": instructions},
            {"text": context}
        ]
    }

    # Generate content
    response = model.generate_content(
        content,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=4000,
            temperature=0.0,
        )
    )

    # Check if the response has candidates and parts
    if not response.candidates or not response.candidates[0].content.parts:
        # Check the safety ratings to determine if the response was blocked
        safety_ratings = response.candidates[0].safety_ratings
        if safety_ratings and safety_ratings[0].blocked:
            raise ValueError(f"Response was blocked for the following reason: {safety_ratings[0].reason}")
        else:
            raise ValueError("No valid parts were returned in the response.")

    # Join the parts' texts
    response_text = "\n".join(part.text for part in response.candidates[0].content.parts)
    return response_text


def send_to_anthropic(context, instructions, model_id):
    client = anthropic.Anthropic()

    message = client.messages.create(
        model=model_id,
        max_tokens=4000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{instructions}\n\n{context}"
                    }
                ]
            }
        ]
    )

    return message.content[0].text


def send_to_openai(context, instructions, model_id):
    client = openai.OpenAI()

    chat_completion = client.chat.completions.create(
    model=model_id,
    messages=[
            {
                "role": "user",
                "content": f"{instructions}\n\n{context}"
            }
        ]
    )

    return chat_completion.choices[0].message.content


def send_to_mistral(context, instructions, model_id):

    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    chat_response = client.chat.complete(
        model=model_id,
        messages=[
            {
                "role": "user",
                "content": f"{instructions}\n\n{context}",
            },
        ]
    )

    return chat_response.choices[0].message.content


MODEL_CONFIGS = {
    "Anthropic": {
        "chunk_size": 200000,
        "send_function": send_to_anthropic,
        "model_id":"claude-3-haiku-20240307" 
    },
    "OpenAI": {
        "chunk_size": 128000,
        "send_function": send_to_openai,
        "model_id": "gpt-4o-mini"
    },
    "Mistral": {
        "chunk_size": 128000,
        "send_function": send_to_mistral,
        "model_id": "open-mistral-nemo"
    },
    "Google": {
        "chunk_size": 1048576,
        "send_function": send_to_google,
        "model_id": "gemini-1.5-flash"
    },
    "OpenRouter": {
        "chunk_size": 32000, #Note this is a guess. see the latest free models here https://openrouter.ai/models?order=top-weekly&max_price=0
        "send_function": send_to_openrouter,
        "model_id": None #this param isn't used, we just pick a random free model
    },
    "Meta": {
        "chunk_size": 128000,
        "send_function": send_to_openrouter,
        "model_id": ["meta-llama/llama-3.1-8b-instruct","meta-llama/llama-3-8b-instruct"]
    }
}


def get_supported_providers():
    return list(MODEL_CONFIGS.keys()) + ["Random"]


def get_smart_answer(instructions, additional_context="", model_provider="OpenRouter", validation=None):
    if model_provider == "Random":
        model_provider = random.choice(list(MODEL_CONFIGS.keys()))
    elif model_provider not in MODEL_CONFIGS:
        raise UnsupportedProviderException(f"Provider={model_provider}")

    config = MODEL_CONFIGS[model_provider]
    
    # NOTE we give the models a little buffer here token-wise by only giving it 90% of its capacity in CHARACTERS (not tokens, precicesly)
    truncated_text = additional_context[:max(0, int((config["chunk_size"] - len(instructions)) // 1.1))]

    # NOTE we always assume the model is able to handle the instructions... that might not always be the case
    response = config["send_function"](truncated_text, instructions, config["model_id"])
    
    if validation is None:
        return response
    elif validation == "url":
        return find_urls(response)
    elif validation == "html":
        return find_html(response)
    elif validation == "json":
        return find_json(response)
    else:
        raise UnsupportedValidationException(validation)

