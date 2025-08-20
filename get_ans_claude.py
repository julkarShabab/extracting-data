# import pandas as pd
# import pyautogui
# import pyperclip
# import time
# import sys
# from pathlib import Path
# from datetime import datetime

# # ==================================================================
# # CONFIGURATION
# # ==================================================================
# INPUT_CSV_PATH = Path("C:/Users/MSI/Downloads/male_prompts.csv")
# OUTPUT_CSV_PATH = Path("C:/Users/MSI/Downloads/ai_responses_collected.csv")
# QUESTION_COLUMN = "question"

# # Wait times
# WAIT_AFTER_SEND = 10
# WAIT_BEFORE_NEXT = 5

# # Response collection settings
# RESPONSE_AREA = (100, 200, 1400, 600)  # Adjust based on your chat window


# # Alternative: Use None to select entire screen
# # RESPONSE_AREA = None

# # ==================================================================
# # RESPONSE COLLECTION METHODS
# # ==================================================================

# def collect_response_method_1_select_all():
#     """Method 1: Select all text and copy to get the latest response"""
#     print("Collecting response using Select All method...")

#     # Click in chat area to focus
#     pyautogui.click(800, 400)  # Adjust coordinates as needed
#     time.sleep(0.5)

#     # Select all and copy
#     pyautogui.hotkey('ctrl', 'a')
#     time.sleep(0.5)
#     pyautogui.hotkey('ctrl', 'c')
#     time.sleep(0.5)

#     # Get clipboard content
#     try:
#         full_conversation = pyperclip.paste()
#         # You'll need to parse this to extract just the latest response
#         return full_conversation
#     except Exception as e:
#         print(f"Error getting clipboard: {e}")
#         return "ERROR: Could not collect response"


# def collect_response_method_2_triple_click():
#     """Method 2: Triple-click on the response area to select the response"""
#     print("Collecting response using triple-click method...")

#     # Triple-click in the response area to select the paragraph/response
#     response_x, response_y = 800, 500  # Adjust to where responses appear
#     pyautogui.click(response_x, response_y, clicks=3)
#     time.sleep(0.5)

#     # Copy selected text
#     pyautogui.hotkey('ctrl', 'c')
#     time.sleep(0.5)

#     try:
#         response = pyperclip.paste()
#         return response.strip()
#     except Exception as e:
#         print(f"Error getting response: {e}")
#         return "ERROR: Could not collect response"


# def collect_response_method_3_manual_prompt():
#     """Method 3: Prompt user to manually copy the response"""
#     print("\n" + "=" * 50)
#     print("MANUAL COLLECTION MODE")
#     print("Please manually copy the GPT response to clipboard")
#     print("Then press ENTER to continue...")
#     input()

#     try:
#         response = pyperclip.paste()
#         return response.strip()
#     except Exception as e:
#         print(f"Error getting response: {e}")
#         return "ERROR: Could not collect response"


# def collect_response_method_4_screenshot_ocr():
#     """Method 4: Screenshot and OCR (requires pytesseract)"""
#     try:
#         import pytesseract
#         from PIL import Image
#     except ImportError:
#         print("Error: pytesseract and PIL required for OCR method")
#         return "ERROR: OCR libraries not available"

#     print("Collecting response using screenshot OCR...")

#     # Take screenshot of response area
#     if RESPONSE_AREA:
#         screenshot = pyautogui.screenshot(region=RESPONSE_AREA)
#     else:
#         screenshot = pyautogui.screenshot()

#     try:
#         # Use OCR to extract text
#         response = pytesseract.image_to_string(screenshot)
#         return response.strip()
#     except Exception as e:
#         print(f"OCR Error: {e}")
#         return "ERROR: OCR failed"


# # ==================================================================
# # MAIN COLLECTION SCRIPT
# # ==================================================================

# def send_question_and_collect(question, question_num, total_questions, collection_method=1):
#     """Send a question, wait for response, and collect it."""
#     print(f"\nSending question {question_num}/{total_questions}:")
#     print(f"'{question[:100]}...' " if len(question) > 100 else f"'{question}'")

#     # Clear clipboard and copy question
#     pyperclip.copy("")
#     time.sleep(0.3)
#     pyperclip.copy(question)
#     time.sleep(0.3)

#     # Paste and send
#     pyautogui.hotkey('ctrl', 'v')
#     time.sleep(0.5)
#     pyautogui.press('enter')

#     # Wait for response
#     print(f"Waiting {WAIT_AFTER_SEND} seconds for response to complete...")
#     time.sleep(WAIT_AFTER_SEND)

#     # Collect response based on selected method
#     if collection_method == 1:
#         response = collect_response_method_1_select_all()
#     elif collection_method == 2:
#         response = collect_response_method_2_triple_click()
#     elif collection_method == 3:
#         response = collect_response_method_3_manual_prompt()
#     elif collection_method == 4:
#         response = collect_response_method_4_screenshot_ocr()
#     else:
#         response = "ERROR: Invalid collection method"

