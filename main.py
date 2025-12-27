import google.generativeai as genai
import yaml
import time
import json
import sys

try:

    # load config

    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    if not config:
        raise ValueError("config.yaml is empty")

    if 'GOOGLE_API_KEY' not in config:
        raise KeyError("GOOGLE_API_KEY not found in config.yaml")

    GOOGLE_API_KEY = config['GOOGLE_API_KEY']
    genai.configure(api_key=GOOGLE_API_KEY)

    print("Setup completed! API key loaded.\n")

    # initialize model

    start_time = time.time()

    print("--- Initializing model ---\n")

    model = genai.GenerativeModel('gemini-2.5-flash')

    # user input

    quantity = input("Enter how many records you want to generate: ")
    fields = input("Enter required fields (e.g. name, age, email): ")

    # validate quantity

    try:
        quantity = int(quantity)
    except ValueError:
        print("Error: quantity must be an integer")
        sys.exit(1)

    # strict prompt

    prompt_json = f"""You are a test data generator.
    Generate EXACTLY {quantity} JSON objects.
    Use ONLY the following fields: {fields}.
    Do not create extra fields.
    Do not explain anything.
    Do not use markdown.
    The response MUST be a valid JSON array."""

    print("\nRequesting JSON data...\n")
    response = model.generate_content(prompt_json)

    # Clean response

    cleaned_text = (
        response.text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    # Validate JSON

    try:
        data = json.loads(cleaned_text)
    except json.JSONDecodeError:
        print("Error: the AI did not return valid JSON.\n")
        print(cleaned_text)
        sys.exit(1)

    # validate structure

    if not isinstance(data, list):
        print("Error: the returned JSON is not an array.")
        sys.exit(1)
    
    end_time = time.time()

    # output

    print(cleaned_text)
    print(f"\nTotal records generated: {len(data)}.")
    print(f"Generation time: {end_time - start_time:.2f} seconds.")

except FileNotFoundError as e:
    print(f"File error: {e}")

except (KeyError, ValueError) as e:
    print(f"Config error: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")