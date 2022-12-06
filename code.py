import array
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn, AnalogOut
import pulseio
import busio
import adafruit_pca9685
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket
#from adafruit_motor import motor
from adafruit_motorkit import MotorKit
import board
import time

## Hardware Configuration

print("Define Hardware")
kit = MotorKit()
# kit.motor1 = Left Motor
# kit.motor2 = Right Motor
# Kit.motor3 = Solenoid (Magnet)
ble = BLERadio()
ble.name = "Chicken"
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

print("Define Digital Inputs")
''' #Remote Boat
forwardPin = DigitalInOut(board.D9)
reversePin = DigitalInOut(board.D10)
leftPin = DigitalInOut(board.D11)
rightPin = DigitalInOut(board.D12)
buttonPin = DigitalInOut(board.D13)

forwardPin.direction = Direction.INPUT
reversePin.direction = Direction.INPUT
leftPin.direction = Direction.INPUT
rightPin.direction = Direction.INPUT
buttonPin.direction = Direction.INPUT


forwardPin.pull = Pull.DOWN
reversePin.pull = Pull.DOWN
leftPin.pull = Pull.DOWN
rightPin.pull = Pull.DOWN
buttonPin.pull = Pull.DOWN
'''



print("Hardware Config Complete")
## Software Configuration
# Global Variables

throttleUpThresh = 25
throttleDownThresh = 20


# Function Definition

def forward(a):
    throttle = a/throttleUpThresh
    if throttle > 1.0:
        throttle = 1.0
    elif throttle > 0 and throttle < 0.3:
        throttle = 0.35
    elif throttle < 0 and throttle > -0.3:
        throttle = -0.35
    elif throttle < -1.0:
        throttle = -1.0
    print("Throttle is: ", throttle)
    kit.motor1.throttle = throttle
    kit.motor2.throttle = throttle
    #return_a = throttle * throttleUpThresh
    #return return_a
    time.sleep(0.5)

def reverse(a):
    throttle = a/throttleDownThresh
    if throttle < -1.0:
        throttle = -1.0
    elif throttle > 0 and throttle < 0.3:
        throttle = 0.35
    elif throttle < 0 and throttle > -0.3:
        throttle = -0.35
    elif throttle > 1.0:
        throttle = 1.0
    print("Throttle is: ", throttle)
    kit.motor1.throttle = throttle
    kit.motor2.throttle = throttle
    #return_a = throttle * throttleDownThresh
    #return return_a
    time.sleep(0.5)

def left(a):
    throttle = a/throttleDownThresh
    if throttle < -1.0:
        throttle = -1.0
    elif throttle > 0 and throttle < 0.3:
        throttle = 0.35
    elif throttle < 0 and throttle > -0.3:
        throttle = -0.35
    elif throttle > 1.0:
        throttle = 1.0
    print("Throttle is: ", throttle)
    kit.motor1.throttle = -0.5
    kit.motor2.throttle = throttle
    #return_a = throttle * throttleDownThresh
    #return return_a
    time.sleep(1)


def right(a):
    throttle = a/throttleDownThresh
    if throttle < -1.0:
        throttle = -1.0
    elif throttle > 0 and throttle < 0.3:
        throttle = 0.35
    elif throttle < 0 and throttle > -0.3:
        throttle = -0.35
    elif throttle > 1.0:
        throttle = 1.0
    print("Throttle is: ", throttle)
    kit.motor1.throttle = throttle
    kit.motor2.throttle = -0.5
    #return_a = throttle * throttleDownThresh
    #return return_a
    time.sleep(1)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0, 0, 0)
# Change SLEEP to 6 for full
SLEEP = 6
BURST_SLEEP = 0.2
DISCHARGE_SLEEP = 0.3

throttle = 0

while True:
    print("WAITING...")
    # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    # Connected
    ble.stop_advertising()
    print("CONNECTED")

    # Loop and read packets
    while ble.connected:
        # Keeping trying until a good packet is received
        try:
            packet = Packet.from_stream(uart_server)
        except ValueError:
            continue

        if isinstance(packet, ButtonPacket) and packet.pressed:
            if packet.button == ButtonPacket.UP:
                print("Button UP")
                kit.motor1.throttle = -1
                kit.motor3.throttle = 1
            if packet.button == ButtonPacket.DOWN:
                print("Button DOWN")
                kit.motor1.throttle = 1
                kit.motor3.throttle = -1
            if packet.button == ButtonPacket.LEFT:
                print("Button LEFT")
                kit.motor1.throttle = -.5
                kit.motor3.throttle = -.5
                time.sleep(.2)
                kit.motor1.throttle = 0
                kit.motor3.throttle = 0
            if packet.button == ButtonPacket.RIGHT:
                print("Button RIGHT")
                kit.motor1.throttle = .5
                kit.motor3.throttle = .5
                time.sleep(.2)
                kit.motor1.throttle = 0
                kit.motor3.throttle = 0
            if packet.button == ButtonPacket.BUTTON_1:
                print("Button 1")
                kit.motor1.throttle = 0
                kit.motor3.throttle = 0
            if packet.button == ButtonPacket.BUTTON_2:
                print("Button 2")
            if packet.button == ButtonPacket.BUTTON_3:
                print("Button 3")
            if packet.button == ButtonPacket.BUTTON_4:
                print("Button 4")

    # Disconnected
    print("DISCONNECTED")