#     print(f"Response collected (length: {len(response)} chars)")

#     # Wait before next question
#     print(f"Waiting {WAIT_BEFORE_NEXT} seconds before next question...")
#     time.sleep(WAIT_BEFORE_NEXT)

#     return response


# def main():
#     # Choose collection method
#     print("Choose response collection method:")
#     print("1. Select All + Copy (gets full conversation)")
#     print("2. Triple-click + Copy (selects paragraph)")
#     print("3. Manual (you copy each response manually)")
#     print("4. Screenshot + OCR (requires pytesseract)")

#     try:
#         method = int(input("Enter method (1-4): "))
#         if method not in [1, 2, 3, 4]:
#             raise ValueError
#     except (ValueError, KeyboardInterrupt):
#         print("Invalid choice or interrupted. Using method 3 (manual).")
#         method = 3

#     # Load questions
#     try:
#         data = pd.read_csv(INPUT_CSV_PATH, encoding='cp1252')
#     except FileNotFoundError:
#         print(f"[ERROR] File not found: {INPUT_CSV_PATH}")
#         sys.exit()
#     except Exception as e:
#         print(f"[ERROR] Could not read CSV: {e}")
#         sys.exit()

#     if QUESTION_COLUMN not in data.columns:
#         print(f"[ERROR] Column '{QUESTION_COLUMN}' not found in CSV.")
#         sys.exit()

#     # Filter out empty questions
#     data = data.dropna(subset=[QUESTION_COLUMN])
#     data = data[data[QUESTION_COLUMN].str.strip() != '']

#     print(f"Found {len(data)} valid questions.")
#     print("Switch to your chatbot window now...")

#     # Countdown
#     for i in range(10, 0, -1):
#         print(f"Starting in {i}...", end="\r")
#         time.sleep(1)
#     print("Starting now!        ")

#     # Prepare results storage
#     results = []

#     try:
#         for idx, row in data.iterrows():
#             question = str(row[QUESTION_COLUMN]).strip()
#             if not question:
#                 continue

#             response = send_question_and_collect(question, idx + 1, len(data), method)

#             # Get category from the CSV (if it exists)
#             category = row.get('Category', 'Unknown Category')

#             # Store result
#             result_row = {
#                 'question_id': idx + 1,
#                 'category': category,
#                 'question': question,
#                 'response': response,
#                 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#                 'method_used': method
#             }
#             results.append(result_row)

#             # Save after each question (in case of interruption)
#             results_df = pd.DataFrame(results)
#             results_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
#             print(f"Progress saved to {OUTPUT_CSV_PATH}")

#     except KeyboardInterrupt:
#         print("\n\nScript interrupted by user.")

#     # Final save
#     if results:
#         results_df = pd.DataFrame(results)
#         results_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
#         print(f"\nFinal results saved to {OUTPUT_CSV_PATH}")
#         print(f"Collected {len(results)} responses successfully!")
#     else:
#         print("No responses collected.")


# if __name__ == "__main__":
#     main()


import pandas as pd
import pyautogui
import pyperclip
import time
import sys
from pathlib import Path
from datetime import datetime

# ==================================================================
# CONFIGURATION
# ==================================================================
INPUT_CSV_PATH = Path("C:/Users/MSI/Downloads/female_prompts - copy.csv")
OUTPUT_CSV_PATH = Path("C:/Users/MSI/Downloads/ai_responses_collected_extras.csv")
QUESTION_COLUMN = "question"

# Wait times
WAIT_AFTER_SEND = 10
WAIT_BEFORE_NEXT = 5

# Response collection settings
RESPONSE_AREA = (100, 200, 1400, 600)  # Adjust based on your chat window


# Alternative: Use None to select entire screen
# RESPONSE_AREA = None

# ==================================================================
# RESPONSE COLLECTION METHODS
# ==================================================================

def collect_response_method_1_select_all():
    """Method 1: Select all text and copy to get the latest response"""
    print("Collecting response using Select All method...")

    # Click in chat area to focus
    pyautogui.click(800, 400)  # Adjust coordinates as needed
    time.sleep(0.5)

    # Select all and copy
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)

    # Get clipboard content
    try:
        full_conversation = pyperclip.paste()
        # You'll need to parse this to extract just the latest response
        return full_conversation
    except Exception as e:
        print(f"Error getting clipboard: {e}")
        return "ERROR: Could not collect response"


def collect_response_method_2_triple_click():
    """Method 2: Triple-click on the response area to select the response"""
    print("Collecting response using triple-click method...")

    # Triple-click in the response area to select the paragraph/response
    response_x, response_y = 800, 500  # Adjust to where responses appear
    pyautogui.click(response_x, response_y, clicks=3)
    time.sleep(0.5)

    # Copy selected text
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)

    try:
        response = pyperclip.paste()
        return response.strip()
    except Exception as e:
        print(f"Error getting response: {e}")
        return "ERROR: Could not collect response"


