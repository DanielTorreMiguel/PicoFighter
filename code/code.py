import board
import digitalio
import analogio
import usb_hid
import time

from hid_gamepad import Gamepad

# buttons mapped to pins
buttonPins = [
    board.GP16,
    board.GP17,
    board.GP18,
    board.GP20,
    board.GP15,
    board.GP19,
    board.GP21,
    board.GP14,
    board.GP12,
    board.GP11,
    board.GP10,
]
# For some reason B6 = GP13 is not working
dpadPins = [board.GP9, board.GP8, board.GP3, board.GP7]  # up down left right
dipPins = [
    board.GP27,
    board.GP26,
    board.GP22,
    board.GP28,
    board.GP6,
    board.GP5,
    board.GP4,
]

buttons = []  # digitalIO objects
dpad = []
dips = []
mode = 0


for i in buttonPins:
    button = digitalio.DigitalInOut(i)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    buttons.append(button)

for i in dpadPins:
    dpadButt = digitalio.DigitalInOut(i)
    dpadButt.direction = digitalio.Direction.INPUT
    dpadButt.pull = digitalio.Pull.UP
    dpad.append(dpadButt)


for i in dipPins:
    dip = digitalio.DigitalInOut(i)
    dip.direction = digitalio.Direction.INPUT
    dip.pull = digitalio.Pull.UP
    dips.append(dip)

# initializations
gp = Gamepad(usb_hid.devices)

delayTime = 0
# check DIP config
if not dips[0].value:
    delayTime = 0.001
else:
    delayTime = 0


while True:
    xAxis = dpad[0].value * 127 + dpad[1].value * -127
    yAxis = dpad[3].value * 127 + dpad[2].value * -127
    gp.move_joysticks(xAxis, yAxis)
    for i in range(0, len(buttons)):
        if not buttons[i].value:
            gp.press_buttons(i + 1)
        else:
            gp.release_buttons(i + 1)
    time.sleep(delayTime)
