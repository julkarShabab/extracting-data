# import pyautogui
# import pytesseract
# from PIL import Image
# from transformers import pipeline

# # =========================
# # 1️⃣ SCREEN CAPTURE
# # =========================

# # Take a screenshot of a specific region (x, y, width, height)
# # Adjust these coordinates for your screen
# region_screenshot = pyautogui.screenshot(region=(100, 200, 500, 300))
# region_screenshot.save("capture.png")
# print("[INFO] Screenshot saved as 'capture.png'.")

# # =========================
# # 2️⃣ OCR TEXT EXTRACTION
# # =========================

# # Path to Tesseract executable (change if installed elsewhere)
# # Example for Windows:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # Extract text from screenshot
# text = pytesseract.image_to_string(Image.open("capture.png"))
# print("[INFO] Extracted text:")
# print(text)

# # =========================
# # 3️⃣ TEXT SUMMARIZATION
# # =========================

# if text.strip():
#     summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#     summary = summarizer(text, max_length=50, min_length=20, do_sample=False)
#     print("[INFO] Summary:")
#     print(summary[0]['summary_text'])
# else:
#     print("[WARNING] No text detected in the screenshot.")

import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


# import pyautogui
# import pytesseract
# from PIL import Image
# import time

# # =========================
# # 0️⃣ PREPARATION MESSAGE
# # =========================

# #pyautogui.alert("You have 5 seconds to switch to your preferred window. Get ready!")
# print("you have  5 seconds")
# time.sleep(5)  # wait 5 seconds

# # =========================
# # 1️⃣ SCREEN CAPTURE
# # =========================

# region_screenshot = pyautogui.screenshot(region=(100, 200, 500, 300))
# region_screenshot.save("capture.png")
# print("[INFO] Screenshot saved as 'capture.png'.")

# # =========================
# # 2️⃣ OCR TEXT EXTRACTION
# # =========================

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# text = pytesseract.image_to_string(Image.open("capture.png"))
# print("[INFO] Extracted text:")
# print(text)

import pyautogui
from PIL import ImageGrab
import pytesseract
import time
import csv
import os

# Alert user and trigger snip tool
#pyautogui.alert("You have 5 seconds to get ready to snip. After that, the snip tool will open.")
time.sleep(5)
pyautogui.hotkey('winleft', 'shift', 's')
print("[INFO] Please select area to snip. Waiting for clipboard...")

# Wait for image in clipboard
timeout = 30
start_time = time.time()
image = None
while (time.time() - start_time) < timeout:
    image = ImageGrab.grabclipboard()
    if isinstance(image, ImageGrab.Image.Image):
        break
    time.sleep(1)

if image is None:
    print("[ERROR] No image found in clipboard within 30 seconds.")
else:
    image.save("snip_capture.png")
    print("[INFO] Screenshot saved as 'snip_capture.png'.")

    # OCR extraction
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    # ... after OCR extraction
text = pytesseract.image_to_string(image)

print("[INFO] Extracted text:")
print(text)

clean_text = text.strip().replace('\n', ' ').replace('\r', ' ')

csv_filename = "extracted_texts.csv"
file_exists = os.path.isfile(csv_filename)

with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    if not file_exists:
        writer.writerow(["Timestamp", "Extracted Text"])
    writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), clean_text])

print(f"[INFO] Extracted text saved to '{csv_filename}'.")
