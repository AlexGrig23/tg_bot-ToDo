import datetime

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler


TOKEN_BOT = "5663964204:AAFvjDaFZblWdEx_8LFYfAqNHtpfA1mmZ74"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

categories = ["products", "entertainment", "health", "auto"]


class FileHandlerSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.filename = "example.txt"
        return cls._instance

    def append_line(self, line):
        with open(self.filename, "a") as f:
            f.write(line)

    def read_lines(self):
        with open(self.filename, "r") as f:
            lines = f.readlines()
        return lines

    def overwrite_file(self, lines):
        with open(self.filename, "w") as f:
            for line in lines:
                f.write(line + "\n")


async def start(update: Update, context: CallbackContext) -> None:
    logging.info("Command start was triggered")
    await update.message.reply_text("Welcom to my ToDo list Bot\n"
                                    "Command\n"
                                    "See categories expenses: /cat\n"
                                    "Add expenses: /add_ex <categories> | <expenses>\n"
                                    "See  expenses: /list_ex [<month>]\n"
                                    "Add income: /add_in <categories income> | <profit>\n"
                                    "See  income: /list_in [<month>]\n"
                                    "See all information /list\n"
                                    "Remove expenses or income: /remove <number expensive or income>\n"
                                    "See statistic catgories for day or month, or year:\n"
                                    "/statistic <categories> [| <date_start> | <date_end>]"
                                    )


async def cat(update: Update, context: CallbackContext) -> None:
    """
    Format add cat command
    /cat
    """
    await update.message.reply_text("\n".join(categories))


async def add_ex(update: Update, context: CallbackContext) -> None:
    """
    Format add add_ex command
    /add_ex <categories> | <expenses>
    """
    await update.message.reply_text("Enter your expenses: Categories, sum of expesses")

    ex = "cost"
    ex_parts = "".join(context.args).split("|")
    ex_cat = ex_parts[0].strip()
    expen = ex_parts[1].strip()
    today = datetime.date.today()

    if ex_cat not in categories:
        logging.error("Invalid category")
        await update.message.reply_text("You enter invalid category, check category comand '/cat'")
        return

    if not expen.isdigit():
        logging.error("Invalid value")
        await update.message.reply_text("You enter invalid value, enter digit")
        return

    file_handler = FileHandlerSingleton()
    lines = file_handler.read_lines()
    print(lines)
    if lines and len(lines) > 0:
        last_line_number = int(lines[-1].split()[0])
    else:
        last_line_number = 0

    new_line_number = last_line_number + 1
    new_line = f"{new_line_number}"

    user_data = [ex_cat, expen, today.strftime('%d.%m.%Y')]

    file_handler.append_line(new_line + ' ' + " | ".join(user_data) + " | " + ex + "\n")
    await update.message.reply_text(f"Expenses {' '.join(user_data)} append successfully")


async def list_ex(update: Update, context: CallbackContext) -> None:
    """
    Format add list_ex command
    /list_ex [<month>]
    """
    ex = "cost"
    file_handler = FileHandlerSingleton()
    lines = file_handler.read_lines()

    target_month = update.message.text.strip().split()[-1]
    if target_month.isdigit():
        target_month = int(target_month)
    else:
        target_month = None

    filter_lines = []
    for line in lines:
        part = line.split("|")
        if len(part) >= 3:
            date_string = part[2].strip()
            date = datetime.datetime.strptime(date_string, "%d.%m.%Y")

            if target_month is None and ex in line:
                filter_lines.append(line)

            elif date.month == target_month and ex in line:
                filter_lines.append(line)

    if filter_lines:
        await update.message.reply_text("".join(filter_lines))
    else:
        await update.message.reply_text("You don't have expenses")


async def list_in(update: Update, context: CallbackContext) -> None:
    """
    Format add list_in command
    /list_in [<month>]
    """
    inc = "profit"
    file_handler = FileHandlerSingleton()
    lines = file_handler.read_lines()

    target_month = update.message.text.strip().split()[-1]
    if target_month.isdigit():
        target_month = int(target_month)
    else:
        target_month = None

    filter_lines = []
    for line in lines:
        part = line.split("|")
        if len(part) >= 3:
            date_string = part[2].strip()
            date = datetime.datetime.strptime(date_string, "%d.%m.%Y")

            if target_month is None and inc in line:
                filter_lines.append(line)

            elif date.month == target_month and inc in line:
                filter_lines.append(line)

    if filter_lines:
        await update.message.reply_text("".join(filter_lines))
    else:
        await update.message.reply_text("You don't have expenses")


