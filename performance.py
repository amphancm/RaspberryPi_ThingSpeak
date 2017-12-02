#!/usr/bin/env python
import psutil
import httplib, urllib
import time
import os,sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

disk = os.statvfs("/")
used = disk.f_bsize * (disk.f_blocks - disk.f_bavail)
sleep = 30 				  # how many seconds to sleep between posts to the channel
key = 'ZG8WMLWF4PBQQVFB'                  # Write Key Thingspeak channel to update
# THIS IS MY KEY for THINGSPEAK Channel 238835
# YOUR MUST CHANGE to YOUR WRITE KEY

#Report Raspberry Pi internal temperature to Thingspeak Channel
def performance():
    while True:
		cpu = psutil.cpu_percent()
		mem = psutil.virtual_memory().used/1000000
		temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp
		params = urllib.urlencode({'field1':cpu ,'field2': temp,'field3':mem,'field4':used/1.073741824e9,'key':key})
		headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
		conn = httplib.HTTPConnection("api.thingspeak.com:80")	
		try:
			conn.request("POST", "/update", params, headers)
			response = conn.getresponse()
			print cpu
			print temp
			if (cpu >= 90):
				notify(ip+" - CPU: "+str(cpu))
			print mem
			mem_percent = (psutil.virtual_memory().used*100/psutil.virtual_memory().total)
			print mem_percent
			if(mem_percent >= 70):
				notify(ip+" - Memory: "+str(mem_percent))
			print response.status, response.reason
			data = response.read()
			conn.close()
		except:
			print "connection failed",sys.exc_info()
		break
		
#sleep for desired amount of time
#if __name__ == "__main__":
while True:
        while True:
			performance()
			time.sleep(sleep)

