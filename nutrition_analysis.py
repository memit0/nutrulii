import requests
import json
import sqlite3
from prettytable import PrettyTable

APP_KEY = '0851e00ec7f9504090bf3c3c2767e5be'
APP_ID = '3509b3ae'
BASE_URL = 'https://api.edamam.com/api'
DB_NAME = 'nutrition.db'

def init_db():
    """Initialize the database and create tables if they do not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS nutrition_data (
                        id INTEGER PRIMARY KEY,
                        ingredient TEXT NOT NULL,
                        nutrition_data TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def store_nutrition_data(ingredient, data):
    """Store nutrition data in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO nutrition_data (ingredient, nutrition_data) VALUES (?, ?)', 
                   (ingredient, json.dumps(data)))
    conn.commit()
    conn.close()

def get_stored_nutrition_data(ingredient):
    """Retrieve stored nutrition data from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT nutrition_data FROM nutrition_data WHERE ingredient = ?', (ingredient,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

def get_nutrition_data(ingredient, nutrition_type='cooking', print_output=True):
    """Fetch nutrition data for a given ingredient."""
    stored_data = get_stored_nutrition_data(ingredient)
    if stored_data:
        if print_output:
            display_nutrition_data(stored_data)
        return stored_data

    url = f"{BASE_URL}/nutrition-data"
    params = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'nutrition-type': nutrition_type,
        'ingr': ingredient
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        store_nutrition_data(ingredient, data)
        if print_output:
            display_nutrition_data(data)
        return data
    else:
        error_msg = {'error': f"Failed to retrieve nutrition data: {response.status_code}"}
        if print_output:
            print(json.dumps(error_msg, indent=4))
        return error_msg

def get_nutrition_details(recipe):
    """Fetch nutrition data for a given recipe."""
    url = f"{BASE_URL}/nutrition-details"
    params = {
        'app_id': APP_ID,
        'app_key': APP_KEY
    }

    response = requests.post(url, params=params, json=recipe)

    if response.status_code == 200:
        data = response.json()
        display_nutrition_data(data)
        return data
    else:
        error_msg = {'error': f"Failed to retrieve nutrition details: {response.status_code}"}
        print(json.dumps(error_msg, indent=4))
        return error_msg

def display_nutrition_data(data):
    """Display the nutrition data in a formatted table."""
    table = PrettyTable()
    table.field_names = ["Nutrient", "Quantity", "Unit"]

    essential_nutrients = [
        'ENERC_KCAL', 'FAT', 'FASAT', 'CHOCDF', 'FIBTG', 'SUGAR', 'PROCNT', 'NA'
    ]

    for nutrient in essential_nutrients:
        if nutrient in data['totalNutrients']:
            table.add_row([
                data['totalNutrients'][nutrient]['label'],
                round(data['totalNutrients'][nutrient]['quantity'], 2),
                data['totalNutrients'][nutrient]['unit']
            ])

    print(table)

def main():
    """Main function to run the nutrition analysis program."""
    print("Welcome to Nutriuli!")
    while True:
        choice = input("Are you making a recipe or tracking ingredients separately? (r/i): ").lower()
        if choice == 'r':
            ingredients = []
            print("Enter ingredients with measurements (e.g., '1 cup of rice', '1 oz of chickpeas'). Type 'done' when finished.")
            while True:
                ingredient = input("Enter an ingredient (or type 'done' to finish): ")
                if ingredient.lower() == 'done':
                    break
                ingredients.append(ingredient)
            if ingredients:
                recipe = {
                    "title": "User Recipe",
                    "ingr": ingredients
                }
                get_nutrition_details(recipe)
        elif choice == 'i':
            ingredient = input("Enter an ingredient with measurement (e.g., '1 apple'): ")
            get_nutrition_data(ingredient)
        else:
            print("Invalid choice. Please select 'r' for recipe or 'i' for individual ingredients.")

        continue_choice = input("Do you want to continue? (yes/no): ").lower()
        if continue_choice != 'yes':
            break

# Initialize the database
init_db()

# Run the main function
main()
