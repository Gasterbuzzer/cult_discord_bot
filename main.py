# Main File for Discord Bot

# Import Default

import json

# Import Custom libraries
import discord
from discord.ext import tasks
from discord import app_commands

import reminder_api
# Import my libraries
import respond_message

# Just some variables definitions

start_activity = "use $help for all commands."

path_user = "files/users/"


# Defining functions to use, much easier if done so.

# This is complicated, so many comments
async def send_message(message, user_message, client, author):
    """Sends message to channel"""
    try:
        # From respond_message we get what to answer. This gets stored.
        response = respond_message.handle_response(user_message, client, message, author)

        # await message.author.send(response) For private message

        # If there is a response, we answer.
        if response["message"]:
            # If there are multiple responses, do this
            if response["multiple"]:

                print(f"Chat Sending Log: Sending multiple things: ")

                for i in response["messages"]:
                    # We loop through all messages and react according to what type they are (image or text) We must
                    # remove/ignore the first number in front of type, so that we can check it, the number is for
                    # order, is not important for printing, however.

                    if i[1:] == "text":
                        # If text send the text to the channel.
                        await message.channel.send(response["messages"][i])
                        print(f"\tText: '{response['messages'][i]}'")

                    elif i[1:] == "image":
                        # Send Image if it is an image. Does not show in console for obvious response.
                        # Image location is the return.
                        await message.channel.send(file=discord.File(response['messages'][i]))
                        print(
                            f"\tImage: Image in Channel (Not showing in console) (Image Location: {response['messages'][i]})")

                    elif i[1:] == "embed":
                        # Send embed.
                        embed = response['messages'][i]

                        # Incase there is no file or image.
                        try:
                            file = response['messages']['0e_image']
                        except Exception:
                            file = None

                        # Check if file exists, if not ignore.
                        if file:
                            await message.channel.send(file=file, embed=embed)
                            print(f"\tEmbed: Embed with image send to channel.")
                        else:
                            await message.channel.send(embed=embed)
                            print(f"\tEmbed: Embed send to channel.")

                    elif i[1:] == "e_image":
                        # Ignore if the object is e_image.
                        continue
                    elif i[1:] == "action":
                        # If an action is required that must be called async or whatever.
                        if response['messages'][i]['action'] == "addrole":
                            # Default Layout {"action": "addrole", "member": member_guild, "role":
                            # rank_lib.get_rank_id(rank), "user_id": id_u}

                            guild_member = response['messages'][i]['member']
                            rank = response['messages'][i]['role']
                            rank_role = message.guild.get_role(rank)
                            user_id = response['messages'][i]['user_id']
                            username = str(client.get_user(user_id))

                            await guild_member.add_roles(rank_role, reason="User ranked up.")
                            print(f"Debug Log: Added Role: {rank} for {username}")

                        elif response['messages'][i]['action'] == "removerole":
                            # Remove Roll from user

                            guild_member = response['messages'][i]['member']
                            rank = response['messages'][i]['role']
                            rank_role = message.guild.get_role(rank)
                            user_id = response['messages'][i]['user_id']
                            username = str(client.get_user(user_id))

                            await guild_member.remove_roles(rank_role, reason="User ranked up.")
                            print(f"Debug Log: Removed Role: {rank} for {username}")

                        elif response['messages'][i]['action'] == "sendprivatemessage":
                            # Send private message to user.
                            user = client.get_user(response["messages"][i]["user_id"])
                            text = response["messages"][i]["message"]
                            await user.send(text)
                            print(f"Debug Log: Send private message to user.")

                        elif response['messages'][i]['action'] == "connect":
                            # Join a given channel. (Template: {"action": "connect", "VoiceChannel":
                            # author.voice.channel})

                            voice_channel = response["messages"][i]["VoiceChannel"]
                            vc = await voice_channel.connect()

                            print(f"Debug Log: Connected to voice channel **{voice_channel.name}**")

                        elif response['messages'][i]['action'] == "disconnect":
                            # Disconnect from an active channel. (Template: {"action": "disconnect", "VoiceClient":
                            # voice})
                            voice_client = response["messages"][i]["VoiceClient"]
                            print("\n\tDebug Log: Stopping music...")
                            voice_client.stop()
                            print("\n\tDebug Log: Disconnecting from voice channel...\n")
                            await voice_client.disconnect()
                            print(f"Debug Log: Disconnected from Voice Channel: **{voice_client.channel.name}**")

                        elif response['messages'][i]['action'] == "play":
                            # Plays a song based on the location and given player.
                            # Default music source="files/audio/music.mp3"

                            voice_channel = response["messages"][i]["VoiceChannel"]

                            for voice in client.voice_clients:
                                if voice.channel.id == voice_channel.id:
                                    _voice_client = voice
                                    _voice_client.play(
                                        discord.FFmpegPCMAudio(source=response["messages"][i]["music_path"]))
                                    break
                                else:
                                    print("Error Log: Bot is not in the voice channel and this cannot play the song.")

                        continue

            else:
                # If there's only one respond, only send that. Does not support images for now.
                print(f"Chat Sending Log: Sending message/image: {response['messages']}")
                await message.channel.send(list(response["messages"].values())[0])

    except Exception as e:
        print("Error could not send message.")
        print(f"Error Log: {e}")

    # print(e)
    # Just if something bad happens, we can react and not crash.


# except ValueError:
# print("What")

def get_dev():
    try:
        with open("dev.json", "r") as f:
            info = json.load(f)
            return info["dev"]
    except FileNotFoundError:
        with open("dev.json", "w") as f:
            info = {"dev": False}
            json.dump(info, f)
            print("Debug Log: Dev file not found, creating one...")
            return False


