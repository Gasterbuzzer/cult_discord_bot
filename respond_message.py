""" Python File to handle responses. """

# Imports
import json
import re

# Imports other library
import discord

# Import custom (mine) libraries
import moon_api
import rank_lib
import main


def read_settings(search):
    """Read Settings Values with given parameter"""

    is_dev = main.get_dev()

    if not is_dev:
        path_settings = "files/settings.json"
    else:
        path_settings = "files/settings_dev.json"

    try:
        with open(path_settings, "r") as f:
            contents = json.load(f)
            try:
                result = contents[search]
                return result
            except KeyError:  # If Key does not exist or is not found, default to 1
                print("Error: Key not found or not existent, defaulting to '1' ...")
                print("Recommended Fix: Write Settings File correctly.")
                return 1
    except FileNotFoundError:
        with open(path_settings, "w") as f:
            contents_ = {"prefix": "$"}
            json.dump(contents_, f)
            print(f"Dev Log: {path_settings} not found, creating one...")


def create_userfile(client_r, id_u, path, data, member_guild):
    # Create user file
    is_new = True
    print(f"Debug Log: File for user was not found, creating a new one for {str(client_r.get_user(id_u))}.")
    with open(path, "w") as f:
        # Write data if not found.
        data["exp"] = 0

        # Get rank (no rank = 0)
        # Rank "The Gravekeeper of the fifth" = 1
        # Rank "The Quatroguards" = 2
        # Rank "The third prayer" = 3
        # Rank "The second circle" = 4
        # Rank "The choosen ascending" = 5
        # Rank "One of the first" = 6

        # If we can't find a role, we default to 0
        role_found = False

        for role in member_guild.roles:
            # Loop through roles and find the ones.
            if role.id == 817941435998535689:
                data["rank"] = 1
                role_found = True
                break
            elif role.id == 817940839404797982:
                data["rank"] = 2
                role_found = True
                break
            elif role.id == 815231250843435018:
                data["rank"] = 3
                role_found = True
                break
            elif role.id == 817935867829682236:  # We load 5 earlier, since it could appear earlier than
                # expected.
                data["rank"] = 5
                role_found = True
                break
            elif role.id == 815230234411532288:
                data["rank"] = 4
                role_found = True
                break
            elif role.id == 815015673935691816:
                data["rank"] = 6
                role_found = True
                break
            elif role.id == 826114593830993933:
                data["rank"] = 7
                role_found = True
            else:
                continue

        if not role_found:
            data["rank"] = 0

        json.dump(data, f)
        return is_new


def handle_response(message, client, message_object, author):
    """Function to handling messages"""
    message_lower = message.lower()

    messages_all = re.findall(r"\w+", message_lower)
    messages_all_without_ = re.findall(r"\w+", message_lower[1:])

    if message_lower[:1] == read_settings("prefix"):
        # Every Response should be a dictionary containing a True or False, if there are multiple messages.
        return handle_message(message_lower[1:], messages_all, messages_all_without_, client, message_object, author)
    else:
        # If Message was not with a prefix, return no message
        return {"message": False}


