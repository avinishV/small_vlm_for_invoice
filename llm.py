import os
import base64
import json
from openai import OpenAI, APIConnectionError
import traceback
import time


def get_base64_image(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def validate_json(job_id, response_json: str):
    try:
        # Parse the JSON response
        data = process_gpt_response(response_json)
        print(f"JobId {job_id} Validation successful.")
        return data
    except Exception as ex:
        print("Validation error:")
        print(traceback.format_exc(ex))
        return None

def process_gpt_response(s):
    try:
        s = s[next(idx for idx, c in enumerate(s) if c in "{["):] 
    except StopIteration:
        return {}
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        return json.loads(s[:e.pos]) #"{\"key\": \"value\"} efgh" to "{\"key\": \"value\"}"

def generate_prompt(prompt, image_list, attachment_type, system_prompt):
    # Start with the base template
    chat_template = [
        { "role": "system", "content": system_prompt },
        { 
            "role": "user", 
            "content": []
        }
    ]

    # Add the text prompt
    chat_template[1]["content"].append({ 
        "type": "text", 
        "text": prompt 
    })

    # Add image URLs
    for image in image_list:
        # path -> read and then encode
        if attachment_type != 'bytes':
            base64_image = get_base64_image(image)
        # bytes
        else:
            base64_image=base64.b64encode(image).decode('utf-8')
        chat_template[1]["content"].append({ 
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })

    return chat_template

def generate_vllm_response(client, model_name, messages, max_tokens=1000, temperature=0):
    try:
        t0 = time.time()
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_tokens
        )
        t1 = time.time()

        print("Prompt Tokens :",response.usage.prompt_tokens,"Completion Tokens :", response.usage.completion_tokens, "Response Time :", str(round(t1-t0, 4)))
        # print("Response received:", response)
        return {
            'statusCode': 200,
            'body': response.choices[0].message.content,
            'input_token': response.usage.prompt_tokens,       
            'output_token': response.usage.completion_tokens
        }

    except Exception as ex:
        print("Exception error: ")
        print(traceback.format_exc(ex))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(ex), 'traceback': traceback.format_exc()})
        }