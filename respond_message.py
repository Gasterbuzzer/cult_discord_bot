""" Python File to handle reponses. """

# Imports
import json

# Import custom (mine) libraries
import moon_api

def read_settings(search):
	with open("files/settings.json", "r") as f:
		contents = json.load(f)
		try:
			result = contents[search]
			return result
		except KeyError:
			print("Error: Key not found or not existant, defaulting to '1' ...")
			print("Recommended Fix: Write Settings File correctly.")
			return 1

def handle_reponse(message):

	message_lower = message.lower()

	if message_lower[:1] == read_settings("prefix"):
		# Every Reponse should be a dictionary containing a True or False, if there are multiple messages.
		return handle_message(message_lower[1:])
	else:
		return {"message": False}


def handle_message(m):
	#reponse = {"message": False, "multiple": False, "message0": None, "message1": None}
	reponse = {"message": False, "multiple": False, "messages": {},}
	if m == "moon":
		reponse["message"] = True
		reponse["multiple"] = True
		reponse["messages"]["1text"] = f"Moon Phase of the {moon_api.get_current_date()} is: {moon_api.get_current_moonphase()}."
		reponse["messages"]["1image"] = moon_api.get_c_mphase_image()
		return reponse

if __name__ == "__main__":
	repons = handle_reponse("$moon")["messages"]
	print(list(repons.values())[0])
	#for i in repons.values():
		#print(i)