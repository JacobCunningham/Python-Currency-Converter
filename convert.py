import validator
from currency import Currency
from converter import Converter


input_valid = False
converter = Converter("usd")

while not input_valid:

    try:
        input_amount = float(input("Please enter orignal amount: "))
    except ValueError:
        print("Invalid amount selection, please only use numbers.")
        continue

    input_currency_code = input("Please enter original currency code: ").upper()
    input_to_currency = input("Please enter currency code to convert to: ").upper()

    if validator.input_is_valid(input_amount, input_currency_code, input_to_currency):
        input_valid = True
    else:
        print("Invalid currency selection, please use a valid currency code.")

input_currency = Currency(input_amount, input_currency_code)

output_currency = converter.convert_to(input_currency, input_to_currency)

print(f"{input_amount} {input_currency_code.upper()} is {output_currency.amount} {output_currency.type.upper()}")