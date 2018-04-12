import requests
import json


base_url = "https://www.potterapi.com/v1/"
hp_api_key = "$2a$10$XPnZrHnIYgf.R9etCbM/8eHqwCnygF9MlSVbcVA4wDlPsIZpwsZa2"

params = {"key":hp_api_key,"name": "Harry Potter"}

response = requests.get(base_url+"characters",params=params)
hp_list = json.loads(response.text) 

print(response.text)