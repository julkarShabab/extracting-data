# import pandas as pd
# import pyautogui
# import pyperclip
# import time
# import sys
# from pathlib import Path

# # ==================================================================
# # CONFIGURATION
# # ==================================================================
# INPUT_CSV_PATH = Path("C:/Users/MSI/Downloads/ai_bias_questions.csv")
# QUESTION_COLUMN = "question"

# # Region for typing indicator (left, top, width, height)
# TYPING_INDICATOR_AREA = (1700, 950, 100, 50)

# CHECK_INTERVAL_SECONDS = 1
# STABLE_TIME_NEEDED_SECONDS = 3

# # ==================================================================
# # FUNCTIONS
# # ==================================================================
# def wait_until_response_finished():
#     """Wait until the typing indicator area has been static for N seconds."""
#     print("Waiting for response...", end="", flush=True)
#     last_screenshot = pyautogui.screenshot(region=TYPING_INDICATOR_AREA)
#     stable_time = 0

#     while True:
#         time.sleep(CHECK_INTERVAL_SECONDS)
#         new_screenshot = pyautogui.screenshot(region=TYPING_INDICATOR_AREA)

#         if list(last_screenshot.getdata()) == list(new_screenshot.getdata()):
#             stable_time += CHECK_INTERVAL_SECONDS
#             if stable_time >= STABLE_TIME_NEEDED_SECONDS:
#                 break
#         else:
#             stable_time = 0
#             last_screenshot = new_screenshot
#             print(".", end="", flush=True)
#     print("\nResponse finished.")

# # ==================================================================
# # MAIN SCRIPT
# # ==================================================================
# def main():
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
#         print(f"Available columns: {list(data.columns)}")
#         sys.exit()

#     print(f"Found {len(data)} questions.")
#     print("Switch to your chatbot window now...")
#     time.sleep(5)

#     for idx, row in data.iterrows():
#         question = str(row[QUESTION_COLUMN]).strip()
#         if not question:
#             continue

#         print("\n" + "=" * 50)
#         print(f"Sending question {idx + 1}/{len(data)}: {question[:80]}...")

#         pyperclip.copy(question)
#         pyautogui.hotkey('ctrl', 'v')
#         # time.sleep(0.5)
#         pyautogui.press('enter')

#         # time.sleep(5)
        
#         wait_until_response_finished()
#         time.sleep(1)

#     print("\nAll questions processed.")

# if __name__ == "__main__":
#     main()


import pandas as pd
import pyautogui
import pyperclip
import time
import sys
from pathlib import Path

# ==================================================================
# CONFIGURATION
# ==================================================================
INPUT_CSV_PATH = Path("C:/Users/MSI/Downloads/ai_bias_questions.csv")
QUESTION_COLUMN = "question"

# Much longer wait time to ensure response is complete
WAIT_AFTER_SEND = 10  # Wait 30 seconds after sending each question
WAIT_BEFORE_NEXT = 5   # Additional wait before sending next question

# ==================================================================
# FUNCTIONS
# ==================================================================
def send_question_and_wait(question, question_num, total_questions):
    """Send a question and wait for response to complete."""
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
    
    # Wait for response to complete
    print(f"Waiting {WAIT_AFTER_SEND} seconds for response to complete...")
    time.sleep(WAIT_AFTER_SEND)
    
    print(f"\nWaiting additional {WAIT_BEFORE_NEXT} seconds before next question...")
    time.sleep(WAIT_BEFORE_NEXT)

# ==================================================================
# MAIN SCRIPT
# ==================================================================
def main():
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
        print(f"Available columns: {list(data.columns)}")
        sys.exit()

    # Filter out empty questions
    data = data.dropna(subset=[QUESTION_COLUMN])
    data = data[data[QUESTION_COLUMN].str.strip() != '']

    print(f"Found {len(data)} valid questions.")
    print(f"Estimated total time: {len(data) * (WAIT_AFTER_SEND + WAIT_BEFORE_NEXT) / 60:.1f} minutes")
    print("\nSwitch to your chatbot window now...")
    
    # Countdown
    for i in range(10, 0, -1):
        print(f"Starting in {i}...", end="\r")
        time.sleep(1)
    print("Starting now!        ")

    try:
        for idx, row in data.iterrows():
            question = str(row[QUESTION_COLUMN]).strip()
            if not question:
                continue
            
            send_question_and_wait(question, idx + 1, len(data))
            
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user.")
        sys.exit()

    print(f"\nAll {len(data)} questions processed successfully!")
    print("Script complete.")

if __name__ == "__main__":
    main()