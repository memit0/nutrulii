import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the variables
app_key = os.getenv('APP_KEY')
app_id = os.getenv('APP_ID')

def get_nutrition(ingredient):
    url = "https://api.edamam.com/api/nutrition-data"
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'ingr': ingredient
    }
    response = requests.get(url, params=params)
    print(response.status_code)
    print(response.text)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

if __name__ == "__main__":
    ingredient = "1 large apple"
    nutrition_data = get_nutrition(ingredient)
    if nutrition_data:
        print(nutrition_data)
    else:
        print("Failed to retrieve nutrition data.")
