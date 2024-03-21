import requests
import re

# Define your API key
api_key = 'YOUR API HERE'

# Function to perform OCR using OCR.space API
def ocr_space_file(image_path, api_key, language='eng'):
    payload = {'apikey': api_key,
               'language': language}
    with open(image_path, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={image_path: f},
                          data=payload)
    return r.json()

# Function to extract name, amount, and address from OCR result
def extract_info(ocr_result):
    text = ocr_result['ParsedResults'][0]['ParsedText']
    
    # Extract name
    name = re.search(r'(?i)Welcome to (.+?)\s+Restaurant', text)
    name = name.group(1) if name else None
    
    # Extract amount
    amount_match = re.search(r'\$\d+\.\d{2}', text)
    amount = amount_match.group() if amount_match else None
    
    # Extract address
    address_match = re.search(r'Yim Thai Kitchen(.+?)\sTel', text)
    address = address_match.group(1).strip() if address_match else None
    
    return {'Name': name, 'Amount': amount, 'Address': address}

# Example usage
image_path = 'C:/Users/hp/Documents/arjunpro/bill management system/test OCR/bill3.png'
ocr_result = ocr_space_file(image_path, api_key)
info = extract_info(ocr_result)
print(info)
