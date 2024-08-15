import requests
import json
import subprocess

def batch_completion(model,messages,temperature,n,max_tokens,
                        api_base='http://127.0.0.1:8000',feature_key=''):

    whoami = get_username()
    all_response = list()
    for message in messages:
        converted_message = convert_input(message)
        payload = json.dumps(converted_message)
        response = payload
        headers = {
            'Content-Type': 'application/json',
            'Wd-PCA-Feature-Key':f'your_feature_key, $(whoami)'
        }

        response = requests.request("POST", api_base, headers=headers, data=payload)
        try:
            response = response.json()
            all_response.append(convert_output(response))
        except Exception as e:
            all_response.append(None)
    return all_response

def get_username():
    result = subprocess.run(['whoami'], capture_output=True, text=True)
    result = result.stdout
    return result

def convert_output(response):
    try:
        chunk = response['prediction']['output']['chunks'][0]
        candidate = chunk['candidates'][0]
        part = candidate['content']['parts'][0]
        return part['text']
    except Exception as e:
        print(e)
        return None


def convert_input(prompt):
    doc_input = {
        "target": {
            "provider": "echo",
            "model": "echo"
        },
        "task": {
            "type": "gcp-multimodal-v1",
            "prediction_type": "gcp-multimodal-v1",
            "input": {
            "contents": [
                {
                "role": "user",
                "parts": [
                    {
                    "text": "Give me a recipe for banana bread."
                    }
                ]
                }
            ],
            "safetySettings": [
                {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_LOW_AND_ABOVE"
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 10,
                "topK": 40,
                "topP": 0.8,
                "stopSequences": [],
                "candidateCount": 1
            }
            }
        }
    }
    doc_input['target']['provider'] = 'gcp'
    doc_input['target']['model'] = 'gemini-1.5-flash'
    doc_input['task']['input']['contents'][0]['parts'] = [{"text":prompt[0]['content']}]
    return doc_input




if __name__=='__main__':
    message_list = ["Hi How are you","I am good","How are you"]
    response = batch_completion('gemini-1.5-flash',message_list,0,1,100,api_base='http://127.0.0.1:5000')
    print(response)
