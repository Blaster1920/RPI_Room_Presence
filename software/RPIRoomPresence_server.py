import time, datetime
import RPi.GPIO as GPIO
import telepot
from telepot.loop import MessageLoop

PIN_TRIGGER = 7
PIN_ECHO = 11

GPIO.setmode(GPIO.BOARD)

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print ('Received: %s' % command)

    if 'distance' in command:
        message = "The distance is currently "
        message = message + str(distance())
        telegram_bot.sendMessage (chat_id, message)

def distance():
     GPIO.output(PIN_TRIGGER, GPIO.LOW)
     time.sleep(0.7)
     GPIO.output(PIN_TRIGGER, GPIO.HIGH)
     time.sleep(0.00001)
     GPIO.output(PIN_TRIGGER, GPIO.LOW)
     while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
     while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()
     pulse_duration = pulse_end_time - pulse_start_time
     calculated_distance = round(pulse_duration * 17150, 2)
     return calculated_distance
     
def presence(id):
    presence_flag=0
    if distance() < 110:
        message = "*THE ROOM IS CURRENTLY BEING USED* " + str(datetime.datetime.now())
        telegram_bot.sendMessage (id, message)
        presence_flag=1
        time.sleep(10)
    while presence_flag:
        if distance()>110:
         while distance()>110:
             time.sleep(0.1)
         message = "*THE ROOM IS NOW EMPTY* " + str(datetime.datetime.now())
         telegram_bot.sendMessage (id, message)
         presence_flag=0

telegram_bot = telepot.Bot('ADD YOUR TELEGRAAM BOT API KEY')
print (telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print ('Up and Running....')

while 1:
    time.sleep(0.125)
    presence('CHAT/CHANNEL ID OF WHERE YOU WANT TO SEND YOUR TXTS')
