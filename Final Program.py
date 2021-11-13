import math
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import speech_recognition as sr
r = sr.Recognizer()
speech = sr.Microphone(device_index=2)

trigger_word = "Pradeep" #This name can be changed to applicable one 
RST = None
# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize oled library.
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height

# Clear display.
disp.clear()
time.sleep(1)
disp.display()

image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

font = ImageFont.truetype("peace_sans.otf",15) #font style is set to default you may choose different font style


while True:
    with speech as source:
        print("say something!…")
        audio = r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        recog = r.recognize_google(audio, language = 'en-US')
        print("You said: " + recog)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    trigger_word_index=recog.find(trigger_word)
    text="None"
    if(trigger_word_index>=0):
        print("triggered")
        text=recog[trigger_word_index+7:]
    print("text is ",text)    
    maxwidth, unused = draw.textsize(text, font=font)
    # Set animation and sine wave parameters.
    maxwidth, unused = draw.textsize(text, font=font)

    # Set animation parameters.
    velocity = -15   #changeable
    startpos = width

    # Animate text.
    print('Press Ctrl-C to quit.')
    pos = startpos
    while True:
        # Clear image buffer by drawing a black filled box.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        # Enumerate characters and draw them.
        x = pos
        for i, c in enumerate(text):
            # Stop drawing if off the right side of screen.
            if x > width:
                break
            # Calculate width but skip drawing if off the left side of screen.
            if x < -10:
                char_width, char_height = draw.textsize(c, font=font)
                x += char_width
                continue
            y = 10
            # Draw text.
            draw.text((x, y), c, font=font, fill=255)
            # Increment x position based on chacacter width.
            char_width, char_height = draw.textsize(c, font=font)
            x += char_width
        # Draw the image buffer.
        disp.image(image)
        
        disp.display()
        # Move position for next frame.
        pos += velocity
        # Start over if text has scrolled completely off left side of screen.
        if pos < -maxwidth:
            break
        # Pause briefly before drawing next frame.
        time.sleep(0.4)
    text=""
    recog=""
    disp.clear()
    disp.display()
    time.sleep(1) 
