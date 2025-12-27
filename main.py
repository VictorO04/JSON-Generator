import google.generativeai as genai
import yaml
import time
import json
import sys

def load_config():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    if not config:
        raise ValueError("config.yaml is empty")

    if 'GOOGLE_API_KEY' not in config:
        raise KeyError("GOOGLE_API_KEY not found in config.yaml")

    return config['GOOGLE_API_KEY']

def init_model(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

def get_user_input():
    quantity = input("Enter how many records you want to generate: ")
    fields = input("Enter required fields (e.g. name, age, email): ")

    try:
        quantity = int(quantity)
    except ValueError:
        raise ValueError("quantity must be an integer")
    
    fields = ", ".join(f.strip() for f in fields.split(","))

    return quantity, fields

def build_prompt(quantity, fields):
    return f"""You are a test data generator.
    Generate EXACTLY {quantity} JSON objects.
    Use ONLY the following fields: {fields}.
    Do not create extra fields.
    Do not explain anything.
    Do not use markdown.
    The response MUST be a valid JSON array.
    """

def generate_json(model, prompt):
    response = model.generate_content(prompt)

    cleaned_text = (
        response.text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        data = json.loads(cleaned_text)
    except json.JSONDecodeError:
        raise ValueError("AI did not return valid JSON")

    if not isinstance(data, list):
        raise ValueError("Returned JSON is not an array")

    return data, cleaned_text

def main():
    start_time = time.time()

    api_key = load_config()
    print("Setup completed! API key loaded.\n")

    print("--- Initializing model ---\n")
    model = init_model(api_key)

    quantity, fields = get_user_input()

    prompt = build_prompt(quantity, fields)

    print("\nRequesting JSON data...\n")

    data, raw_json = generate_json(model, prompt)

    end_time = time.time()

    print(raw_json)
    print(f"\nTotal records generated: {len(data)}.")
    print(f"Generation time: {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print(f"File error: {e}")

    except (KeyError, ValueError) as e:
        print(f"Config error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")