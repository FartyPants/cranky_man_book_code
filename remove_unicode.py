import json
import os

def clean_text(text):
    """
    Replaces common Unicode "smart" characters with their simpler ASCII equivalents.
    """
    if not isinstance(text, str):
        return text # Return as is if not a string (e.g., None, int, etc.)

    # Define a mapping for Unicode characters to their ASCII equivalents
    # Add more mappings here if you find other unicode characters you want to simplify
    replacements = {
        '\u201c': '"',  # Left double quotation mark
        '\u201d': '"',  # Right double quotation mark
        '\u2019': "'",  # Right single quotation mark / apostrophe
        '\u2018': "'",  # Left single quotation mark
        '\u2026': '...',# Ellipsis
        '\u2014': '--', # Em dash
        '\u2013': '-',  # En dash
        '\xa0': ' ',   # Non-breaking space
        # Add more as needed:
        # '\u00A9': '(c)', # Copyright symbol
        # '\u00AE': '(R)', # Registered trademark symbol
        # '\u2122': '(TM)',# Trademark symbol
        # etc.
    }

    # Create a translation table
    # str.maketrans can take a dictionary mapping unicode characters to replacement strings
    translation_table = str.maketrans(replacements)

    # Apply the translation
    return text.translate(translation_table)

def process_alpaca_dataset(input_filepath, output_filepath):
    """
    Loads an Alpaca-format JSON dataset, cleans the 'instruction' field,
    and saves the modified dataset to a new JSON file.
    """
    processed_data = []

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        print(f"Successfully loaded dataset from {input_filepath}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {input_filepath}. Check file format.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while loading the file: {e}")
        return

    total_items = len(dataset)
    print(f"Processing {total_items} items...")

    for i, item in enumerate(dataset):
        if "instruction" in item:
            original_instruction = item["instruction"]
            cleaned_instruction = clean_text(original_instruction)
            item["instruction"] = cleaned_instruction
        
        processed_data.append(item)

        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{total_items} items...")

    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=4, ensure_ascii=False)
        print(f"\nSuccessfully saved processed dataset to {output_filepath}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

# --- Main execution ---
if __name__ == "__main__":
    # Define your input and output file paths
    # Make sure 'your_dataset.json' exists in the same directory, or provide a full path
    input_file = 'pride_prejudice800.json' # Replace with your actual input file name
    output_file = 'pride_prejudice800_UTF-8.json'

   
    # Process the dataset
    process_alpaca_dataset(input_file, output_file)

    # Optional: Verify the content of the output file
    print("\n--- Verifying a sample from the cleaned file ---")
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            cleaned_sample = json.load(f)[:2] # Load first 2 items to check
            for item in cleaned_sample:
                print(f"Cleaned Instruction: {item['instruction']}")
    except Exception as e:
        print(f"Could not read cleaned file for verification: {e}")