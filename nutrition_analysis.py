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

def list_available_foods():
    """List all available foods stored in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT ingredient FROM nutrition_data')
    rows = cursor.fetchall()
    conn.close()
    if rows:
        print("Available foods in the database:")
        for row in rows:
            print(row[0])
    else:
        print("No foods available in the database.")

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
    table.field_names = ["Nutrient", "Amount Per Serving", "% Daily Value*"]

    essential_nutrients = {
        'ENERC_KCAL': ('Calories', None),
        'FAT': ('Total Fat', 65),
        'FASAT': ('Saturated Fat', 20),
        'TRANSFAT': ('Trans Fat', None),
        'CHOLE': ('Cholesterol', 300),
        'NA': ('Sodium', 2400),
        'CHOCDF': ('Total Carbohydrate', 300),
        'FIBTG': ('Dietary Fiber', 25),
        'SUGAR': ('Total Sugars', None),
        'PROCNT': ('Protein', 50),
        'VITD': ('Vitamin D', 20),
        'CA': ('Calcium', 1300),
        'FE': ('Iron', 18),
        'K': ('Potassium', 4700)
    }

    for nutrient, (label, daily_value) in essential_nutrients.items():
        if nutrient in data['totalNutrients']:
            amount = round(data['totalNutrients'][nutrient]['quantity'], 1)
            unit = data['totalNutrients'][nutrient]['unit']
            daily_value_percent = f"{round((amount / daily_value) * 100)}%" if daily_value else "-"
            table.add_row([label, f"{amount} {unit}", daily_value_percent])

    print("Amount Per Serving")
    print(table)
    print("% Daily Value*")

def main():
    """Main function to run the nutrition analysis program."""
    print("Welcome to Nutriuli!")
    while True:
        

        choice = input("Are you making a recipe or tracking ingredients separately? (r/i): ").lower()
        if choice == 'r':
            recipe_name = input("Enter the name of your recipe: ")
            ingredients = []
            print("Enter ingredients with measurements (e.g., '1 cup of rice', '1 oz of chickpeas'). Type 'done' when finished.")
            while True:
                ingredient = input("Enter an ingredient (or type 'done' to finish): ")
                if ingredient.lower() == 'done':
                    break
                ingredients.append(ingredient)
            if ingredients:
                recipe = {
                    "title": recipe_name,
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

# Initialize the database and prepopulate with some example foods
init_db()

# Run the main function
main()
