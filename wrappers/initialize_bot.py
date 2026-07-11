# wrapper for initializing bot

import logging

import discord
from psycopg.errors import DuplicateDatabase

from database.handlers import create_database, initialize_users_table
from utils.custom_errors import DatabaseCreationFailedError, UserTableInitializeError
from utils.utils import get_member_id_from_string

# instantiate logger
logger = logging.getLogger(__name__)


def handle_initialize_bot(
    interaction: discord.Interaction, exception_members: str = ""
):
    # first create database and table:
    try:
        create_database()

        members = get_guild_members(
            interaction=interaction, exception_members=exception_members
        )

        if len(members) < 2:
            return {
                "error": True,
                "message": "There needs to be atleast two members to initialize the bot.",
            }

        initialize_users_table(members)

        member_name = []
        for member in members:
            member_name.append(member[1])

        return {
            "error": False,
            "message": f"Hisab Bot initialized successfully for members: {', '.join(member_name)}",
        }

    except DatabaseCreationFailedError as e:
        cause = e.__cause__
        if isinstance(cause, DuplicateDatabase):
            logger.warning("Database already exists.")
            return {
                "error": True,
                "message": "Database already exists. Delete it to reinitialize.",
            }

        logger.error(e)
        return {"error": True, "message": "Unexpected error occured creating database."}

    except UserTableInitializeError as e:
        logger.error(e)
        return {"error": True, "message": "Failed to initialize members."}

    except Exception as e:
        logger.error(e)

        return {"error": True, "message": "Failed to initialize the database."}


def get_guild_members(interaction: discord.Interaction, exception_members: str):
    members = interaction.guild.members
    exception_member_ids = get_member_id_from_string(exception_members)
    pruned_members = []
    for member in members:
        if member.id not in exception_member_ids:
            if member.bot is False:
                name = member.global_name or member.name
                print(name)
                pruned_members.append((member.id, name))

    return pruned_members