def handle_message(m, all_m, all_m_without_, client_r, message_object, author):
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
    elif m == "fullmoon":
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
    elif m == "nextfullmoon":
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
    elif m == "help":
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

        embed.add_field(name=f"{prefix}getuser", value="Shows the EXP and Rank of a User in the server.", inline=True)
        embed.add_field(name=f"Example", value=f"**'{prefix}getuser @Lucas**'", inline=True)

        embed.add_field(name=chr(173), value=chr(173))

        embed.add_field(name=f"{prefix}rankup", value="**Admin**: Rank up user if he has 100 EXP.", inline=True)
        embed.add_field(name=f"Example", value=f"**'{prefix}rankup @Lucas**'", inline=True)

        embed.add_field(name=chr(173), value=chr(173))

        embed.add_field(name=f"{prefix}derank", value="**Admin**: Derank user if he has less than 100 EXP.",
                        inline=True)
        embed.add_field(name=f"Example", value=f"**'{prefix}derank @Lucas**'", inline=True)

        embed.add_field(name=chr(173), value=chr(173))

        embed.add_field(name=f"{prefix}ritual", value="Start a ritual in your current voice channel!",
                        inline=False)

        embed.set_thumbnail(
            url="attachment://image.png")  # Use the attachment url inorder to use local files and/or images

        embed.set_footer(text="Sekte Bot Help")

        response["messages"]["1embed"] = embed
        response["messages"]["0e_image"] = file
        return response

    # Command to get data of a specified user.
    elif all_m_without_[0] == "getuser":
        response["message"] = True
        response["multiple"] = True
        if not len(all_m_without_) == 2:
            return raise_error(1, response, all_m_without_[2:], m, len(all_m_without_) - 1, 1)
        try:
            id_u = int(all_m_without_[1])
        except ValueError:
            return raise_error(2, response, all_m_without_[1], m)

        member_guild = message_object.guild.get_member(id_u)
        embed = discord.Embed(
            title=f"User {str(client_r.get_user(id_u))}:",
            colour=discord.Colour.yellow(),
        )
        embed.set_footer(text="Sekte Bot")

        path = "files/users/" + f"{str(client_r.get_user(id_u))}.json"
        data = {"username": str(client_r.get_user(id_u)), "exp": 0, "rank": 0}
        is_new = False
        try:
            with open(path, "r") as f:
                # Load the data of user.
                data = json.load(f)
                rank = data["rank"]
                exp = data["exp"]
        except FileNotFoundError:
            is_new = create_userfile(client_r, id_u, path, data, member_guild)

        if is_new:
            with open(path, "r") as f:
                # Load the data of user.
                data = json.load(f)
                rank = data["rank"]
                exp = data["exp"]

        rank_name = "No rank"
        rank_name = rank_lib.get_rank(rank)

        # Add fields.
        embed.add_field(name=f"EXP: ",
                        value=f"**{exp}**",
                        inline=True)

        embed.add_field(name=f"Rank: ",
                        value=f"**'{rank_name}'**",
                        inline=True)

        # Gets url of avatar, yes I suffered finding the url out.
        url_a = member_guild.avatar.url
        # print(url_a)

        # Old but could be helpful
        # url = f"https://cdn.discordapp.com/avatars/{member_guild.id}/{member_guild.avatar.url}.png?size=1024"
        # urllib.request.urlretrieve(url, "files/images/member.png")
        # file = discord.File("files/images/member.png", filename="member.png")

        embed.set_image(url=url_a)

        response["messages"]["1embed"] = embed

        response["messages"]["0e2_image"] = url_a

        # print(f"Debug Log: User Test Found: {str(client_r.get_user(214730164813299712))}") A test to see if works.
        # print(f"Debug Log: User Found: {str(client_r.get_user(id_u))}")
        return response

    elif all_m_without_[0] == "rankup":
        # Ranks up user if he has 100 messages.
        response["message"] = True
        response["multiple"] = True

        if not len(all_m_without_) == 2:
            return raise_error(1, response, all_m_without_[2:], m, len(all_m_without_) - 1, 1)
        try:
            id_u = int(all_m_without_[1])
        except ValueError:
            return raise_error(2, response, all_m_without_[1], m)

        permission_role = False
        for role in author.roles:
            if role.id == rank_lib.get_rank_id(8):
                permission_role = True

        if not permission_role:
            return raise_error(6, response, all_m_without_[1], m, client_r=client_r, id_u=id_u)

        member_guild = message_object.guild.get_member(id_u)
        embed = discord.Embed(
            title=f"User {str(client_r.get_user(id_u))} has been Ranked up!",
            colour=discord.Colour.yellow(),
        )
        embed.set_footer(text="Sekte Bot")

        path = "files/users/" + f"{str(client_r.get_user(id_u))}.json"
        data = {"username": str(client_r.get_user(id_u)), "exp": 0, "rank": 0}
        is_new = False
        try:
            with open(path, "r") as f:
                # Load the data of user.
                data = json.load(f)
                rank = data["rank"]
                exp = data["exp"]
        except FileNotFoundError:
            is_new = create_userfile(client_r, id_u, path, data, member_guild)

        if is_new:
            with open(path, "r") as f:
                # Load the data of user.
                data = json.load(f)
                rank = data["rank"]
                exp = data["exp"]

        if rank == 0:
            rank += 1
            exp = 0
        elif exp >= 100:
            rank += 1
            exp = 0
        else:
            return raise_error(3, response, all_m_without_[1], m, client_r=client_r, id_u=id_u)

        rank_name = rank_lib.get_rank(rank)

        try:
            with open(path, "w") as f:
                # Load the data of user.
                data["rank"] = rank
                data["exp"] = exp
                json.dump(data, f)
        except FileNotFoundError:
            print("Error Log: Could not find file even if created.")

        # Add fields.
        embed.add_field(name=f"User is now rank: ",
                        value=f"**{rank_name}**",
                        inline=True)

        embed.add_field(name=f"**Congrats to your new Rank**",
                        value=f"**'{str(client_r.get_user(id_u))}'**",
                        inline=True)

        embed.add_field(name=f"**Note: This is currently a test, not ranking up.**",
                        value=f"**'Test'**",
                        inline=False)

        url_a = member_guild.avatar.url

        embed.set_image(url=url_a)

        response["messages"]["1embed"] = embed

        response["messages"]["0e2_image"] = url_a

        response["messages"]["1action"] = {"action": "addrole", "member": member_guild,
                                           "role": rank_lib.get_rank_id(rank), "user_id": id_u}
        response["messages"]["2action"] = {"action": "removerole", "member": member_guild,
                                           "role": rank_lib.get_rank_id(rank - 1), "user_id": id_u}

        return response

    elif all_m_without_[0] == "derank":
        # Ranks up user if he has 100 messages.
        response["message"] = True
        response["multiple"] = True

        if not len(all_m_without_) == 2:
            return raise_error(1, response, all_m_without_[2:], m, len(all_m_without_) - 1, 1)
        try:
            id_u = int(all_m_without_[1])
        except ValueError:
            return raise_error(2, response, all_m_without_[1], m)

        permission_role = False
        for role in author.roles:
            if role.id == rank_lib.get_rank_id(8):
                permission_role = True

        if not permission_role:
            return raise_error(6, response, all_m_without_[1], m, client_r=client_r, id_u=id_u)

        member_guild = message_object.guild.get_member(id_u)
        embed = discord.Embed(
            title=f"User {str(client_r.get_user(id_u))} has been deranked up.",
            colour=discord.Colour.red(),
        )
        embed.set_footer(text="Sekte Bot")

        path = "files/users/" + f"{str(client_r.get_user(id_u))}.json"
        data = {"username": str(client_r.get_user(id_u)), "exp": 0, "rank": 0}
        is_new = False
        try:
            with open(path, "r") as f:
                # Load the data of user.
                data = json.load(f)
                rank = data["rank"]
                exp = data["exp"]
        except FileNotFoundError:
            is_new = create_userfile(client_r, id_u, path, data, member_guild)

        if is_new:
            with open(path, "r") as f:
                # Load the data of user.
                data = json.load(f)
                rank = data["rank"]
                exp = data["exp"]

        if rank == 0:
            return raise_error(5, response, all_m_without_[1], m, client_r=client_r, id_u=id_u)
        elif exp <= 100:
            rank -= 1
            exp = 0
        else:
            return raise_error(4, response, all_m_without_[1], m, client_r=client_r, id_u=id_u)

        rank_name = rank_lib.get_rank(rank)

        try:
            with open(path, "w") as f:
                # Load the data of user.
                data["rank"] = rank
                data["exp"] = exp
                json.dump(data, f)
        except FileNotFoundError:
            print("Error Log: Could not find file even if created.")

        # Add fields.
        embed.add_field(name=f"User has been derank to: ",
                        value=f"**{rank_name}**",
                        inline=True)

        embed.add_field(name=f"**Note: This is currently a test, not deranking.**",
                        value=f"**'Test'**",
                        inline=False)

        url_a = member_guild.avatar.url

        embed.set_image(url=url_a)

        response["messages"]["1embed"] = embed

        response["messages"]["0e2_image"] = url_a

        response["messages"]["1action"] = {"action": "removerole", "member": member_guild,
                                           "role": rank_lib.get_rank_id(rank), "user_id": id_u}
        response["messages"]["2action"] = {"action": "addrole", "member": member_guild,
                                           "role": rank_lib.get_rank_id(rank - 1), "user_id": id_u}

        return response

    # Test Command to see all parameters.
    elif all_m_without_[0] == "ritual":
        response["message"] = True
        response["multiple"] = True

        # The command must be run while the user is in a voice channel.

        if not author.voice:
            return raise_error(7, response, all_m_without_[0], m)

        # We check if the Bot is already connected to the channel of the user, if yes, we disconnect.
        for voice in client_r.voice_clients:
            if voice.channel.id == author.voice.channel.id:
                response["messages"]["1action"] = {"action": "disconnect", "VoiceClient": voice}

                embed = discord.Embed(
                    title=f"Disconnected from the Voice Channel.",
                    description="Bot has disconnected from the current Voice Channel.",
                    colour=discord.Colour.yellow(),
                )
                embed.set_footer(text="Sekte Bot")

                response["messages"]["1embed"] = embed

                return response

        # If the Bot was not in any of the channels that the user called, then join the user and display a message.
        response["messages"]["1action"] = {"action": "connect", "VoiceChannel": author.voice.channel}

        embed = discord.Embed(
            title=f"Connected to the voice channel **{author.voice.channel.name}**.",
            description="Bot joined the voice channel and is now starting the ritual.",
            colour=discord.Colour.yellow(),
        )
        embed.set_footer(text="Sekte Bot")

        response["messages"]["1embed"] = embed

        response["messages"]["1embed"] = embed

        return response

    elif all_m_without_[0] == "test2":
        response["message"] = True
        response["multiple"] = True

        try:
            id_u = int(all_m_without_[1])
        except ValueError:
            return raise_error(2, response, all_m_without_[1], m)

        member_guild = message_object.guild.get_member(id_u)

        response["messages"]["1action"] = {"action": "removerole", "member": member_guild,
                                           "role": rank_lib.get_rank_id(-1), "user_id": id_u}
        response["messages"]["2action"] = {"action": "addrole", "member": member_guild,
                                           "role": rank_lib.get_rank_id(-2), "user_id": id_u}
        return response

    # If Command is empty
    elif m == "":
        response_fallback = {"message": False}
        return response_fallback

    # Incase nothing happens just ignore it.
    response_fallback = {"message": False}
    return response_fallback


