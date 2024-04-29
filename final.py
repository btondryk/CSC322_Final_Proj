#libraries
import os
import sys
import time
import logging
import spidev as SPI
import random
from PIL import Image
from lib import LCD_1inch28
import RPi.GPIO as GPIO

#navigating directories
sys.path.append("/home/btondryk/LCD_Module_RPI_code/RaspberryPi/python")
imagePath = "/home/btondryk/LCD_Module_RPI_code/RaspberryPi/python/"

def display_random_image(disp, image_path=None):
    '''
    This function will be responsible for picking a random image from all of the image files. It uses 
    random choice to randomly select an image. It also orients the image properly as well as displays the
    image on the lcd screen. Always starts with the same image.
    '''
    if image_path is None:
        image_files = ['pic/bam.jpg','pic/bam2.jpg', 'pic/boom.jpg', 'pic/boom2.jpg', 'pic/bra.jpg', 'pic/bullet.jpg', 'pic/business.jpg','pic/Bzz.jpg','pic/cross.jpg', 'pic/cross2.jpg', 'pic/cross3.jpg', 'pic/cross4.jpg', 'pic/cross5.jpg', 'pic/cross6.jpg','pic/flink.jpg','pic/fox.jpg', 'pic/gun.jpg', 'pic/gun2.jpg', 'pic/koala.jpg', 'pic/pirate.jpg', 'pic/pirate2.jpg','pic/pirate3.jpg','pic/pop.jpg', 'pic/pop2.jpg', 'pic/pow.jpg', 'pic/pwon.jpg', 'pic/pwon2.jpg', 'pic/sloth.jpg', 'pic/whoosh1.jpg', 'pic/whoosh2.jpg']  # Add more image paths as needed
        random_image_path = random.choice(image_files)
        image = Image.open(f'{imagePath}{random_image_path}')
    else:
        image = Image.open(f'{imagePath}{image_path}')
    im_r = image.rotate(180)
    disp.ShowImage(im_r)

def main():

    RST = 27    #reset to initial state
    DC = 25     #Data/command selection (high for data, low for command)
    BL = 18     #Backlight

    #communicate with the LCD module
    bus = 0     #the SPI bus 
    device = 0  #device number

    logging.basicConfig(level=logging.DEBUG) #

    try:
        GPIO.setmode(GPIO.BCM)  #refers to channel number rather than physical pins
        disp = LCD_1inch28.LCD_1inch28()    #initialize LCD_module object
        disp.Init()     #initialize lcd_module
        disp.clear()    #clears the display
        disp.bl_DutyCycle(50)   #controls the brightness of the backlight, here it is 50%        
        im_r = Image.new("RGB", (disp.width, disp.height), "BLACK").rotate(180)     #display the image with the proper orientation
        disp.ShowImage(im_r)

        display_random_image(disp, 'pic/logo.jpg')  #Always displays this image on the LCD_screen upon boot up
        time.sleep(0.250)
        
        SWITCH_PIN = 16 #where the switch pin is connnected and how quickly in between presses you can click
        DEBOUNCE_TIME_MS = 250

        GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #detecs button presses

        while True:
            input_state = GPIO.input(SWITCH_PIN)
            if input_state == False: #when limit switch is pressed input_state == False
                display_random_image(disp)
                time.sleep(0.250)  # Debouncing delay

    except KeyboardInterrupt:
        logging.info("Keyboard interrupt detected, cleaning up GPIO...")
        GPIO.cleanup()
        disp.module_exit()
        logging.info("Quit.")

    except IOError as e:
        logging.info(e) #catches errors

if __name__ == "__main__":
    main()