async def add_in(update: Update, context: CallbackContext) -> None:
    """
    Format add add_in command
    /add_in <categories income> | <profit>
    """
    await update.message.reply_text("Enter your incoming: Categories, sum incoming")

    inc = "profit"
    inc_parts = "".join(context.args).split("|")
    inc_cat = inc_parts[0].strip()
    incomin = inc_parts[1].strip()
    today = datetime.date.today()
    data_incoming = [inc_cat, incomin, today.strftime('%d.%m.%Y')]

    if not inc_cat.isalpha():
        logging.error("Invalid category")
        await update.message.reply_text("You enter invalid category, enter text")
        return

    if not incomin.isdigit():
        logging.error("Invalid value")
        await update.message.reply_text("You enter invalid value, enter digit")
        return

    file_handler = FileHandlerSingleton()
    lines = file_handler.read_lines()
    print(lines)
    if lines and len(lines) > 0:
        last_line_number = int(lines[-1].split()[0])
    else:
        last_line_number = 0

    new_line_number = last_line_number + 1
    new_line = f"{new_line_number}"

    file_handler.append_line(new_line + " " + " | ".join(data_incoming) + " | " + inc)
    await update.message.reply_text(f"Expenses {' '.join(data_incoming)} append successfully")


async def list(update: Update, context: CallbackContext) -> None:
    file_handler = FileHandlerSingleton()
    lines = file_handler.read_lines()
    await update.message.reply_text(" ".join(lines))


async def remove(update: Update, context: CallbackContext) -> None:
    """
    Format add remove command
    /remove <number expensive or income>
    """
    try:
        remove_idx = int(context.args[0])

        file_handler = FileHandlerSingleton()
        lines = file_handler.read_lines()
        idx = False
        for line in lines:
            if line.startswith(str(remove_idx)):
                idx = True
                break
        if not idx:
            await update.message.reply_text(f"You don't have cost with number {remove_idx}")
            return

        file_handler = FileHandlerSingleton()
        file_handler.overwrite_file([line for line in lines if not line.startswith(str(remove_idx))])
        await update.message.reply_text(f"You have successfully deleted costs under number {remove_idx}")

    except (ValueError, IndexError):
        await update.message.reply_text("You entered an invalid number or you don't entered number")


async def statistic(update: Update, context: CallbackContext) -> None:
    """
    Format add statistic command
    /statistic <categories> [| <date_start> | <date_end>]
    """

    stat_parts = "".join(context.args).split("|")
    stat_cat = stat_parts[0].strip()
    statistic_data = []
    if len(stat_parts) == 1:
        file_handler = FileHandlerSingleton()
        lines = file_handler.read_lines()
        for line in lines:
            if stat_cat == line.split("|")[0].split()[1]:
                statistic_data.append(line)
        await update.message.reply_text("".join(statistic_data))

    if len(stat_parts) >= 2:
        try:
            start_date = datetime.datetime.strptime(stat_parts[1].strip(), "%d.%m.%Y")
            if len(stat_parts) >= 3:
                end_date = datetime.datetime.strptime(stat_parts[2].strip(), "%d.%m.%Y")
            else:
                end_date = None
        except ValueError:
            logging.error("Invalid date format")
            await update.message.reply_text("Your date argument is not valid ")
            return

        file_handler = FileHandlerSingleton()
        lines = file_handler.read_lines()
        for line in lines:
            part = line.split("|")
            date_string = part[2].strip()
            date = datetime.datetime.strptime(date_string, "%d.%m.%Y")
            if end_date is None:
                if start_date == date:
                    statistic_data.append(line)
            else:
                if start_date <= date <= end_date:
                    statistic_data.append(line)

        await update.message.reply_text("".join(statistic_data))


def run():
    app = ApplicationBuilder().token(TOKEN_BOT).build()
    logging.info("Application build succesfully")

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('cat', cat))
    app.add_handler(CommandHandler('add_ex', add_ex))
    app.add_handler(CommandHandler("add_in", add_in))
    app.add_handler(CommandHandler("list_ex", list_ex))
    app.add_handler(CommandHandler("remove", remove))
    app.add_handler(CommandHandler("list", list))
    app.add_handler(CommandHandler("list_in", list_in))
    app.add_handler(CommandHandler("statistic", statistic))
    app.run_polling()


if __name__ == "__main__":
    run()
