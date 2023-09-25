### TETSHOUSE ROBOT @ candelatechnologies

### Pin connections of pn532 rfreader
###----------------------------------
### GPIO<-->Inx
### 2   <--> SDA
### 3   <--> SCL
### 5V  <--> VCC
### GND <--> GND

### Pin connections of cytron motor driver
###----------------------------------
### GPIO<-->Inx
### 19  <--> RED(PWM2)
### 21  <--> ORANGE(DIR2)
### 13  <--> YELLOW(PWM1)
### 20  <--> GREEN(DIR1)
### GND <--> BROWN,BLACK

### Pin connections of line sensor
###----------------------------------
### GPIO<-->Inx
### 14  <--> S1
### 17  <--> S2
### 23  <--> S3
### 27  <--> S4
### 24  <--> S5
### GND <--> GND

#PWM GPIO pins are GPIO 12,13,18,19

import RPi.GPIO as GPIO
import time
import json
from gpiozero import Robot, LineSensor
from signal import pause


logfile = '/home/canbee/Desktop/ROBOT/py532lib/robot_logs.json'
nfcRead = '/home/canbee/Desktop/ROBOT/py532lib/nfcRead.py'
inputsfile = '/home/canbee/Desktop/ROBOT/py532lib/input.json'

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

# map the GPIO to read IR sensor
left_sensor = LineSensor(17)
leftMost = LineSensor(15)
right_sensor = LineSensor(27)
righMost = LineSensor(24)
middle = LineSensor(23)
frequency=2000
p = GPIO.PWM(13, frequency)
q = GPIO.PWM(19, frequency)
p.start(0) #//Starting point of PWM signal you can select any value between 0 to 100.
q.start(0)
### To drive the motors using cytron MD20A motor driver
def navigate_bot(cmd, speed, frequency):

    if(cmd=='f'):
        GPIO.output(21,GPIO.HIGH)
        GPIO.output(20,GPIO.LOW)
        p.ChangeDutyCycle(speed)
        q.ChangeDutyCycle(speed)
    elif(cmd=='right'):
    # 		print("Turning Right")
        GPIO.output(21,GPIO.LOW)
        GPIO.output(20,GPIO.LOW)
        p.ChangeDutyCycle(speed)
        q.ChangeDutyCycle(speed)
    elif(cmd=='l'):
    # 		print("Turning Left")
        GPIO.output(21,GPIO.HIGH)
        GPIO.output(20,GPIO.HIGH)
        p.ChangeDutyCycle(speed)
        q.ChangeDutyCycle(speed)
    elif(cmd=='s'):
        #print("stopped")
        p.ChangeDutyCycle(0)
        q.ChangeDutyCycle(0)
        GPIO.output(21,GPIO.LOW)
        GPIO.output(20,GPIO.LOW)
    elif(cmd=='b'):
    # 		print("back")
        p.ChangeDutyCycle(10)
        q.ChangeDutyCycle(10)
        GPIO.output(21,GPIO.LOW)
        GPIO.output(20,GPIO.HIGH)

    return None

### To follow the inputs and folow the line accordingly
def line_follow(speed, frequency):
    while(1):
        try:
            x = open(logfile,'r')
            data=json.load(x)
            x.close()
        except:
            print("error with reading Robot_log.json")
            data={}
        left=int(left_sensor.value)
        right=int(right_sensor.value)
        line=int(middle.value)
        Line_data=[int(leftMost.value),int(left_sensor.value),int(middle.value),int(right_sensor.value),int(righMost.value)]
        if(Line_data==[1,1,0,1,1]):
            navigate_bot(cmd='f', speed=speed, frequency=frequency)
            data['bot_status']='Moving forward with full speed'

        elif(Line_data==[1,1,1,1,1]):
            if((data['bot_status']!='Moving forward with reduced speed') ):
                navigate_bot(cmd='s', speed=0, frequency=frequency)
                time.sleep(0.1)
            navigate_bot(cmd='f', speed=50, frequency=frequency)
            data['bot_status']='Moving forward with reduced speed'


        elif(Line_data==[1,1,0,0,1]):
            if((data['bot_status']!='Moving Right with reduced speed') or (data=={})):
                navigate_bot(cmd='s', speed=0, frequency=frequency)
                time.sleep(0.1)
            navigate_bot(cmd='right', speed=40, frequency=frequency)
            data['bot_status']='Moving Right with reduced speed'

        elif(Line_data==[1,1,1,0,1]):
            navigate_bot(cmd='right', speed=speed, frequency=frequency)
            data['bot_status']='Moving Right'

        elif(Line_data==[1,0,0,1,1]):
            if((data['bot_status']!='Moving Left with reduced speed') or (data=={})):
                navigate_bot(cmd='s', speed=0, frequency=frequency)
                time.sleep(0.1)
            navigate_bot(cmd='l', speed=40, frequency=frequency)
            data['bot_status']='Moving Left with reduced speed'

        elif(Line_data==[1,0,1,1,1]):
            print("execute 10111")
            navigate_bot(cmd='l', speed=speed, frequency=frequency)
            data['bot_status']='Moving Left'

        elif(Line_data==[0,0,0,0,0]):
            print("stop else")
            navigate_bot('s', speed=speed, frequency=frequency)
            data['bot_status']='Stopped'
            x=open(inputsfile, 'r')
            temp=json.load(x)
            x.close()
            temp['mode']='Auto'
            temp['halt']='Stop'
            x = open(inputsfile,'w')
            json.dump(temp,x,indent=4)
            x.close()
        elif(Line_data==[1,0,0,0,1]):
            print("stop else")
            navigate_bot('s', speed=speed, frequency=frequency)
            data['bot_status']='Stopped'
            x=open(inputsfile, 'r')
            temp=json.load(x)
            x.close()
            temp['mode']='Auto'
            temp['halt']='Stop'
            x = open(inputsfile,'w')
            json.dump(temp,x,indent=4)
            x.close()
        elif(Line_data==[0,0,1,0,0]):
            print("stop else")
            navigate_bot('s', speed=speed, frequency=frequency)
            data['bot_status']='Stopped'
            x=open(inputsfile, 'r')
            temp=json.load(x)
            x.close()
            temp['mode']='Auto'
            temp['halt']='Stop'
            x = open(inputsfile,'w')
            json.dump(temp,x,indent=4)
            x.close()

        print(data['bot_status'])
        data['Sensor_Output']=Line_data
        x = open(logfile,'w')
        json.dump(data, x, indent=4)
        x.close()
        print(int(leftMost.value),int(left_sensor.value),int(middle.value),int(right_sensor.value),int(righMost.value))
        return None

while(True):
    try:
        x = open(inputsfile,'r')
        data=json.load(x)
        speed=data['speed']
        frequency=data['frequency']
        x.close()
    except:
        speed=50
        frequency=1000
    if(data['mode']=='Auto' and (data['halt']=='Start' or data['halt']=='Skipped')):
        line_follow(speed=speed,frequency=frequency)
    elif(data['mode']=='Auto' and data['halt']=='Skip'):
        data['halt']='Skipped'
        x = open(inputsfile,'w')
        json.dump(data, x, indent=4)
        x.close()
        navigate_bot('f',speed=50, frequency=frequency)
        time.sleep(0.5)
        line_follow(speed=speed,frequency=frequency)
    else:
        navigate_bot('s',speed=speed,frequency=frequency)
