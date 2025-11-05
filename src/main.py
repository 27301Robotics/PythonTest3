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

LftBck = Motor(Ports.PORT13)
LftFnt = Motor(Ports.PORT1, True)

RgtBck = Motor(Ports.PORT16, True)
RgtFnt = Motor(Ports.PORT10)

Intake1 = Motor(Ports.PORT19)
Intake2 = Motor(Ports.PORT17)


inert = Inertial(Ports.PORT7)

colorchk = Optical(Ports.PORT9)
distancechk = Distance(Ports.PORT3)

RmG = MotorGroup(RgtBck, RgtFnt)
LmG = MotorGroup(LftBck, LftFnt)

DriverTrain = SmartDrive(LmG, RmG, inert, 300, 320, 320, INCHES, 1)

Control = Controller(PRIMARY)

def ColorSortA():
    while True:
        brain.screen.set_cursor(7, 1)
        colorchk.set_light(100)
        Intake1.set_velocity(100, PERCENT)
        Intake2.set_velocity(100, PERCENT)
        Intake1.spin(FORWARD)
        Intake2.spin(FORWARD)
        color = colorchk.color()
        if color == Color.RED:
            Intake1.spin(REVERSE)
            Intake2.spin(FORWARD)
            brain.screen.clear_line()
            brain.screen.set_pen_color(Color.RED)
            brain.screen.print("Red Detected")
        elif color == Color.BLUE:
            #Intake1.spin(REVERSE)
            #Intake2.spin(FORWARD)
            brain.screen.clear_line()
            brain.screen.set_pen_color(Color.BLUE)
            brain.screen.print("Blue Detected")
        else:
            brain.screen.clear_line()
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.print("No Color Detected")
        wait(5, MSEC)

def ColorSortD():
    while True:
        brain.screen.set_cursor(9, 1)
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
        brain.screen.set_cursor(3, 1)
        brain.screen.print("Battery Life ")
        brain.screen.set_pen_color(Color.RED)
        brain.screen.print(brain.battery.capacity())
        brain.screen.set_pen_color(Color.WHITE)
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
        brain.screen.set_cursor(3, 1)
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
    brain.screen.set_cursor(1, 1)
    inert.calibrate()
    DriverTrain.set_stopping(HOLD)
    DriverTrain.set_heading(0, DEGREES)
    DriverTrain.set_rotation(0, DEGREES)


def autonomous():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("autonomous code")
    brain.screen.new_line()
    thread1 = Thread(AutonPrinting)
    thread2 = Thread(ColorSortA)
    DriverTrain.drive_for(FORWARD, 100, MM)
    
    

    # place automonous code here


def user_control():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("driver control")
    DriverTrain.set_stopping(COAST)
    thread3 = Thread(DriverPrinting)
    thread4 = Thread(ColorSortD)
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