# Main File for Discord Bot

# Import Default

import json

# Import Custom libraries
import discord

# Import my librariers
import respond_message

# Just some variables definitions

start_activity = "use $help for all commands."

path_user = "files/users/"

# Defining functions to use, much easier if done so.

# This is complicated, so many comments
async def send_message(message, user_message):
	"""Sends message to channel"""
	try:
		# From repond_message we get what to answer. This gets stored.
		reponse = respond_message.handle_reponse(user_message)

		#await message.author.send(reponse) For private message

		# If there is an reponse, we answer.
		if reponse["message"] == True:
			if reponse["multiple"] == True: # If there are multiple reponses, do this

				print(f"Chat Sending Log: Sending multiple things: ")

				for i in reponse["messages"]:
					# We loop through all messages and react according to what type they are (image or text)
					# We must remove/ignore the first number infront of type, so that we can check it, the number is for order, is not important for printing however.

					if i[1:] == "text": 
						# If text send the text to the channel.
						await message.channel.send(reponse["messages"][i])
						print(f"\tText: '{reponse['messages'][i]}'")

					elif i[1:] == "image":
						# Send Image if image. Does not show in console for obvious resons.
						# Image location is the return.
						await message.channel.send(file=discord.File(reponse['messages'][i]))
						print(f"\tImage: Image in Channel (Not showing in console) (Image Location: {reponse['messages'][i]})")

					elif i[1:] == "embed":
						# Send embed.
						embed = reponse['messages'][i]

						# Incase there is no file or image.
						try:
							file = reponse['messages']['0e_image']
						except:
							file = None

						if file: # Check if file exists, if not ignore.	

							await message.channel.send(file=file, embed=embed)
							print(f"\tEmbed: Embed with image send to channel.")
						else:
							await message.channel.send(embed=embed)
							print(f"\tEmbed: Embed send to channel.")

					elif i[1:] == "e_image":
						# Ignore if the object is e_image.
						continue

			else:
				# If theres only one respond, only send that. Does not support images for now.
				print(f"Chat Sending Log: Sending message/image: {reponse['messages']}")
				await message.channel.send(list(reponse["messages"].values())[0])

	except Exception as e:
		print("Error could not send message.")
		print(f"Error Log: {e}")
		# Just if something bad happens, we can react and not crash.


async def gain_exp_user(author):
	"""Function that gives an user xp."""
	# Default (0) EXP and Rank:
	username = str(author)
	data_to_save = {"username": username, "exp": 0, "rank": 0,}
	exp = data_to_save["exp"]
	rank = data_to_save["rank"]

	# Creating path to user file.
	path = path_user + f"{username}.json"
	try:
		with open(path, "r") as f:
			# Load the data of user.
			data = json.load(f)
			data_to_save["rank"] = data["rank"]
			# Trying to load user data if existant
			try:
				exp = data["exp"]
			except:
				exp = 1

			# Increase EXP
			exp += 1

			data_to_save["exp"] = exp
			# Save the file.
			with open(path, "w") as f:
				json.dump(data_to_save, f)

	except Exception as e:
		print(f"Debug Log: File for user was not found, creating a new one for {username}.")
		#print(f"Error Log: Error detail: {e}")
		with open(path, "w") as f:
			# Write data if not found.
			data_to_save["exp"] = 1

			# Get rank (no rank = 0)
			# Rank "The Gravekeeper of the fith" = 1
			# Rank "The Quatroguards" = 2
			# Rank "The third prayer" = 3
			# Rank "The second circle" = 4
			# Rank "The choosen ascending" = 5
			# Rank "One of the first" = 6

			# If we can't find a role, we default to 0
			role_found = False

			for role in author.roles:
				# Loop through roles and find the ones.
				if role.id == 817941435998535689:
					data_to_save["rank"] = 1
					role_found = True
					break
				elif role.id == 817940839404797982:
					data_to_save["rank"] = 2
					role_found = True
					break
				elif role.id == 815231250843435018:
					data_to_save["rank"] = 3
					role_found = True
					break
				elif role.id == 817935867829682236: # We load 5 earlier, since it could appear earlier than expected.
					data_to_save["rank"] = 5
					role_found = True
					break
				elif role.id == 815230234411532288:
					data_to_save["rank"] = 4
					role_found = True
					break	
				elif role.id == 815015673935691816:
					data_to_save["rank"] = 6
					role_found = True
					break
				else:
					continue

			if role_found == False:
				data_to_save["rank"] = 0

			json.dump(data_to_save, f)

# Bot stuff here.

def run_bot():
	"""Runs the bot and enables all asyncs."""
	print(f"Debug Log: Project from 'https://github.com/Gasterbuzzer/cult_discord_bot'.")
	# Enable intents
	intents = discord.Intents.all()
	intents.message_content = True
	client = discord.Client(intents=intents, activity=discord.Game(name=start_activity))

	@client.event
	async def on_ready():
		"""When bot is ready"""
		print(f"Debug Log: Bot logged in as '{client.user}'.")
		print(f"Debug Log: Bot set status to '{start_activity}'.")

	@client.event
	async def on_message(message):
		"""If message happens."""
		# Check if message is the bot, if yes ignore it.
		if message.author == client.user:
			return

		# Check message, getting info for that.
		username = str(message.author)
		user_message = str(message.content)
		channel = str(message.channel)
		print(f"Chat Message Log: '{username}' has send the message '{user_message}' in '{channel}'.")

		# Note that message is the give parameter from the event async, user_message is just a string from it.
		await send_message(message, user_message)
		await gain_exp_user(message.author)

	# Read Bot Token from File.
	token = None
	print("Debug Log: Reading token from discordt.txt ...")
	with open("files/discordt.txt") as f:
		token = f.read()
		print("Debug Log: Token grabbed.")
		
	# Start Bot
	print("Debug Log: Bot is starting to run...")
	client.run(token)
	

# Main
if __name__ == "__main__":
	# Start Bot if file is started as main.
	run_bot()