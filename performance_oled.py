#!/usr/bin/env python
import psutil
import httplib, urllib
import time
import os,sys
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

disk = os.statvfs("/")
used = disk.f_bsize * (disk.f_blocks - disk.f_bavail)
sleep = 30 				  # how many seconds to sleep between posts to the channel
key = 'ZG8WMLWF4PBQQVFB'  # Write Key Thingspeak channel to update

#Report Raspberry Pi internal temperature to Thingspeak Channel
def performance():
    while True:
		# Get Raspberry Pi CPU temp
		cpu = psutil.cpu_percent(interval=0)
		mem = psutil.virtual_memory().used/1000000
		temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 
		
		params = urllib.urlencode({'field1':cpu ,'field2': temp,'field3':mem,'field4':used/1.073741824e9,'key':key})
		headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
		conn = httplib.HTTPConnection("api.thingspeak.com:80")

		str_temp = ' {0:0} *C '.format(temp)	
		str_cpu  = ' {0:0.2f} %'.format(cpu)

		# Clear image buffer by drawing a black filled box.
		draw.rectangle((0,0,width,height), outline=0, fill=0)	
		
		# Write two lines of text.
		draw.text((x, top),    str_cpu,  font=font18, fill=255)	
		draw.text((x, top+22), str_temp, font=font18, fill=255)

		# Display image.
		#disp.image(image)
		#disp.display()
		
		try:
			conn.request("POST", "/update", params, headers)
			response = conn.getresponse()
			print response.status,response.reason
			print cpu
			print temp
			
			draw.text((x, top+46), ' status '+ response.reason, font=font10, fill=255)
			disp.image(image)
			disp.display()
			
			if (cpu >= 90):
				notify(ip+" - CPU: "+str(cpu))
			print mem
			mem_percent = (psutil.virtual_memory().used*100/psutil.virtual_memory().total)
			print mem_percent
			if(mem_percent >= 70):
				notify(ip+" - Memory: "+str(mem_percent))
			print response.status, response.reason
			#data = response.read()
			conn.close()
		except:
			print "connection failed",sys.exc_info()
		break
		
def checkNet():  
    try:
        response = requests.get("http://www.google.com")
        print response
    except requests.ConnectionError:
        print "Could not connect"			
		
# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 2
shape_width = 20
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = padding

# Load default font.
font = ImageFont.load_default()
font10 = ImageFont.truetype('Minecraftia.ttf', 10)
font18 = ImageFont.truetype('Minecraftia.ttf', 18)
font42 = ImageFont.truetype('Minecraftia.ttf', 42)

# Write two lines of text.
draw.text((x, top),    ' ThingSpeak',  font=font, fill=255)
draw.text((x, top+20), 'Raspberry', font=font18, fill=255)

# Display image.
disp.image(image)
disp.display()
time.sleep(2)

	
#sleep for desired amount of time
#if __name__ == "__main__":
while True:
        while True:
			performance()
			time.sleep(sleep)

