from gpiozero import Button, DistanceSensor
from grove.grove_thumb_joystick import GroveThumbJoystick
from grove.grove_mini_pir_motion_sensor import GroveMiniPIRMotionSensor
from grove.grove_led import GroveLed
from grove.gpio import GPIO
from grovepi import *

import time
from subprocess import run
import pyautogui

"""
Třída pro inicializaci tlačítek pro ovládání konzole
"""
class Button_controller:
    """
    Inicializace tlačítka
    pin - pin na kterém je tlačítko připojeno (int)
    key - klávesa, jejíž stisknutí se vyvolá po stisku tlačítka (str)
    """
    def __init__(self, pin, key):
        self.key = str(key)
        self.pin = pin
        self.button = Button(int(pin))
        self.button.when_pressed = self.button_pressed

    def button_pressed(self):
        pyautogui.press(self.key)

"""
Třída pro inicializaci joysticku pro ovládání konzole
"""
class Joystick_controller:
    """
    Initializace joysticku
    pin - pin na kterém je joystick připojen (int)
    """
    def __init__(self, pin):
        self.pin = pin
        self.joystick = GroveThumbJoystick(int(pin))
    
    """
    Načítání hodnot joysticku a volání klávesy podle hodnoty
    """
    def joystick_handle(self, root):
        x,y = self.joystick.value
        if x > 900:
            pyautogui.press('g')
            print("joystick pressed")
        elif x < 300 and 450 < y < 550:
            #pyautogui.press('up') #left
            pyautogui.press('left')
            
        elif x > 700 and 450 < y < 550:
            #pyautogui.press('down') #right
            pyautogui.press('right')
            
        elif y < 300 and 450 < x < 550:
            #pyautogui.press('left') #down
            pyautogui.press('down')
            
        elif y > 700 and 450 < x < 550:
            #pyautogui.press('right') #up
            pyautogui.press('up')
            
        if root is not None:
            root.after(50, self.joystick_handle, root)
        
class PIRMotionSensor:
    def __init__(self, pin):
        self.pin = pin
        self.sensor = GroveMiniPIRMotionSensor(int(pin))
        self.motion_detected = False
        self.start_time = time.time()
        self.seconds_since_motion = 0
    
    def get_motion(self, root):
        if self.sensor.read():
            self.motion_detected = True
            run('DISPLAY=:0 xrandr --output HDMI-1 --auto', shell=True)
            
        else:
            self.motion_detected = False
            #print("no motion detected")

        if self.motion_detected:            
            self.start_time = time.time()
        else:
            self.seconds_since_motion = time.time() - self.start_time
        
        if self.seconds_since_motion >= 30:
            #print("no motion detected for 30 seconds, turning off display")
            run('DISPLAY=:0 xrandr --output HDMI-1 --off', shell=True)
            self.seconds_since_motion = 0
        
        if root is not None:
            root.after(50, self.get_motion, root)

class FlashLed:
    def __init__(self, pin_led1, pin_led2):
        self.pin_led1 = pin_led1
        self.pin_led2 = pin_led2
        self.led_1 = GroveLed(int(pin_led1))
        self.led_2 = GroveLed(int(pin_led2))
        self.led_1.off()
        self.led_2.off()

    def flash(self):
        self.led_1.on()
        self.led_2.on()
        time.sleep(4)
        self.led_1.off()
        self.led_2.off()