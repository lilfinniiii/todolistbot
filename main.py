import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import TOKEN_API

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN_API)
dp = Dispatcher()

user_todos = {'todo': [], 'doing': [], 'done': []}

HELP_COMMANDS = """
<b>/start</b> - start bot.
<b>/add [task] [status]</b> - add task in todolist.
<b>/delete [task] [status]</b> - delete task in todolist.
<b>/move [task] [new_status]</b> - moved task in any status todolist.
<b>/list</b> - show all tasks
<b>/help</b> - this commands.
<b>/contact</b> - send contact bot`s developer"""

@dp.message(Command('contact'))
async def contact_command(message: types.Message):
    await message.answer("""
    <b>telegram</b> - @lilfinniiii
<b>github</b> - https://github.com/lilfinniiii""", parse_mode='HTML')

@dp.message(Command('help'))
async def help_commands(message: types.Message):
    await message.answer(text=HELP_COMMANDS, parse_mode='HTML')

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer("yo, i`m to-do list bot :0")
    await message.delete()

@dp.message(Command('add'))
async def add_task(message: types.Message):
    args = message.text.split(maxsplit=2)
    if len(args) == 3:
        _, task, status = args
        task = args[1]
        if status in user_todos:
            user_todos[status].append(task)
            await message.reply(F"task '{task}' add in {status}.")
        else:
            await message.reply(f"status '{status}' not found")
    else:
        await message.reply("use command /add '[name task]' '[status]' for add task")

@dp.message(Command('list'))
async def show_tasks(message: types.Message):
    response = ""
    for status, tasks in user_todos.items():
        response += f"<b>**{status.capitalize()}**</b>:\n"
        for task in tasks:
            response += f"- {task}\n"
    await message.reply(response, parse_mode='HTML')

@dp.message(Command('delete'))
async def delete_task(message: types.Message):
    args = message.text.split(maxsplit=2)
    if len(args) == 3:
        _, task, status = args
        task = args[1]
        if status in user_todos:
            if task in user_todos[status]:
                user_todos[status].remove(task)
                await message.reply(F"task '{task}' in '{status}' deleted.")
                return
            else:
                await message.reply(F"task '{task}' in '{status}' not found.")
        else:
            await message.reply(f"status '{status}' not found.")
    else:
        await message.reply("use command /delete '[name task]' '[status]'for delete task.")

@dp.message(Command('move'))
async def move_task(message: types.Message):
    args = message.text.split(maxsplit=2)
    if len(args) == 3:
        _, task, new_status = args
        for status in user_todos:
            if new_status in user_todos:
                if task in user_todos[status]:
                    user_todos[status].remove(task)
                    user_todos[new_status].append(task)
                    await message.reply(f"task '{task}' moved in '{new_status}'.")
                    return
                else:
                    await message.reply(f"task '{task}' not found.")

        await message.reply(f"status '{new_status}' not found.")
    else:
        await message.reply("use /move '[name task]' '[status]' for move task.")






async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
