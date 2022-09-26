from datetime import datetime
import re #Regex
from PIL import Image
from io import BytesIO
import urllib.request

import requests

def get_current_moonphase():
	"""Gets the current moon phase"""
	today = datetime.today().strftime("%m/%d/%Y")
	url = "https://www.moongiant.com/phase/" + today + "/"

	r = requests.get(url)
	#print(f"Debug Log: Status Code of Moon API: {r.status_code}.\n")

	page_text = r.text

	moon_phase = re.findall("Phase: <span>(.*)</span>", page_text)

	moon = f"{moon_phase[0]}"
	return moon

def get_c_mphase_image():
	"""Get an image of the current moon phase."""
	today = datetime.today().strftime("%m/%d/%Y")
	url = "https://www.moongiant.com/phase/" + today + "/"

	r = requests.get(url)
	#print(f"Debug Log: Status Code of Moon API: {r.status_code}.\n")

	page_text = r.text

	moon_image_url = re.findall('<div id="todayMoonContainer"><img src="(.*)" width="164"', page_text)
	url_image = "https://www.moongiant.com" + moon_image_url[0]

	urllib.request.urlretrieve(url_image, "files/images/moon_phase.jpg")

	#img = Image.open(BytesIO(r.content))

	return "files/images/moon_phase.jpg"

def get_current_date():
	"""Returns current Date in format %d-%m-%Y"""
	today = datetime.today().strftime("%d-%m-%Y")
	return today

if __name__ == "__main__":
	#print(get_current_moonphase())
	print(get_c_mphase_image())