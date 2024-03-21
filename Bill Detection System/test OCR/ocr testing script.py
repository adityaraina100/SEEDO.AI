import requests

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

# Example usage for testing
def test_ocr():
    image_path = 'C:/Users/hp/Documents/arjunpro/bill management system/test OCR/Arjun Fee.jpg'  # Replace with the path to your sample image
    ocr_result = ocr_space_file(image_path, api_key)
    if ocr_result.get('ParsedResults'):
        print("Text extracted successfully:")
        print(ocr_result['ParsedResults'][0]['ParsedText'])
    else:
        print("Failed to extract text from the image.")

# Call the testing function
test_ocr()