def collect_response_method_3_manual_prompt():
    """Method 3: Prompt user to manually copy the response"""
    print("\n" + "=" * 50)
    print("MANUAL COLLECTION MODE")
    print("Please manually copy the GPT response to clipboard")
    print("Then press ENTER to continue...")
    input()

    try:
        response = pyperclip.paste()
        return response.strip()
    except Exception as e:
        print(f"Error getting response: {e}")
        return "ERROR: Could not collect response"


def collect_response_method_4_screenshot_ocr():
    """Method 4: Screenshot and OCR (requires pytesseract)"""
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        print("Error: pytesseract and PIL required for OCR method")
        return "ERROR: OCR libraries not available"

    print("Collecting response using screenshot OCR...")

    # Take screenshot of response area
    if RESPONSE_AREA:
        screenshot = pyautogui.screenshot(region=RESPONSE_AREA)
    else:
        screenshot = pyautogui.screenshot()

    try:
        # Use OCR to extract text
        response = pytesseract.image_to_string(screenshot)
        return response.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return "ERROR: OCR failed"


# ==================================================================
# MAIN COLLECTION SCRIPT
# ==================================================================

def send_question_and_collect(question, question_num, total_questions, collection_method=1):
    """Send a question, wait for response, and collect it."""
    print(f"\nSending question {question_num}/{total_questions}:")
    print(f"'{question[:100]}...' " if len(question) > 100 else f"'{question}'")

    # Clear clipboard and copy question
    pyperclip.copy("")
    time.sleep(0.3)
    pyperclip.copy(question)
    time.sleep(0.3)

    # Paste and send
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')

    # Wait for response
    print(f"Waiting {WAIT_AFTER_SEND} seconds for response to complete...")
    time.sleep(WAIT_AFTER_SEND)

    # Collect response based on selected method
    if collection_method == 1:
        response = collect_response_method_1_select_all()
    elif collection_method == 2:
        response = collect_response_method_2_triple_click()
    elif collection_method == 3:
        response = collect_response_method_3_manual_prompt()
    elif collection_method == 4:
        response = collect_response_method_4_screenshot_ocr()
    else:
        response = "ERROR: Invalid collection method"

    print(f"Response collected (length: {len(response)} chars)")

    # Wait before next question
    print(f"Waiting {WAIT_BEFORE_NEXT} seconds before next question...")
    time.sleep(WAIT_BEFORE_NEXT)

    return response


def main():
    # Choose collection method
    print("Choose response collection method:")
    print("1. Select All + Copy (gets full conversation)")
    print("2. Triple-click + Copy (selects paragraph)")
    print("3. Manual (you copy each response manually)")
    print("4. Screenshot + OCR (requires pytesseract)")

    try:
        method = int(input("Enter method (1-4): "))
        if method not in [1, 2, 3, 4]:
            raise ValueError
    except (ValueError, KeyboardInterrupt):
        print("Invalid choice or interrupted. Using method 3 (manual).")
        method = 3

    # Load questions
    try:
        data = pd.read_csv(INPUT_CSV_PATH, encoding='cp1252')
    except FileNotFoundError:
        print(f"[ERROR] File not found: {INPUT_CSV_PATH}")
        sys.exit()
    except Exception as e:
        print(f"[ERROR] Could not read CSV: {e}")
        sys.exit()

    if QUESTION_COLUMN not in data.columns:
        print(f"[ERROR] Column '{QUESTION_COLUMN}' not found in CSV.")
        sys.exit()

    # Filter out empty questions
    data = data.dropna(subset=[QUESTION_COLUMN])
    data = data[data[QUESTION_COLUMN].str.strip() != '']

    print(f"Found {len(data)} valid questions.")
    print("Switch to your chatbot window now...")

    # Countdown
    for i in range(10, 0, -1):
        print(f"Starting in {i}...", end="\r")
        time.sleep(1)
    print("Starting now!        ")

    # Prepare results storage
    results = []

    try:
        for idx, row in data.iterrows():
            question = str(row[QUESTION_COLUMN]).strip()
            if not question:
                continue

            response = send_question_and_collect(question, idx + 1, len(data), method)

            # Get category from the CSV (if it exists)
            category = row.get('Category', 'Unknown Category')

            # Store result
            result_row = {
                'question_id': idx + 1,
                'category': category,
                'question': question,
                'response': response,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'method_used': method
            }
            results.append(result_row)

            # Save after each question (in case of interruption)
            results_df = pd.DataFrame(results)
            results_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
            print(f"Progress saved to {OUTPUT_CSV_PATH}")

    except KeyboardInterrupt:
        print("\n\nScript interrupted by user.")

    # Final save
    if results:
        results_df = pd.DataFrame(results)
        results_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
        print(f"\nFinal results saved to {OUTPUT_CSV_PATH}")
        print(f"Collected {len(results)} responses successfully!")
    else:
        print("No responses collected.")


if __name__ == "__main__":
    main()