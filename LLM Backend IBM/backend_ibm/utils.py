import requests
from dotenv import load_dotenv,find_dotenv
import os

load_dotenv(find_dotenv())
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

def get_ibm_red_vote(prompt,active_list):
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

    body = {
        "input": f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        Youre a player and youre trying to find out which player is human 
        with his/her answers and conversations. Active List is {active_list}. Give the number of the human player.
        With stating only number of the human player. Text messagess : {prompt}
        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 900,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        },
        "model_id": "meta-llama/llama-3-3-70b-instruct",
        "project_id": "418fa904-02e8-4a83-8093-918fe3cb13c1",
        "moderations": {
            "hap": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                }
            },
            "pii": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                }
            }
        }
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    print(data['results'][0]['generated_text'])
    return data['results'][0]['generated_text']

def get_ibm_blue_vote(prompt,active_list):
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

    body = {
        "input": f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        Youre a player and youre trying to find out which player is human 
        with his/her answers and conversations. Active List is {active_list}. Give the number of the human player.
        With stating only number of the human player. Text messagess : {prompt}
        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 900,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        },
        "model_id": "meta-llama/llama-3-3-70b-instruct",
        "project_id": "418fa904-02e8-4a83-8093-918fe3cb13c1",
        "moderations": {
            "hap": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                }
            },
            "pii": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                }
            }
        }
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BEARER_TOKEN}"    
        }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    print(data['results'][0]['generated_text'])
    return data['results'][0]['generated_text']

def get_ibm_red_chat(prompt):
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

    body = {
        "input": f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        You are an player and youre trying to pretend like a human in a game and answer 
        questions as a human would do. Also, give your answer very short and dont repeat any past messages. Past messages : {prompt}
        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 900,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        },
        "model_id": "meta-llama/llama-3-3-70b-instruct",
        "project_id": "418fa904-02e8-4a83-8093-918fe3cb13c1",
        "moderations": {
            "hap": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                }
            },
            "pii": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                }
            }
        }
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BEARER_TOKEN}"    
        }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    print(data['results'][0]['generated_text'])
    return data['results'][0]['generated_text']

def get_ibm_blue_chat(prompt):
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

    body = {
        "input": f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        You are an player and youre trying to pretend like a human in a game and answer 
        questions as a human would do. Also, give your answer very short and dont repeat any past messages. Past messages : {prompt}
        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 900,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        },
        "model_id": "meta-llama/llama-3-3-70b-instruct",
        "project_id": "418fa904-02e8-4a83-8093-918fe3cb13c1",
        "moderations": {
            "hap": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                }
            },
            "pii": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                }
            }
        }
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BEARER_TOKEN}"    
        }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    print(data['results'][0]['generated_text']) 
    return data['results'][0]['generated_text']


    
