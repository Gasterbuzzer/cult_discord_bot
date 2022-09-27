# Main File for Discord Bot

# Imports
import discord

import respond_message

# Just some variables definitions

start_activity = "use $help for all commands."

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
		print(e)
		# Just if something bad happens, we can react and not crash.




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