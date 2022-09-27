""" Python File to handle reponses. """

# Imports
import json

# Imports other library
import discord

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

		file = discord.File(f"{moon_api.get_c_mphase_image()}", filename="moon_phase.png")
		embed = discord.Embed(
			title = "Today's Moon Phase: ",
			colour = discord.Colour.yellow(),
			)
		embed.set_footer(text="Sekte Bot")
		embed.set_image(url="attachment://moon_phase.png")

		# Get Moon Phase as text and return it as embed.
		embed.add_field(name=f"Date: ", value=f"Moon Phase of {moon_api.get_current_date()} is **'{moon_api.get_current_moonphase()}'** ", inline = False)
		reponse["messages"]["1embed"] = embed
		# Get Moon Phase Image and store it, returns a path
		reponse["messages"]["0e_image"] = file
		# Return Reponse
		return reponse

	# Fullmoon Command, gets the date for the full moon.
	if m == "fullmoon":
		reponse["message"] = True
		reponse["multiple"] = True

		file = discord.File("files/images/moon_lr.png", filename="moon.png")
		embed = discord.Embed(
			title = "This month the fullmoon was:",
			colour = discord.Colour.yellow(),
			)
		embed.set_footer(text="Sekte Bot")
		embed.set_thumbnail(url="attachment://moon.png")

		
		fullmoon_day = moon_api.get_fullmoon()
		fullmoon_day_text = f"{fullmoon_day}{moon_api.get_ending_day(fullmoon_day)}"

		embed.add_field(name=f"The fullmoon was/is on the: ", value=f"{fullmoon_day_text} of {moon_api.get_current_month_text()}.", inline = False)

		reponse["messages"]["1embed"] = embed
		reponse["messages"]["0e_image"] = file

		return reponse

	# Nextfullmoon Command, gets the next coming fullmoon.
	if m == "nextfullmoon":
		reponse["message"] = True
		reponse["multiple"] = True
		fullmoon_day = moon_api.get_fullmoon()

		file = discord.File("files/images/moon_lr.png", filename="moon.png")
		embed = discord.Embed(
			title = "Next Fullmoon is on the:",
			colour = discord.Colour.yellow(),
			)
		embed.set_footer(text="Sekte Bot")
		embed.set_thumbnail(url="attachment://moon.png")

		if not moon_api.is_fullmoon_over(fullmoon_day):
			# Get fullmoon of current month.
			print("Debug Log: Sending Fullmoon of this month.")
			fullmoon_day_text = f"{fullmoon_day}{moon_api.get_ending_day(fullmoon_day)}"

			embed.add_field(name=f"Date: ", value=f"{fullmoon_day_text} of {moon_api.get_current_month_text()}.", inline = False)

			reponse["messages"]["1embed"] = embed
			reponse["messages"]["0e_image"] = file
		else:
			# Get fullmoon of next month.
			print(f"Debug Log: Sending Fullmoon of next month ({moon_api.get_next_month_current()}).")
			fullmoon_day = moon_api.get_fullmoon(month=moon_api.get_next_month_current())
			fullmoon_day_text = f"{fullmoon_day}{moon_api.get_ending_day(fullmoon_day)}"

			embed.add_field(name=f"Date: ", value=f"{fullmoon_day_text} of {moon_api.get_given_month_text(month=moon_api.get_next_month_current())}.", inline = False)

			reponse["messages"]["1embed"] = embed
			reponse["messages"]["0e_image"] = file

		return reponse

	# Help Command to show all commands.
	if m == "help":
		reponse["message"] = True
		reponse["multiple"] = True

		prefix = read_settings("prefix")

		file = discord.File("files/images/pfp.png", filename="image.png")
		embed = discord.Embed(
			title = "All Commands:",
			description = "List of all commands in the bot.",
			colour = discord.Colour.yellow(),
			)

		embed.add_field(name=f"{prefix}help", value="Show all commands. (This here)", inline = False)
		embed.add_field(name=f"{prefix}moon", value="Show the **'current'** Moon State", inline = False)
		embed.add_field(name=f"{prefix}fullmoon", value="Show when the fullmoon this month **'was'**.", inline = False)
		embed.add_field(name=f"{prefix}nextfullmoon", value="Show when the next fullmoon is **'coming'** in the future.", inline = False)

		embed.set_thumbnail(url="attachment://image.png") #Use the attachment url inorder to use local files and/or images

		embed.set_footer(text="Sekte Bot Help")

		reponse["messages"]["1embed"] = embed
		reponse["messages"]["0e_image"] = file
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