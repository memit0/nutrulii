import requests
import json

APP_ID = '3509b3ae'
APP_KEY = '0851e00ec7f9504090bf3c3c2767e5be'
BASE_URL = 'https://api.edamam.com/api'

def get_nutrition_data(ingredient, nutrition_type='cooking', print_output=True):
    """
    Fetch nutrition data for a given ingredient

    Parameters:
    - ingredient (str): The ingredient to fetch nutrition data for
    - nutrition_type (str): Type of nutrition data, cooking or raw
    - print_output (bool): Whether to print the output JSON. 

    Returns:
    - dict: The nutritional data or an error message
    """

    url = f"{BASE_URL}/nutrition-data"
    params = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'nutrition-type': nutrition_type,
        'ingr': ingredient
    }

    # Make a GET request to the API
    response = requests.get(url, params=params)

    if response.status_code == 200:
        # Parse response JSON if request is successful
        data = response.json()
        if print_output:
            # Print formatted JSON with indentation for readability
            print(json.dumps(data, indent=4))
        return data
    else:
        # Return an error message if the API request fails
        error_msg = {'error': f"Failed to retrieve nutrition data: {response.status_code}"}
        if print_output:
            print(json.dumps(error_msg, indent=4))
        return error_msg

def get_nutrition_details(recipe):
    """
    Fetch nutrition data for a given recipe.

    Args:
        recipe (dict): The recipe data, like ingredients and amount, to fetch the nutrition details for

    Returns:
        dict: The detailed nutritional data or an error message.
    """

    url = f"{BASE_URL}/nutrition-details"
    params = {
        'app_id': APP_ID,
        'app_key': APP_KEY
    }

    response = requests.post(url, params=params, json=recipe)

    if response.status_code == 200:
        # Parse response JSON if request is successful
        data = response.json()
        # Print formatted JSON with indentation for readability
        print(json.dumps(data, indent=4))
        return data
    else:
        # Return an error message if the API request fails
        error_msg = {'error': f"Failed to retrieve nutrition details: {response.status_code}"}
        print(json.dumps(error_msg, indent=4))
        return error_msg
