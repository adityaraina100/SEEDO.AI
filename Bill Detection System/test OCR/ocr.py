import requests
import re

# Define your OCR.space API key
api_key = 'YOUR_API_KEY'

# Function to perform OCR using OCR.space API
def ocr_space_file(image_path, api_key, language='eng'):
    payload = {'apikey': api_key,
               'language': language}
    with open(image_path, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={image_path: f},
                          data=payload)
    return r.json()

# Function to extract required fields from OCR result
def extract_info(ocr_result):
    text = ocr_result['ParsedResults'][0]['ParsedText']
    
    # Extract Student Name
    name_match = re.search(r'Student Name:\s*([^\n]+)', text)
    name = name_match.group(1).strip() if name_match else None
    
    # Extract Receipt No.
    receipt_match = re.search(r'Receipt No.:\s*([^\n]+)', text)
    receipt = receipt_match.group(1).strip() if receipt_match else None
    
    # Extract Admission No.
    admission_match = re.search(r'Admission No.:\s*([^\n]+)', text)
    admission = admission_match.group(1).strip() if admission_match else None
    
    # Extract Date & Time
    datetime_match = re.search(r'Date & Time:\s*([^\n]+)', text)
    datetime = datetime_match.group(1).strip() if datetime_match else None
    
    # Extract Total
    total_match = re.search(r'Total\s*:?\s*([0-9,.]+)', text)
    total = total_match.group(1).strip() if total_match else None
    
    # Remove 'Ref No.' if it's not found
    ref_no = None
    if 'Ref No.:' in text:
        ref_no_match = re.search(r'Ref No.:\s*([^\n]+)', text)
        ref_no = ref_no_match.group(1).strip() if ref_no_match else None
    
    return {'Student Name': name, 'Receipt No.': receipt, 'Admission No.': admission, 'Date&Time': datetime, 'Total': total, 'Ref No.': ref_no}

# Example usage
image_path = 'C:/Users/hp/Documents/arjunpro/bill management system/test OCR/Arjun Fee.jpg'
ocr_result = ocr_space_file(image_path, api_key)
info = extract_info(ocr_result)
print(info)
