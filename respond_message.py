""" Python File to handle reponses. """

# Imports
import json

# Import custom (mine) libraries
import moon_api

def read_settings(search):
	"""Read Settings Values with given parameter"""
	with open("files/settings.json", "r") as f:
		contents = json.load(f)
		try:
			result = contents[search]
			return result
		except KeyError: # If Key does not exist or is not found, default to 1
			print("Error: Key not found or not existant, defaulting to '1' ...")
			print("Recommended Fix: Write Settings File correctly.")
			return 1

def handle_reponse(message):
	"""Function to handling messages"""
	message_lower = message.lower()

	if message_lower[:1] == read_settings("prefix"):
		# Every Reponse should be a dictionary containing a True or False, if there are multiple messages.
		return handle_message(message_lower[1:])
	else:
		# If Message was not with a prefix, return no message
		return {"message": False}


def handle_message(m):
	""" Method checking what the command was and sending appropaite Message """
	# Default Reponse layout, message is if there is a message, multiple is if there are multiple reponses, messages contains all messages
	reponse = {"message": False, "multiple": False, "messages": {},}
	# Note to 'messages', every message and image included start with a number, represententing their order (example: 1text) this should be ignored, also
	# there are only 'text' and 'image' reponses until now, they get handled in main.

	# Moon Command, gets current moon phase.
	if m == "moon":
		reponse["message"] = True
		reponse["multiple"] = True
		# Get Moon Phase as text
		reponse["messages"]["1text"] = f"Moon Phase of the {moon_api.get_current_date()} is: {moon_api.get_current_moonphase()}."
		# Get Moon Phase Image and store it, returns a path
		reponse["messages"]["1image"] = moon_api.get_c_mphase_image()
		# Return Reponse
		return reponse

	# Fullmoon Command, gets the date for the full moon.
	if m == "fullmoon":
		reponse["message"] = True
		reponse["multiple"] = False
		fullmoon_day = moon_api.get_fullmoon()
		fullmoon_day_text = f"{fullmoon_day}{moon_api.get_ending_day(fullmoon_day)}"
		reponse["messages"]["1text"] = f"The fullmoon is on the {fullmoon_day_text} of {moon_api.get_current_month_text()}."
		return reponse

	if m == "nextfullmoon":
		reponse["message"] = True
		reponse["multiple"] = False
		fullmoon_day = moon_api.get_fullmoon()
		if not moon_api.is_fullmoon_over(fullmoon_day):
			# Get fullmoon of current month.
			print("Debug Log: Sending Fullmoon of this month.")
			fullmoon_day_text = f"{fullmoon_day}{moon_api.get_ending_day(fullmoon_day)}"
			reponse["messages"]["1text"] = f"The fullmoon is on the {fullmoon_day_text} of {moon_api.get_current_month_text()}."
		else:
			# Get fullmoon of next month.
			print(f"Debug Log: Sending Fullmoon of next month ({moon_api.get_next_month_current()}).")
			fullmoon_day = moon_api.get_fullmoon(month=moon_api.get_next_month_current())
			fullmoon_day_text = f"{fullmoon_day}{moon_api.get_ending_day(fullmoon_day)}"
			reponse["messages"]["1text"] = f"The fullmoon is on the {fullmoon_day_text} of {moon_api.get_given_month_text(month=moon_api.get_next_month_current())}."
		return reponse

	# If Command is empty
	if m == "":
		reponse = {"message": False}
		return reponse

# Debugging
if __name__ == "__main__":
	# Is used to test different reponses.
	repons = handle_reponse("$nextfullmoon")
	print(list(repons.values())[0])
	#for i in repons.values():
		#print(i)