async def gain_exp_user(author):
    """Function that gives a user xp."""
    # Default (0) EXP and Rank:
    username = str(author)
    data_to_save = {"username": username, "exp": 0, "rank": 0, }
    exp = data_to_save["exp"]
    rank = data_to_save["rank"]

    # Creating path to user file.
    path = path_user + f"{username}.json"
    try:
        with open(path, "r") as f:
            # Load the data of user.
            data = json.load(f)
            data_to_save["rank"] = data["rank"]
            # Trying to load user data if existent
            exp = data["exp"]
            # Increase EXP
            exp += 1

            data_to_save["exp"] = exp
            # Save the file.
            with open(path, "w") as f_:
                json.dump(data_to_save, f_)

    except FileNotFoundError:
        print(f"Debug Log: File for user was not found, creating a new one for {username}.")
        # print(f"Error Log: Error detail: {e}")
        with open(path, "w") as f:
            # Write data if not found.
            data_to_save["exp"] = 1

            # Get rank (no rank = 0)
            # Rank "The Gravekeeper of the fifth" = 1
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
                elif role.id == 817935867829682236:  # We load 5 earlier, since it could appear earlier than expected.
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
                elif role.id == 826114593830993933:
                    data["rank"] = 7
                    role_found = True
                else:
                    continue

            if not role_found:
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
    tree = app_commands.CommandTree(client)

    @tasks.loop(hours=24.0)
    async def send_message_to_me():

        print(f"Debug Log: 24 Hours Loop Finished: ")
        await reminder_api.update_days()

        user = client.get_user(659890824783462411)
        channel = client.get_channel(815248996062462042)

        file = discord.File("files/images/moon_re.png", filename="image.png")
        embed = discord.Embed(
            title="Fullmoon Reminder:",
            description="@everyone Your friendly fullmoon reminder.",
            colour=discord.Colour.yellow(),
        )
        embed.add_field(name=f"**Fullmoon is in: {reminder_api.days_to_fullmoon() - 1} days.**", value="This reminder "
                                                                                                       "will not "
                                                                                                       "appear "
                                                                                                       "again.",
                        inline=False)
        embed.set_thumbnail(
            url="attachment://image.png")  # Use the attachment url inorder to use local files and/or images
        embed.set_footer(text="Sekte Bot Remind")

        if reminder_api.need_remind():

            print(f"\tDebug Log: Reminding User that fullmoon is near.")

            await channel.send(embed=embed, file=file)
            print("\tDebug Log: Sent message to channel chat.")

            # This step is repeated incase the first one gets closed by python bruh
            file = discord.File("files/images/moon_re.png", filename="image.png")
            embed.set_thumbnail(
                url="attachment://image.png")  # Use the attachment url inorder to use local files and/or images

            await user.send(embed=embed, file=file)
            print("\tDebug Log: Sent message to user...")

            reminder_api.was_reminded(True)
        else:
            if reminder_api.need_remind() and reminder_api.is_reminded():
                print(f"\tDebug Log: Not Reminding, since there is still {reminder_api.days_to_fullmoon()} days.")
            elif not reminder_api.is_reminded() and not reminder_api.need_remind():
                print(f"\tDebug Log: Not Reminding, since there is still {reminder_api.days_to_fullmoon()} days. "
                      f"\n\tUpdating file to represent this...")
                reminder_api.was_reminded(False)
                print("\tInfo: Set Reminded = False in file.")
            elif not reminder_api.need_remind() and reminder_api.is_reminded():
                print(f"\tDebug Log: Not Reminding, since there is still {reminder_api.days_to_fullmoon()} days.")

        print("Debug Log: Resuming normal operations...")

    @client.event
    async def on_ready():
        """When bot is ready"""
        print(f"Debug Log: Bot logged in as '{client.user}'.")
        print(f"Debug Log: Bot set status to '{start_activity}'.")
        if not get_dev():
            send_message_to_me.start()
        else:
            print(f"\n\n DEV Log: Developer environment found, some functionality is disabled. \n\n")
        # App Commands.
        try:
            synced = await tree.sync(guild=None)
            print(f"Debug Log: Synced slash commands with Command Tree.")
        except Exception as e:
            print(f"Error Log: Encountered Error while syncing:  {e}.")

    # A slash command for help.
    @tree.command(name="help", description="Displays help info of discord bot.", nsfw=False, guild=None)
    async def helps(interaction: discord.Interaction):
        print(f"Debug Log: Slash Command 'help' was used.")

        response = respond_message.handle_response(message="help", client=client, message_object=interaction.message,
                                                   author=interaction.user, ignore_prefix=True)

        embed = response['messages']["1embed"]
        file = response['messages']['0e_image']

        await interaction.response.send_message(embed=embed, file=file, ephemeral=True)

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
        await send_message(message, user_message, client, message.author)
        await gain_exp_user(message.author)

    # Read Bot Token from File.
    if get_dev():
        path = "files/discordt_dev.txt"
        filename = "discordt_dev.txt"
    else:
        path = "files/discordt.txt"
        filename = "discordt.txt"
    token = None
    try:
        print(f"Debug Log: Reading token from {filename} ...")
        with open(path) as f:
            token = f.read()
            print("Debug Log: Token grabbed.")
    except FileNotFoundError:
        print(f"\n\nCritical Error: File {filename} was not found in files folder.\n"
              "This file should contain one line with the bot token.\n\n")
        input()
        raise SystemExit()

    # Start Bot
    print("Debug Log: Bot is starting to run...")
    client.run(token)


# Main
if __name__ == "__main__":
    # Start Bot if file is started as main.
    run_bot()
