import os
import sys
import time
import logging
import spidev as SPI
import random
#helps with references
sys.path.append("/home/btondryk/LCD_Module_RPI_code/RaspberryPi/python")
from PIL import Image
from lib import LCD_1inch28
import RPi.GPIO as GPIO
#makes referencing the image files easier
imagePath = "/home/btondryk/LCD_Module_RPI_code/RaspberryPi/python/"
#displays a random image when the limit switch is pressed, always starts with the same starting image to indicate
#the code is ready
def display_random_image(disp, image_path=None):
    if image_path is None:
        image_files = ['pic/Earth.jpg','pic/koala.jpg', 'pic/rabbit.jpg', 'pic/fire.jpg', 'pic/crosshair.jpg', 'pic/planes.jpg', 'pic/star.jpg']  # Add more image paths as needed
        random_image_path = random.choice(image_files)
        image = Image.open(f'{imagePath}{random_image_path}')
    else:
        image = Image.open(f'{imagePath}{image_path}')
    im_r = image.rotate(180)
    disp.ShowImage(im_r)

def main():
    RST = 27
    DC = 25
    BL = 18
    bus = 0
    device = 0
    logging.basicConfig(level=logging.DEBUG)

    try:
        GPIO.setmode(GPIO.BCM)
        disp = LCD_1inch28.LCD_1inch28()
        disp.Init()
        disp.clear()
        disp.bl_DutyCycle(50)
        #display the image with the proper orientation
        im_r = Image.new("RGB", (disp.width, disp.height), "BLACK").rotate(180)
        disp.ShowImage(im_r)

        display_random_image(disp, 'pic/logo.jpg')
        time.sleep(0.250)
        #where the switch pin is connnected and how quickly in between presses you can click
        SWITCH_PIN = 16
        DEBOUNCE_TIME_MS = 250

        GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        def button_callback(channel):
            display_random_image(disp)

        GPIO.add_event_detect(SWITCH_PIN, GPIO.RISING, callback=button_callback, bouncetime=DEBOUNCE_TIME_MS)
        #sleep
        while True:
            time.sleep(0.250)

    except KeyboardInterrupt:

        GPIO.cleanup()
        disp.module_exit()
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        disp.module_exit()
        logging.info("Quit.")

if __name__ == "__main__":
    main()