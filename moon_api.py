"""Custom python file which can get info of the moon"""

# Default Imports
from datetime import datetime
import re #Regex
from PIL import Image
from io import BytesIO
import urllib.request

import requests

def get_current_moonphase():
	"""Gets the current moon phase"""
	# Gets current date and creates fitting url
	today = datetime.today().strftime("%m/%d/%Y")
	url = "https://www.moongiant.com/phase/" + today + "/"

	# Loads Page
	r = requests.get(url)
	#print(f"Debug Log: Status Code of Moon API: {r.status_code}.\n")

	page_text = r.text

	# Regex finding the moon phase information on page.
	moon_phase = re.findall("Phase: <span>(.*)</span>", page_text)

	# Returns moon phase
	moon = f"{moon_phase[0]}"
	return moon

def get_c_mphase_image():
	"""Get an image of the current moon phase."""
	# Gets current date and creates fitting url
	today = datetime.today().strftime("%m/%d/%Y")
	url = "https://www.moongiant.com/phase/" + today + "/"

	# Gets Page and loads it as text
	r = requests.get(url)
	#print(f"Debug Log: Status Code of Moon API: {r.status_code}.\n")

	page_text = r.text

	# Finding the image of todays moon and creating an url to that image
	moon_image_url = re.findall('<div id="todayMoonContainer"><img src="(.*)" width="164"', page_text)
	url_image = "https://www.moongiant.com" + moon_image_url[0]

	# Retrieving image from url and saving it.
	urllib.request.urlretrieve(url_image, "files/images/moon_phase.jpg")

	# Old way to transfer image, wasn't working with discord.py
	#img = Image.open(BytesIO(r.content))

	# Returns path to image
	return "files/images/moon_phase.jpg"

def get_current_date():
	"""Returns current Date in format %d-%m-%Y"""
	today = datetime.today().strftime("%d-%m-%Y")
	return today

# Debugging
if __name__ == "__main__":
	# Used to test functions
	#print(get_current_moonphase())
	print(get_c_mphase_image())