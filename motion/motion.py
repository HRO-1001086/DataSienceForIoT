# CONFIG
pushoverEnabled = False
pushoverClientId = 'YOUR_CLIENT_ID'
pushoverAppToken = 'YOUR_APP_TOKEN'

import RPi.GPIO as GPIO
import time
from pushover import Client

# Pushover is used to send a message to clients
# Set api token and user key
if pushoverEnabled:
  client = Client(pushoverClientId, api_token=pushoverAppToken)

# Set pin variables
PIR_PIN = 4
BUZZER_PIN = 17

loopForMotion = True

# Set pins to correct settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# Password for matrix keypad
correctPin = '1234'
checkPin = ''

# Setup outputs of keypad
rowPins = [26, 19, 13, 6]
colPins = [21, 20, 16, 12]

for i in range(4):
  GPIO.setup(rowPins[i], GPIO.OUT)

for j in range(4):
  GPIO.setup(colPins[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Keypad
keys = [['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']]

print('Home alarm system online')

def main():
  global loopForMotion
  # As long as program is online, loop and search for motion
  while loopForMotion:
    # If PIR sensor triggers output stop the loop and ask for password
    if GPIO.input(PIR_PIN):
      time.sleep(1)
      loopForMotion = False
      motionDetected()



def motionDetected():
  print('Motion detected')
  # Send message to client that motion was detected
  if pushoverEnabled:
    client.send_message("Motion detected inside home", title="Motion detected")
  buzz()
  
  checkForPin()

def buzz():
  # Turn buzzer on
  GPIO.output(BUZZER_PIN, GPIO.HIGH)

def printCharacter(row, character):
  global checkPin
  GPIO.output(row, GPIO.HIGH)

  # Check each column for input
  # If input is detected, add to checkPin
  # If input is #, check pin for correct code
  if GPIO.input(colPins[0]) == 1:
    print(character[0])
    checkPin += character[0]
    while(GPIO.input(colPins[0]) == 1):
      pass
  if GPIO.input(colPins[1]) == 1:
    print(character[1])
    checkPin += character[1]
    while(GPIO.input(colPins[1]) == 1):
      pass
  if GPIO.input(colPins[2]) == 1:
    print(character[2])
    if character[2] == '#':
      checkForPass(checkPin)
    else:
      checkPin += character[2]
      while(GPIO.input(colPins[2]) == 1):
        pass
  if GPIO.input(colPins[3]) == 1:
    print(character[3])
    checkPin += character[3]
    while(GPIO.input(colPins[3]) == 1):
      pass
  GPIO.output(row, GPIO.LOW)

def checkForPin():
  print('Please enter your pin')
  global checkPin
  while True:
    # Check each row for input
    printCharacter(rowPins[0], keys[0])
    printCharacter(rowPins[1], keys[1])
    printCharacter(rowPins[2], keys[2])
    printCharacter(rowPins[3], keys[3])
    time.sleep(0.1)

def checkForPass(code):
  # Check if code is correct
  if(code == correctPin):
    # Turn off all pins and exit program
    print('Welcome home')
    GPIO.cleanup()
    quit()
  else:
    # Reset checkPin
    global checkPin
    print('Wrong code')
    checkPin = ''

try:
  main()
except KeyboardInterrupt:
  # if ctrl+c is pressed, turn off all pins and exit program
  print('Exiting code: KeyboardInterrupt')
  GPIO.cleanup()
  quit()