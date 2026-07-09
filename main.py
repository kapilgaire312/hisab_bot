import os

import discord
from dotenv import load_dotenv

load_dotenv()


intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)

# initialize tree to use slash commands
tree = discord.app_commands.CommandTree(client=client)


# targeting a specific server is faster when developing.
guild_id = os.getenv("GUILD_ID")
GUILD = discord.Object(id=guild_id)


@tree.command(name="next", guild=GUILD)
async def next(interaction, sender: str, receiver: str, value: str):
    print(sender, receiver)
    print(value)
    await interaction.response.send_message("sup")


@client.event
async def on_ready():
    try:
        synced = await tree.sync(
            guild=GUILD
        )  # register the slash command  #initializing the slash command in specific sever only
        print(f"Synced {len(synced)} commands")
        for cmd in synced:
            print(cmd.name)

    except Exception as e:
        print(e)
    print(f"ready: {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.mention_everyone:
        return

    if client.user not in message.mentions:
        return

    print(message.content)
    first_word = message.content.split(maxsplit=1)[0]
    application_id = "<@" + str(client.application_id) + ">"

    try:
        if first_word == application_id:
            print("true")
            split_words = message.content.split(maxsplit=2)
            print(split_words)

            match split_words[1]:
                case "--help":
                    await message.channel.send("So you need help, huh?")

                case "--format":
                    await message.channel.send("format of what, huh?")

                case _:
                    raise ValueError("Choose a valid option")

        else:
            raise ValueError("Choose a valid option")
    except ValueError:
        await message.channel.send(
            "Enter a valid command. Use '@HisabBot --help' for help."
        )

    except Exception as e:
        print(e)
        await message.channel.send("Failed to make changes, erorr occures.")


token = os.getenv("BOT_TOKEN")
client.run(token)
