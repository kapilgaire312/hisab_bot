# Hisab Bot

Hisab Bot is a Discord expense-tracking bot for shared groups. It lets a server team register members, log shared expenses and repayments, inspect balances, view transaction history, and export records to CSV.

## Features

- Initialize a server member list directly from Discord.
- Add shared expenses with per-participant shares.
- Record repayments between members.
- View balances, transaction history, and all transactions.
- Export all transactions as a CSV report.
- Delete individual expenses or repayments when needed.
- Reset the active history window with a cleared timestamp.

## Requirements

- Python 3.13 or newer
- A PostgreSQL database
- A Discord bot application with the `message content` and `members` intents enabled
- A guild where the bot is invited and slash commands can be synced

## Environment Variables

Create a `.env` file in the project root with these values:

```env
BOT_TOKEN=your_discord_bot_token
GUILD_ID=your_target_discord_server_id
DEFAULT_DB_NAME=postgres
BOT_DB_NAME=hisab_bot
DB_CONNECTION_STRING=postgresql://user:password@host:5432/hisab_bot

```

- `BOT_TOKEN` is the Discord bot token.
- `GUILD_ID` is the Discord server where slash commands are registered.
- `DB_CONNECTION_STRING` should point to a PostgreSQL connection that can create databases and should end with `/hisab_bot` instead of the default `/postgres` database.
- `DEFAULT_DB_NAME` is the admin database used while creating and deleting the bot database.
- `BOT_DB_NAME` is the database name created for Hisab Bot data.

## Setup

1. Install dependencies.

```bash
uv sync
```

2. Configure your `.env` file with the values above.

3. Start the bot.

```bash
uv run python main.py
```

If you are not using `uv`, install the dependencies from `pyproject.toml` with your preferred tool and run `python main.py`.

## Slash Commands

Commands are registered in the configured guild when the bot starts.

### Help and Setup

- `/help` - Show the command reference.
- `/initiliaze_bot` - Initialize the bot with all non-bot members in the server.
- `/initiliaze_bot_with_exception exclude:<members>` - Initialize the bot while excluding specific members.
- `/clear_records` - Reset the active history window starting now.
- `/delete_database` - Permanently delete the bot database.

### Expenses and Payments

- `/expense payer:<member> description:<text> amount:<number> participants:<member:share,...>` - Add a shared expense.
- `/repay receiver:<member> amount:<number> note:<text>` - Record a repayment.
- `/delete id:<e123|p456>` - Delete an expense or repayment by ID.

### Reports

- `/balance user:<member>` - Show what a member owes and who owes them.
- `/history user:<member>` - Show a member's transaction history since the last clear.
- `/history_all` - Show all transactions since the last clear.
- `/members_list` - Show the members that were registered during initialization.
- `/export_transactions` - Export all transactions as a CSV file.

## Usage Notes

- Only moderators or administrators can initialize the bot or delete the database.
- Expense participants must be members that were registered during initialization.
- Expense participant input uses Discord mentions with shares, for example `@user1:50,@user2:25`.
- The bot only tracks activity after the latest cleared timestamp.
- Transaction IDs use an `e` prefix for expenses and a `p` prefix for repayments.

## Limitations

- The bot is designed to work with one Discord server at a time.
- Adding the bot to multiple servers can mix data in the database, so it should be used for a single server only.

## Database Model

The bot creates and uses these core tables:

- `users`
- `expenses`
- `expense_participants`
- `repayments`
- `cleared_date`

## Project Structure

- `main.py` - Discord client and slash-command registration.
- `database/` - PostgreSQL connection and query layer.
- `wrappers/` - Business logic for each bot command.
- `utils/` - Shared helpers, validation, and custom errors.

