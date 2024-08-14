import time
import json
import os

import spacy
from openai.types import Completion as OpenAICompletion
from openai import RateLimitError as OpenAIRateLimitError
from openai import APIError as OpenAIAPIError
from openai import Timeout as OpenAITimeout

# from litellm import batch_completion
# from litellm.types.utils import ModelResponse

# Setup spaCy NLP
nlp = None

# Setup OpenAI API
openai_client = None

# Setup Claude 2 API
bedrock = None
anthropic_client = None


def get_llm_full_name(llm_name):
    if llm_name == 'claude3-sonnet':
        return 'anthropic.claude-3-sonnet-20240229-v1:0' if os.environ.get('AWS_REGION_NAME') else 'claude-3-sonnet-20240229'
    elif llm_name == 'claude3-haiku':
        return 'anthropic.claude-3-haiku-20240307-v1:0' if os.environ.get('AWS_REGION_NAME') else 'claude-3-haiku-20240307'
    return llm_name


def sentencize(text):
    """Split text into sentences"""
    global nlp
    if not nlp:
        nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    return [sent for sent in doc.sents]


def split_text(text, segment_len=200):
    """Split text into segments according to sentence boundaries."""
    segments, seg = [], []
    sents = [[token.text for token in sent] for sent in sentencize(text)]
    for sent in sents:
        if len(seg) + len(sent) > segment_len:
            segments.append(" ".join(seg))
            seg = sent
            # single sentence longer than segment_len
            if len(seg) > segment_len:
                # split into chunks of segment_len
                seg = [
                    " ".join(seg[i:i+segment_len])
                    for i in range(0, len(seg), segment_len)
                ]
                segments.extend(seg)
                seg = []
        else:
            seg.extend(sent)
    if seg:
        segments.append(" ".join(seg))
    return segments


def get_model_batch_response(
        prompts,
        model,
        temperature=0,
        n_choices=1,
        max_new_tokens=500,
        api_base=None
):
    """
    Get batch generation results with given prompts.

    Parameters
    ----------
    prompts : List[str]
        List of prompts for generation.
    temperature : float, optional
        The generation temperature, use greedy decoding when setting
        temperature=0, defaults to 0.
    model : str, optional
        The model for generation, defaults to 'bedrock/anthropic.claude-3-sonnet-20240229-v1:0'.
    n_choices : int, optional
        How many samples to return for each prompt input, defaults to 1.
    max_new_tokens : int, optional
        Maximum number of newly generated tokens, defaults to 500.

    Returns
    -------
    response_list : List[str]
        List of generated text.
    """
    if not prompts or len(prompts) == 0:
        raise ValueError("Invalid input.")

    message_list = []
    for prompt in prompts:
        if len(prompt) == 0:
            raise ValueError("Invalid prompt.")
        if isinstance(prompt, str):
            messages = [{
                'role': 'user',
                'content': prompt
            }]
        elif isinstance(prompt, list):
            messages = prompt
        else:
            raise ValueError("Invalid prompt type.")
        message_list.append(messages)
    import litellm
    litellm.suppress_debug_info = True
    # litellm.drop_params=True
    while True:
        responses = batch_completion(
            model=model,
            messages=message_list,
            temperature=temperature,
            n=n_choices,
            max_tokens=max_new_tokens,
            api_base=api_base
        )
        try:
            assert all([isinstance(r, ModelResponse) for r in responses])
            if n_choices == 1:
                response_list = [r.choices[0].message.content for r in responses]
            else:
                response_list = [[res.message.content for res in r.choices] for r in responses]

            assert all([r is not None for r in response_list])
            return response_list
        except:
            exception = None
            for e in responses:
                if isinstance(e, ModelResponse):
                    continue
                elif isinstance(e, OpenAIRateLimitError) or isinstance(e, OpenAIAPIError) or isinstance(e, OpenAITimeout):
                    exception = e
                    break
                else:
                    print('Exit with the following error:')
                    print(e)
                    return None

            print(f"{exception} [sleep 10 seconds]")
            time.sleep(10)
            continue

