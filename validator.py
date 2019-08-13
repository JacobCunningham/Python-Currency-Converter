import re
from urllib import request
import urllib

currency_code_pattern = re.compile("^[a-zA-Z]{1,25}$")

def input_is_valid(input_amount, input_code, input_to_code):
    if not isinstance(input_amount,float):
        return False
    
    if currency_code_pattern.match(input_code):
        try:
            response =  request.urlopen(f"https://api.exchangeratesapi.io/latest?symbols={input_code},{input_to_code}")
        except urllib.error.URLError:
            return False
        if response.status == 200:
            return True
    else: return False

