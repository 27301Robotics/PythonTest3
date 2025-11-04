# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       frankiedonahue                                               #
# 	Created:      10/22/2025, 4:28:34 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

brain = Brain()

LftBck = Motor(Ports.PORT11)
LftFnt = Motor(Ports.PORT1, True)

RgtBck = Motor(Ports.PORT20, True)
RgtFnt = Motor(Ports.PORT10)

inert = Inertial(Ports.PORT12)
colorchk = Optical(Ports.PORT2)
distancechk = Distance(Ports.PORT3)

RmG = MotorGroup(RgtBck, RgtFnt)
LmG = MotorGroup(LftBck, LftFnt)

DriverTrain = SmartDrive(LmG, RmG, inert, 300, 320, 320, INCHES, 1)

Control = Controller(PRIMARY)

def ColorSort():
    while True:
        colorchk.set_light(100)
        color = colorchk.color()
        if color == Color.RED:
            brain.screen.clear_line()
            brain.screen.set_pen_color(Color.RED)
            brain.screen.print("Red Detected")
        elif color == Color.BLUE:
            brain.screen.clear_line()
            brain.screen.set_pen_color(Color.BLUE)
            brain.screen.print("Blue Detected")
        else:
            brain.screen.clear_line()
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.print("No Color Detected")
        wait(5, MSEC)

def AutonPrinting():
    while True:
        brain.screen.clear_screen()
        brain.screen.print("autonomous code")
        brain.screen.new_line()
        brain.screen.new_line()
        brain.screen.print("Battery Life ")
        brain.screen.set_pen_color(Color.BLUE)
        brain.screen.print(brain.battery.capacity())
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.new_line()
        brain.screen.new_line()
        brain.screen.print("Heading ", inert.heading())
        brain.screen.new_line()
        brain.screen.print("Rotation ", inert.rotation())
        Control.screen.clear_screen()
        Control.screen.set_cursor(1,1)
        Control.screen.print("Heading ", inert.heading())
        Control.screen.new_line()
        Control.screen.print("Rotation ", inert.rotation())
        wait(5, MSEC)

def DriverPrinting():
    while True:
        brain.screen.clear_screen()
        brain.screen.print("Driver Control")
        brain.screen.new_line()
        brain.screen.new_line()
        brain.screen.print("Battery Life")
        brain.screen.set_pen_color(Color.BLUE)
        brain.screen.print(" ",brain.battery.capacity())
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.new_line()
        brain.screen.new_line()
        brain.screen.print("Left Back Motor Temp", Motor.temperature(LftBck))
        brain.screen.new_line()
        brain.screen.print("Left Front Motor Temp", Motor.temperature(LftFnt))
        brain.screen.new_line()
        brain.screen.print("Right Back Motor Temp", Motor.temperature(RgtBck))
        brain.screen.new_line()
        brain.screen.print("Right Front Motor Temp", Motor.temperature(RgtFnt))
        brain.screen.new_line()
        brain.screen.print("Heading ", inert.heading())
        brain.screen.new_line()
        brain.screen.print("Rotation ", inert.rotation())
        Control.screen.clear_screen()
        Control.screen.set_cursor(1,1)
        Control.screen.print("LB", LftBck.temperature(), " ")
        Control.screen.print("LF", LftFnt.temperature())
        Control.screen.new_line()
        Control.screen.print("RB", RgtBck.temperature(), " ")
        Control.screen.print("RF", RgtFnt.temperature())
        Control.screen.new_line()
        wait(5,MSEC)



def pre_auton():
    brain.screen.clear_screen()
    inert.calibrate()
    DriverTrain.set_stopping(HOLD)
    DriverTrain.set_heading(0, DEGREES)
    DriverTrain.set_rotation(0, DEGREES)
    while inert.is_calibrating():
        Control.rumble("----")
        wait(5, MSEC)


def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    Thread = (AutonPrinting)
    Thread2 = (ColorSort)
    DriverTrain.drive_for(FORWARD, 200, MM)

    # place automonous code here


def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    DriverTrain.set_stopping(COAST)
    Thread = (DriverPrinting)
    Thread2 = (ColorSort)
    # place driver control in this while loop
    while True:
        RmG.set_velocity((Control.axis3.position() + Control.axis1.position()), PERCENT)
        LmG.set_velocity((Control.axis3.position() - Control.axis1.position()), PERCENT)
        RmG.spin(FORWARD)
        LmG.spin(FORWARD)
        
        wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)
pre_auton()

# actions to do when the program starts
brain.screen.clear_screen()