# Displays an error if called to the user.
def raise_error(number, _response, problem, full_command, amount_problem=1, amount_normal=1, client_r=None, id_u=0):
    _response["message"] = True
    _response["multiple"] = True
    if number == 1:
        embed = discord.Embed(
            title="Error:",
            description="Got too many arguments in command.",
            colour=discord.Colour.red(),
        )
        embed.set_footer(text="Sekte Bot")

        embed.add_field(name=f"Your Command: ",
                        value=f"**'{full_command}'**",
                        inline=False)

        error_text = f""
        for error in problem:
            error_text += f"\n**'{error}'**"

        embed.add_field(name=f"Only expected {amount_normal} but got {amount_problem} instead: ",
                        value=f"{error_text}",
                        inline=False)
        _response["messages"]["1embed"] = embed

        return _response
    elif number == 2:
        embed = discord.Embed(
            title="Error:",
            description="You did not provide a Username",
            colour=discord.Colour.red(),
        )
        embed.set_footer(text="Sekte Bot")

        embed.add_field(name=f"Your Command: ",
                        value=f"**'{full_command}'**",
                        inline=False)

        embed.add_field(name=f"Expected Username (Example @SekteBot) but did not get Username: ",
                        value=f"{problem}",
                        inline=False)
        _response["messages"]["1embed"] = embed

        return _response
    elif number == 3:
        embed = discord.Embed(
            title="Error:",
            description=f"The User {str(client_r.get_user(id_u))} cannot rank up.",
            colour=discord.Colour.red(),
        )
        embed.set_footer(text="Sekte Bot")

        embed.add_field(name=f"The User {str(client_r.get_user(id_u))}: ",
                        value=f"Does not have 100 EXP to rank up.",
                        inline=False)

        _response["messages"]["1embed"] = embed

        return _response
    elif number == 4:
        embed = discord.Embed(
            title="Error:",
            description=f"The User {str(client_r.get_user(id_u))} cannot be deranked.",
            colour=discord.Colour.red(),
        )
        embed.set_footer(text="Sekte Bot")

        embed.add_field(name=f"The User {str(client_r.get_user(id_u))}: ",
                        value=f"Has more than 100 exp, therefore cannot be deranked.",
                        inline=False)

        _response["messages"]["1embed"] = embed

        return _response
    elif number == 5:
        embed = discord.Embed(
            title="Error:",
            description=f"The User {str(client_r.get_user(id_u))} is already the lowest rank.",
            colour=discord.Colour.red(),
        )
        embed.set_footer(text="Sekte Bot")

        embed.add_field(name=f"The User {str(client_r.get_user(id_u))}: ",
                        value=f"Has either no rank or is too low of a rank to be deranked.",
                        inline=False)

        _response["messages"]["1embed"] = embed

        return _response
    elif number == 6:
        embed = discord.Embed(
            title="Error:",
            description=f"You do not have the permission to use this command.",
            colour=discord.Colour.red(),
        )
        embed.set_footer(text="Sekte Bot")

        embed.add_field(name=f"This command requires higher permission: ",
                        value=f"If this is wrong, contact your administrator.",
                        inline=False)

        _response["messages"]["1embed"] = embed

        return _response
    elif number == 7:
        embed = discord.Embed(
            title="Error:",
            description=f"You are not in a voice channel.",
            colour=discord.Colour.red(),
        )
        embed.set_footer(text="Sekte Bot")

        embed.add_field(name=f"Not in a voice channel: ",
                        value=f"You must be in a voice channel in order to call this command.",
                        inline=False)

        _response["messages"]["1embed"] = embed

        return _response


# Debugging
if __name__ == "__main__":
    # Is used to test different responses.
    # response = handle_response("$nextfullmoon", discord.Client())
    # print(list(response.values())[0])
    print("True")
# for i in response.values():
# print(i)