# import aiohttp
# import asyncio
# from typing import List, Union, Dict, Any
#
# async def get_model_batch_response(
#     prompts: List[Union[str, List[dict]]],
#     feature_key: str,
#     model: str = 'gemini-1.5-flash',
#     temperature: float = 0.0,
#     n_choices: int = 1,
#     max_new_tokens: int = 1024,
#     api_base: str = 'http://localhost:8000/v1alpha1/v1alpha1/predictions',
#     top_k: int = 40,
#     top_p: float = 1.0,
#     provider: str = 'gcp',
#     task_type: str = 'gcp-multimodal-v1',
#     max_retries: int = 3,
#     retry_delay: float = 1.0
# ):
#     """
#     Get batch generation results with given prompts using the updated API structure.
#
#     Parameters
#     ----------
#     prompts : List[Union[str, List[dict]]]
#         List of prompts for generation. Each prompt can be a string or a list of message dictionaries.
#     model : str, optional
#         The model for generation, defaults to 'gemini-1.5-flash'.
#     temperature : float, optional
#         The generation temperature, defaults to 0.0.
#     n_choices : int, optional
#         How many samples to return for each prompt input, defaults to 1.
#     max_new_tokens : int, optional
#         Maximum number of newly generated tokens, defaults to 1024.
#     api_base : str, optional
#         The base URL for the API, defaults to 'http://localhost:8000/v1alpha1/v1alpha1/predictions'.
#     feature_key : str, optional
#         Your feature key for authentication.
#     top_k : int, optional
#         Top-k parameter for generation, defaults to 40.
#     top_p : float, optional
#         Top-p parameter for generation, defaults to 1.0.
#     provider : str, optional
#         The provider for the model, defaults to 'gcp'.
#     task_type : str, optional
#         The task type for generation, defaults to 'gcp-multimodal-v1'.
#     max_retries : int, optional
#         Maximum number of retries for each request, defaults to 3.
#     retry_delay : float, optional
#         Initial delay between retries in seconds, defaults to 1.0.
#
#     Returns
#     -------
#     response_list : List[str]
#         List of generated text.
#     """
#     if not prompts or len(prompts) == 0:
#         raise ValueError("Invalid input.")
#
#     url = f"{api_base}?bypass_auth=true"
#     headers = {
#         'Content-Type': 'application/json',
#         'Wd-PCA-Feature-Key': f'{feature_key}, {await asyncio.to_thread(get_username)}'
#     }
#
#     async def fetch(session, prompt):
#         if isinstance(prompt, str):
#             contents = [{"role": "user", "parts": [{"text": prompt}]}]
#         elif isinstance(prompt, list):
#             contents = [{"role": m['role'], "parts": [{"text": m['content']}] } for m in prompt]
#         else:
#             raise ValueError("Invalid prompt type.")
#
#         data = {
#             "target": {
#                 "provider": provider,
#                 "model": model
#             },
#             "task": {
#                 "type": task_type,
#                 "prediction_type": task_type,
#                 "input": {
#                     "contents": contents,
#                     "safetySettings": [
#                         {
#                             "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#                             "threshold": "BLOCK_LOW_AND_ABOVE"
#                         }
#                     ],
#                     "generationConfig": {
#                         "temperature": temperature,
#                         "maxOutputTokens": max_new_tokens,
#                         "topK": top_k,
#                         "topP": top_p,
#                         "stopSequences": [],
#                         "candidateCount": n_choices
#                     }
#                 }
#             }
#         }
#
#         for attempt in range(max_retries):
#             try:
#                 async with session.post(url, headers=headers, json=data) as response:
#                     response.raise_for_status()
#                     result = await response.json()
#                     return result['predictions'][0]['candidates'][0]['content']
#             except aiohttp.ClientError as e:
#                 if attempt == max_retries - 1:
#                     print(f"Failed after {max_retries} attempts: {e}")
#                     return None
#                 await asyncio.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
#
#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch(session, prompt) for prompt in prompts]
#         return await asyncio.gather(*tasks)
#
# async def get_username():
#     process = await asyncio.create_subprocess_exec(
#         'whoami', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
#     )
#     stdout, _ = await process.communicate()
#     return stdout.decode().strip()
