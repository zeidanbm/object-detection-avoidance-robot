from Adafruit_IO import *
import RPi.GPIO as GPIO
import time
import random
from picamera import PiCamera
import socketio
import secrets

aio = Client(ADAFRUIT_USERNAME, ADAFRUIT_TOKEN)
print('~~~ AdaFruit connected ~~ ', aio)

server = WEBSOCKET_SERVER  # Server IP Address or domain
sio = socketio.Client()
global is_active # determine if we are moving or not
is_active = True

# dc motors
en1, L1, L2 = 23, 24, 25
en2, R1, R2 = 21, 16, 20

# ultrasonic sensor
trig, echo = 15, 18


def backward():
    GPIO.output(L1, GPIO.HIGH)
    GPIO.output(L2, GPIO.LOW)

    GPIO.output(R1, GPIO.HIGH)
    GPIO.output(R2, GPIO.LOW)


def forward():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.HIGH)

    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.HIGH)


def right():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.HIGH)

    GPIO.output(R1, GPIO.HIGH)
    GPIO.output(R2, GPIO.LOW)


def left():
    GPIO.output(L1, GPIO.HIGH)
    GPIO.output(L2, GPIO.LOW)

    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.HIGH)


def stop():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.LOW)

    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.LOW)


def distance():
    GPIO.output(trig, GPIO.HIGH)

    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(echo) == 0:
        StartTime = time.time()

    while GPIO.input(echo) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2

    return distance


def take_snapshot():
  image = '/home/pi/Desktop/image.jpg'
  camera = PiCamera()
  camera.start_preview()
  time.sleep(2)
  camera.capture(image)
  camera.stop_preview()


@sio.event
def connect():
    print("I'm connected!")


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


@sio.on('TRIGGER_SNAPSHOT_PI')
def on_snapshot_trigger(data):
    print('I received a message!')
    print(data)
    take_snapshot()
    time.sleep(0.2)


@sio.on('TOGGLE_MOTOR_PI')
def on_motor_trigger(data):
    global is_active
    print('I received a message!')
    print(data)
    if data and is_active == False:
      is_active = True
      run()
    elif data == False and is_active == True:
      is_active = False
      stop()


def connect_to_ws():
  sio.connect(server)
  sio.sleep(2)
  sio.emit('raspberrypi', 1)



def loop(left_motor, right_motor):
    try:
        n = 20
        while is_active:
            dist = distance()
            if n == 0:
                n = 20
                aio.send('f1', dist)
                carSpeed = int(aio.receive('f3-speed').value)  # cloud dashboard controls direction of car
                print(carSpeed)
                left_motor.ChangeDutyCycle(carSpeed)
                right_motor.ChangeDutyCycle(carSpeed)

            else:
                n -= 1


            if dist <= 20:
                stop()
                time.sleep(0.4)
                backward()
                time.sleep(0.7)
                stop()
                if bool(random.getrandbits(1)):
                  left()
                  print('going left')
                else:
                  right()
                  print('going right')
                time.sleep(0.7)
                stop()
            else:
                forward()

            print("Measured Distance = %.1f cm" % dist)
            time.sleep(0.1)

    except KeyboardInterrupt:
        destroy()


def run():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    # right motor
    GPIO.setup(L1, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
    GPIO.setup(en1, GPIO.OUT)
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.LOW)

    # left motor
    GPIO.setup(R1, GPIO.OUT)
    GPIO.setup(R2, GPIO.OUT)
    GPIO.setup(en2, GPIO.OUT)
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.LOW)

    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

    #setMotorFrequency(80)
    left_motor = GPIO.PWM(en1, 100)
    right_motor = GPIO.PWM(en2, 100)
    left_motor.start(55)
    right_motor.start(55)
    loop(left_motor, right_motor)

def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    print('Program is starting...')
    connect_to_ws()
    run()
