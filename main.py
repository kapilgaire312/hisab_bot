import os

import discord
from dotenv import load_dotenv

from database.handlers import delete_database
from wrappers.add_expense_and_repayments import add_expense, add_repayment
from wrappers.initialize_bot import handle_initialize_bot
from wrappers.show_history import show_history
from wrappers.show_member_balance import show_balance

load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


client = discord.Client(intents=intents)

# initialize tree to use slash commands
tree = discord.app_commands.CommandTree(client=client)


# targeting a specific server is faster when developing.
guild_id = os.getenv("GUILD_ID")
GUILD = discord.Object(id=guild_id)


@tree.command(
    name="initiliazebot",
    description="Initialize the bot with all the members in the server.",
    guild=GUILD,
)
async def initialize_bot(interaction):
    response = handle_initialize_bot(interaction=interaction)
    await interaction.response.send_message(f"{response['message']}")


@tree.command(
    name="initiliazebotwithexception",
    description="Initialize the bot by excluding certain members.",
    guild=GUILD,
)
async def initialize_bot_with_exception(interaction, exclude: str):
    response = handle_initialize_bot(interaction=interaction, exception_members=exclude)
    await interaction.response.send_message(f"{response['message']}")


@tree.command(
    name="deletedb",
    description="!!!!Delete the entire database. This cant be undone. Export a copy first.",
    guild=GUILD,
)
async def delete_db(interaction):
    delete_database()
    await interaction.response.send_message("Entire database deleted successfully.")


@tree.command(name="expense", description="Add new shared expense.", guild=GUILD)
async def expense(
    interaction,
    payer: discord.Member,
    description: str,
    amount: float,
    participants: str,
):
    print(interaction.user.id, description)
    print(amount, participants)
    response = add_expense(
        payer_id=payer.id,
        description=description,
        amount=amount,
        listed_by=interaction.user.id,
        participants=participants,
    )
    await interaction.response.send_message(f"{response['message']}")


@tree.command(name="repay", description="Log repayment info to the bot.", guild=GUILD)
async def repay(interaction, receiver: discord.Member, amount: float, note: str):
    response = add_repayment(interaction.user.id, receiver.id, amount, note)
    await interaction.response.send_message(f"{response['message']}")


@tree.command(
    name="balance", description="Shows how much debt/credit a user has.", guild=GUILD
)
async def balance(interaction, user: discord.Member):
    response = show_balance(member_id=user.id)
    await interaction.response.send_message(f"{response['message']}")


@tree.command(
    name="history",
    description="Shows all user transactions from last cleared date.",
    guild=GUILD,
)
async def history(interaction, user: discord.Member):
    response = show_history(member_id=user.id)
    await interaction.response.send_message(f"{response['message']}")


@tree.command(
    name="historyall",
    description="Shows all transactions from last cleared date.",
    guild=GUILD,
)
async def historyall(interaction):
    respose = show_history()
    await interaction.response.send_message(respose["message"])


@tree.command(
    name="delete",
    description="Delete a expense using its id.",
    guild=GUILD,
)
async def delete_expense(interaction, id: str):
    await interaction.response.send_message("the expense was deleted successfully.")


@tree.command(
    name="export",
    description="Export all data since initialization as csv.",
    guild=GUILD,
)
async def export(interaction):
    await interaction.response.send_message("Your file will be exported.")


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

    if message.reference is not None:  # if the message is a reply
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
