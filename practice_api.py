import requests
import json

def get_hp_data(char_name):
	base_url = "https://www.potterapi.com/v1/"
	hp_api_key = "$2a$10$XPnZrHnIYgf.R9etCbM/8eHqwCnygF9MlSVbcVA4wDlPsIZpwsZa2"

	params = {"key":hp_api_key,"name": char_name}

	response = requests.get(base_url+"characters",params=params)
	hp_list = json.loads(response.text) 

	return response.text

print(get_hp_data("Harry Potter"))
print(get_hp_data("Hermione Granger"))
