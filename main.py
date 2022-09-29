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
async def send_message(message, user_message, client):
    """Sends message to channel"""
    try:
        # From respond_message we get what to answer. This gets stored.
        response = respond_message.handle_response(user_message, client, message)

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
                        except ValueError:
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
            with open(path, "w") as f:
                json.dump(data_to_save, f)

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
        await send_message(message, user_message, client)
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
