import requests
import json

APP_ID = '3509b3ae'
APP_KEY = '0851e00ec7f9504090bf3c3c2767e5be'
BASE_URL = 'https://api.edamam.com/api'

def get_nutrition_data(ingredient, nutrition_type='cooking'):
    url = f"{BASE_URL}/nutrition-data"
    params = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'nutrition-type': nutrition_type,
        'ingr': ingredient
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f"Failed to retrieve nutrition data: {response.status_code}"}

def get_nutrition_details(recipe):
    url = f"{BASE_URL}/nutrition-details"
    params = {
        'app_id': APP_ID,
        'app_key': APP_KEY
    }
    response = requests.post(url, params=params, json=recipe)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f"Failed to retrieve nutrition details: {response.status_code}"}
