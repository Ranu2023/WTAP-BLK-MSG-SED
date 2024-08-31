import pywhatkit as kit
import datetime
import pyautogui
import time

now = datetime.datetime.now()

current_hour = now.hour
current_minute = now.minute + 1  # Send one minute later


if current_minute >= 60:
    current_minute = 0
    current_hour += 1

   
    if current_hour >= 24:
        current_hour = 0

kit.sendwhatmsg("#which number to send the message", "#what message to send ", current_hour, current_minute)


time.sleep(10)

# Number of times to send the message
repeat_count = 10

try:
    for i in range(repeat_count):
        # Type the message
        pyautogui.typewrite("moj karo ")
        
        # Press 'Enter' to send the message automatically
        pyautogui.press('enter')
        
        print(f"Message {i+1} sent successfully!")

        time.sleep(1)

except Exception as e:
    print(f"An error occurred: {e}")