""" Python File to handle responses. """

# Imports
import json
import re

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
        except KeyError:  # If Key does not exist or is not found, default to 1
            print("Error: Key not found or not existent, defaulting to '1' ...")
            print("Recommended Fix: Write Settings File correctly.")
            return 1


def handle_response(message, client):
    """Function to handling messages"""
    message_lower = message.lower()

    messages_all = re.findall(r"\w+", message_lower)
    messages_all_without_ = re.findall(r"\w+", message_lower[1:])

    if message_lower[:1] == read_settings("prefix"):
        # Every Response should be a dictionary containing a True or False, if there are multiple messages.
        return handle_message(message_lower[1:], messages_all, messages_all_without_, client)
    else:
        # If Message was not with a prefix, return no message
        return {"message": False}


def handle_message(m, all_m, all_m_without_, client_r):
    """ Method checking what the command was and sending appropriate Message """
    # Default Response layout, message is if there is a message, multiple is if there are multiple responses,
    # messages contains all messages
    response = {"message": False, "multiple": False, "messages": {}, }
    # Note to 'messages', every message and image included start with a number, representing their order (example:
    # 1text) this should be ignored, also there are only 'text' and 'image' responses until now, they get handled in
    # main.

    # Moon Command, gets current moon phase.
    if m == "moon":
        response["message"] = True
        response["multiple"] = True

        file = discord.File(f"{moon_api.get_c_mphase_image()}", filename="moon_phase.png")
        embed = discord.Embed(
            title="Today's Moon Phase: ",
            colour=discord.Colour.yellow(),
        )
        embed.set_footer(text="Sekte Bot")
        embed.set_image(url="attachment://moon_phase.png")

        # Get Moon Phase as text and return it as embed.
        embed.add_field(name=f"Date: ",
                        value=f"Moon Phase of {moon_api.get_current_date()} is **'{moon_api.get_current_moonphase()}'** ",
                        inline=False)
        response["messages"]["1embed"] = embed
        # Get Moon Phase Image and store it, returns a path
        response["messages"]["0e_image"] = file
        # Return Response
        return response

    # Fullmoon Command, gets the date for the full moon.
    if m == "fullmoon":
        response["message"] = True
        response["multiple"] = True

        file = discord.File("files/images/moon_lr.png", filename="moon.png")
        embed = discord.Embed(
            title="This month the fullmoon was:",
            colour=discord.Colour.yellow(),
        )
        embed.set_footer(text="Sekte Bot")
        embed.set_thumbnail(url="attachment://moon.png")

        fullmoon_day = moon_api.get_fullmoon()
        fullmoon_day_text = f"{fullmoon_day}{moon_api.get_ending_day(fullmoon_day)}"

        embed.add_field(name=f"The fullmoon was/is on the: ",
                        value=f"{fullmoon_day_text} of {moon_api.get_current_month_text()}.", inline=False)

        response["messages"]["1embed"] = embed
        response["messages"]["0e_image"] = file

        return response

    # Nextfullmoon Command, gets the next coming fullmoon.
    if m == "nextfullmoon":
        response["message"] = True
        response["multiple"] = True
        fullmoon_day = moon_api.get_fullmoon()

        file = discord.File("files/images/moon_lr.png", filename="moon.png")
        embed = discord.Embed(
            title="Next Fullmoon is on the:",
            colour=discord.Colour.yellow(),
        )
        embed.set_footer(text="Sekte Bot")
        embed.set_thumbnail(url="attachment://moon.png")

        if not moon_api.is_fullmoon_over(fullmoon_day):
            # Get fullmoon of current month.
            print("Debug Log: Sending Fullmoon of this month.")
            fullmoon_day_text = f"{fullmoon_day}{moon_api.get_ending_day(fullmoon_day)}"

            embed.add_field(name=f"Date: ", value=f"{fullmoon_day_text} of {moon_api.get_current_month_text()}.",
                            inline=False)

            response["messages"]["1embed"] = embed
            response["messages"]["0e_image"] = file
        else:
            # Get fullmoon of next month.
            print(f"Debug Log: Sending Fullmoon of next month ({moon_api.get_next_month_current()}).")
            fullmoon_day = moon_api.get_fullmoon(month=moon_api.get_next_month_current())
            fullmoon_day_text = f"{fullmoon_day}{moon_api.get_ending_day(fullmoon_day)}"

            embed.add_field(name=f"Date: ",
                            value=f"{fullmoon_day_text} of {moon_api.get_given_month_text(month=moon_api.get_next_month_current())}.",
                            inline=False)

            response["messages"]["1embed"] = embed
            response["messages"]["0e_image"] = file

        return response

    # Help Command to show all commands.
    if m == "help":
        response["message"] = True
        response["multiple"] = True

        prefix = read_settings("prefix")

        file = discord.File("files/images/pfp.png", filename="image.png")
        embed = discord.Embed(
            title="All Commands:",
            description="List of all commands in the bot.",
            colour=discord.Colour.yellow(),
        )

        embed.add_field(name=f"{prefix}help", value="Show all commands. (This here)", inline=False)
        embed.add_field(name=f"{prefix}moon", value="Show the **'current'** Moon State", inline=False)
        embed.add_field(name=f"{prefix}fullmoon", value="Show when the fullmoon this month **'was'**.", inline=False)
        embed.add_field(name=f"{prefix}nextfullmoon",
                        value="Show when the next fullmoon is **'coming'** in the future.", inline=False)

        embed.set_thumbnail(
            url="attachment://image.png")  # Use the attachment url inorder to use local files and/or images

        embed.set_footer(text="Sekte Bot Help")

        response["messages"]["1embed"] = embed
        response["messages"]["0e_image"] = file
        return response

    # Command to get data of a specified user.
    if all_m_without_[0] == "getuser":
        response["message"] = True
        response["multiple"] = True
        if len(all_m_without_) > 2:
            return raise_error(1, response)

        id_u = int(all_m_without_[1])

        response["messages"]["1text"] = f"User: " + str(client_r.get_user(id_u))
        # print(f"Debug Log: User Test Found: {str(client_r.get_user(214730164813299712))}") A test to see if works.
        print(f"Debug Log: User Found: {str(client_r.get_user(id_u))}")
        return response

    # Test Command to see all parameters.
    if all_m_without_[0] == "test":
        response["message"] = True
        response["multiple"] = True
        print(f"Debug Log: All Input: {all_m_without_}")

        response["messages"]["1text"] = "Input in Console."
        return response

    # If Command is empty
    if m == "":
        response_fallback = {"message": False}
        return response_fallback


# Displays an error if called to the user.
def raise_error(number, _response):
    _response["message"] = True
    _response["multiple"] = True
    if number == 1:
        _response["messages"]["1text"] = "Error: Unexpected size, please use command correctly."
        print(_response)
        return _response


# Debugging
if __name__ == "__main__":
    # Is used to test different responses.
    response = handle_response("$nextfullmoon", discord.Client())
    print(list(response.values())[0])
# for i in response.values():
# print(i)
