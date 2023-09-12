from datetime import datetime
from time import sleep
import json
import random

# List of valid credit card number prefixes
prefixes = ['4', '51', '52', '53', '54', '55', '34', '37', '6011', '30', '36', '38', '3528', '3589']

# Range of valid credit card lengths
length_range = (13, 19)

# List to store generated credit card information
credit_card_info = []

# Calculate the current year, considering only the last two digits
current_year = datetime.now().year - 2000

# Define the range of valid expiration years (from current year + 1 to current year + 6)
expiration_range = (current_year + 1, current_year + 6)


def is_valid_credit_card(card_number):
    card_number = card_number.replace(" ", "").replace("-", "")

    # Check if the card number is numeric and within the valid length range
    if not card_number.isdigit() or not length_range[0] <= len(card_number) <= length_range[1]:
        return False

    total = 0
    reverse_digits = [int(digit) for digit in card_number[::-1]]
    double_digit = False

    for n in reverse_digits:
        if double_digit:
            n *= 2
            if n > 9:
                n -= 9
            double_digit = False
        else:
            double_digit = True

        total += n

    return total % 10 == 0


def get_card_type(card_number):
    card_schemes = {
        'Visa': ['4'],
        'MasterCard': ['51', '52', '53', '54', '55'],
        'American Express': ['34', '37'],
        'Discover': ['6011'],
        'Diners Club': ['30', '36', '38'],
        'JCB': ['3528', '3589'],
    }

    card_number = card_number.replace(" ", "").replace("-", "")

    if not is_valid_credit_card(card_number):
        return 'Invalid'

    for card_type, iin_ranges in card_schemes.items():
        for iin in iin_ranges:
            if card_number.startswith(iin):
                return card_type

    return 'Unknown'


def gen_cc():
    prefix = random.choice(prefixes)
    remaining_length = random.randint(length_range[0] - len(prefix), length_range[1] - len(prefix))

    number = prefix + ''.join(str(random.randint(0, 9)) for _ in range(remaining_length - 1))

    reversed_digits = [int(digit) for digit in reversed(number)]
    for i in range(1, len(reversed_digits), 2):
        reversed_digits[i] *= 2
        reversed_digits[i] = reversed_digits[i] - 9 if reversed_digits[i] > 9 else reversed_digits[i]

    total = sum(reversed_digits)
    final_digit = (10 - (total % 10)) % 10
    number += str(final_digit)

    cvv_gen = random.randint(100, 9999)

    random_month = random.randint(1, 12)
    random_year = random.randint(*expiration_range)

    exp_date = f"{random_month:02}/{random_year:02}"

    return number, cvv_gen, exp_date


def gen_loop(loops):
    while loops > 0:
        card_number, cvv, expiration_date = gen_cc()

        if is_valid_credit_card(card_number):
            card_type = get_card_type(card_number)
            print(f"-[VALID]{card_type}: {card_number} {cvv} {expiration_date}")

            card_info = {
                "Card Type": card_type,
                "Card Number": card_number,
                "CVV": cvv,
                "Expiration Date": expiration_date
            }
            credit_card_info.append(card_info)

            loops -= 1
            sleep(delay)

        else:
            print(f"[INVALID] {card_number} {cvv} {expiration_date}")


if __name__ == '__main__':
    print("Welcome to CC Generator! By Smoodie")
    performance_mode = int(input("Choose a performance mode:\n1-Ultra, 2-High, 3-Balanced, 4-Medium, 5-Low\n>"))
    delay = performance_mode / 1000.0

    num_valid_cards = int(input("How many valid credit cards do you want to generate?\n>"))

    gen_loop(num_valid_cards)

    print("\nGeneration ended successfully:")
    formatted_credit_card_info = json.dumps(credit_card_info, indent=4)
    print(formatted_credit_card_info)

    # Save credit cards as JSON file
    if input("Save as JSON file? (Y/N)").lower() == 'y':
        file_name = input("Enter the file name (e.g., credit_cards.json): ")

        # Add .json extension if not provided by the user
        if not file_name.endswith(".json"):
            file_name += ".json"

        try:
            # Open the file for writing and save the JSON data
            with open(file_name, "w") as json_file:
                json_file.write(formatted_credit_card_info)
            print(f"Data saved to {file_name}")
        except Exception as e:
            input(f"An error occurred while saving the JSON file: {e}")
