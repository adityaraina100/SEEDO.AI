import requests
import re

# Define your OCR.space API key
api_key = 'K85581677688957'

# Function to perform OCR using OCR.space API
def ocr_space_file(image_path, api_key, language='eng'):
    payload = {'apikey': api_key,
               'language': language}
    with open(image_path, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={image_path: f},
                          data=payload)
    return r.json()

# Function to extract specific fields including bill items and amounts from OCR result
def extract_info_from_ocr(ocr_result):
    extracted_info = {}
    parsed_text = ocr_result.get('ParsedResults', [])
    if parsed_text:
        parsed_text = parsed_text[0]['ParsedText']
        lines = parsed_text.split('\n')
        bill_items = {}
        in_bill_items = False
        for line in lines:
            if line.startswith('Student Name:'):
                extracted_info['Name'] = line.split(':')[1].strip()
            elif line.startswith('Receipt No.:'):
                extracted_info['Receipt No.'] = line.split(':')[1].strip()
            elif line.startswith('Date & Time:'):
                extracted_info['Date & Time'] = line.split(':')[1].strip()
            elif line.startswith('Admission No.:'):
                extracted_info['Admission No.'] = line.split(':')[1].strip()
            elif 'Bill Item' in line:  # Modified to detect the start of bill items
                # Reached the start of bill items section
                in_bill_items = True
            elif in_bill_items:
                # Inside the bill items section
                match = re.match(r'(.+)\s+(\d+,\d+\.\d{2})', line)
                if match:
                    item, amount = match.groups()
                    bill_items[item.strip()] = amount.strip()
            elif 'Total' in line:  # Modified to detect the end of bill items
                # Reached the end of bill items section
                break
        extracted_info['Bill Items'] = bill_items
    return extracted_info

# Example usage for testing
def test_ocr():
    image_path = 'C:/Users/hp/Documents/arjunpro/bill management system/test OCR/Arjun Fee.jpg'  # Replace with the path to your sample image
    ocr_result = ocr_space_file(image_path, api_key)
    if ocr_result.get('ParsedResults'):
        print("Text extracted successfully:")
        extracted_info = extract_info_from_ocr(ocr_result)
        for key, value in extracted_info.items():
            print(f"{key}: {value}")
    else:
        print("Failed to extract text from the image.")

# Call the testing function
test_ocr()
