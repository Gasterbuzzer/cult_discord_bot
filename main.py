# Main File for Discord Bot

# Imports
import discord

import respond_message

# Just some functions

start_activity = "with your feelings."

# Defining functions to use, much easier if done so.

async def send_message(message, user_message):
	try:
		# From repond_message we get what to answer. This gets stored.
		reponse = respond_message.handle_reponse(user_message)

		#await message.author.send(reponse) For private message

		# If there is an reponse, we answer.
		if reponse["message"] == True:
			if reponse["multiple"] == True:

				print(f"Chat Sending Log: Sending multiple things: ")

				for i in reponse["messages"]:

					if i[1:] == "text":
						await message.channel.send(reponse["messages"][i])
						print(f"\tText: '{reponse['messages'][i]}'")

					elif i[1:] == "image":
						# Image location is in given string.
						await message.channel.send(file=discord.File(reponse['messages'][i]))
						print(f"\tImage: Image in Channel (Not showing in console) (Image Location: {reponse['messages'][i]})")

			else:

				print(f"Chat Sending Log: Sending message/image: {reponse['messages']}")
				await message.channel.send(list(reponse["messages"].values())[0])

	except Exception as e:
		print(e)
		# Just if something bad happens, we can react and not crash.

# Bot stuff here.

def run_bot():
	"""Runs the bot and enables all asyncs."""
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
	

if __name__ == "__main__":
	# Start Bot if file is started as main.
	run_bot()