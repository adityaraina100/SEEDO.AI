import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to perform OCR
def perform_ocr():
    global image_path
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ocr_text = pytesseract.image_to_string(gray)
    parsed_info = parse_ocr_text(ocr_text)
    show_ocr_result(parsed_info)

# Function to parse OCR text
def parse_ocr_text(ocr_text):
    # Here, you can write your own logic to parse the OCR text into different sections or fields
    # For example, you can use regular expressions to extract specific patterns or keywords
    
    parsed_info = {
        "Customer Name": "John Doe",
        "Address": "123 Main Street",
        "Phone Number": "555-1234",
        "Date": "2024-03-15",
        # Add more fields as needed
    }
    
    return parsed_info

# Function to open file dialog and select image
def open_file_dialog():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if image_path:
        load_image(image_path)

# Function to load and display image in GUI
def load_image(path):
    image = Image.open(path)
    image.thumbnail((400, 400))
    photo = ImageTk.PhotoImage(image)
    img_label.config(image=photo)
    img_label.image = photo

# Function to display parsed OCR result in a dialog box with colorful boxes
def show_ocr_result(parsed_info):
    result_dialog = tk.Toplevel(root)
    result_dialog.title("OCR Result")

    # Colors for the boxes
    colors = ["#1abc9c", "#3498db", "#9b59b6", "#e74c3c", "#f1c40f"]

    # Display parsed info in different colorful boxes
    for i, (key, value) in enumerate(parsed_info.items()):
        color = colors[i % len(colors)]
        
        frame = tk.Frame(result_dialog, bg=color, padx=10, pady=5)
        frame.pack(fill=tk.X)
        
        label_key = tk.Label(frame, text=key + ":", font=("Arial", 12, "bold"), bg=color, fg="white")
        label_key.pack(side=tk.LEFT)
        
        label_value = tk.Label(frame, text=value, font=("Arial", 12), bg=color, fg="white")
        label_value.pack(side=tk.RIGHT)

# Create GUI window
root = tk.Tk()
root.title("OCR GUI")
root.configure(bg="#f0f0f0")

# Create widgets
open_button = tk.Button(root, text="Open Image", command=open_file_dialog, bg="#3c8dbc", fg="white", font=("Arial", 12))
open_button.pack(pady=10)

img_label = tk.Label(root)
img_label.pack()

perform_button = tk.Button(root, text="Perform OCR", command=perform_ocr, bg="#3c8dbc", fg="white", font=("Arial", 12))
perform_button.pack(pady=10)

# Run the GUI
root.mainloop()
