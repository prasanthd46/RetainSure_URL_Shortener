# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need



import random
import string
import re

def generate_short_code(existing_codes, length=6):
    
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if code not in existing_codes:
            return code

def validate_url(url):
    pattern = re.compile(
        r'^(https?://)'                
        r'([a-zA-Z0-9-]+\.)+'          
        r'([a-zA-Z]{2,})'              
        r'([:/?#][^\s]*)?$',           
        re.IGNORECASE
    )
     
    return bool(pattern.match(url))
