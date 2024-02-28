import asyncio
import sqlite3
import logging
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import TOKEN_API


async def user_db(user_id):
    db_name = f"user_{user_id}_todos.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            status TEXT,
            description TEXT,
            file_id TEXT,
            file_type TEXT
        )
    ''')
    conn.commit()
    return conn, cursor


logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN_API)
dp = Dispatcher()

class AddTaskStates(StatesGroup):
    task = State()
    description = State()
    status = State()
    file_id = State()


class DeleteTask(StatesGroup):
    waiting_for_delete = State()


class MoveTask(StatesGroup):
    move_number = State()
    move_choose = State()
    move_finish = State()


class ListTask(StatesGroup):
    show_full_task = State()


HELP_COMMANDS = """
<b>/start</b> - start bot.
<b>/add</b> - add task in todolist.
<b>/delete</b> - delete task in todolist.
<b>/move</b> - moved task in any status todolist.
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
    await message.answer("write <b>/help</b> to see a commands", parse_mode='HTML')
    await message.delete()


@dp.message(Command('add'))
async def add_task(message: types.Message, state: FSMContext):
    await message.answer('write ur task')
    await message.answer('write "/stop" to stop')
    await state.set_state(AddTaskStates.task)


@dp.message(AddTaskStates.task)
async def process_task(message: types.Message, state: FSMContext):
    task = message.text
    if message.text == '/stop':
        await message.answer('okay, bye')
        await state.clear()
        return
    if task:
        await state.update_data(task=task)
        await message.answer('write the description of the task')
        await message.answer('if not write "/skip"')
        await state.set_state(AddTaskStates.description)
    else:
        await message.answer("task cannot be empty. please write your task again.")

@dp.message(AddTaskStates.description)
async def process_descr(message: types.Message, state: FSMContext):
    if message.text == '/skip':
        description = 'nothing'
    else:
        description = message.text
    if description:
        await state.update_data(description=description)
        await message.answer('attach the file if you want.')
        await message.answer('if not write "/skip"')
        await state.set_state(AddTaskStates.file_id)
    else:
        await message.answer("description cannot be empty. please write your task again.")

@dp.message(AddTaskStates.file_id)
async def process_file(message: types.Message, state: FSMContext):
    file_id = None
    file_type = ""
    if message.document:
        file_id = message.document.file_id
        file_type = 'document'
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_type = 'photo'
    elif message.audio:
        file_id = message.audio.file_id
        file_type = 'audio'
    elif message.voice:
        file_id = message.voice.file_id
        file_type = 'voice'
    elif message.text == '/skip':
        await message.answer('okay, skip')
        await state.set_state(AddTaskStates.status)
    else:
        await message.reply("Please upload a file.")
        return

    await state.update_data(file_id=file_id)
    await state.update_data(file_type=file_type)
    await message.answer('write the status of task.')
    await state.set_state(AddTaskStates.status)
@dp.message(AddTaskStates.status)
async def process_status(message: types.Message, state: FSMContext):
    conn, cursor = await user_db(message.from_user.id)
    status = message.text.lower()
    if message.text == '/stop':
        await message.answer('okay, bye')
        await state.clear()
        return
    data = await state.get_data()
    task = data.get('task')
    description = data.get('description')
    file_id = data.get('file_id')
    file_type = data.get('file_type')
    cursor.execute('SELECT name FROM tasks WHERE name = ?', (task,))
    existing_task = cursor.fetchall()

    if existing_task:
        await message.answer('theres already such a task.')
        await state.clear()
        return
    cursor.execute('INSERT INTO tasks (name, status, description, file_id, file_type) VALUES (?, ?, ?, ?, ?)', (task, status, description, file_id, file_type))
    conn.commit()
    await message.answer('task added successfully!')
    await state.clear()


@dp.message(Command('list'))
async def show_tasks(message: types.Message, state: FSMContext):
    conn, cursor = await user_db(message.from_user.id)
    cursor.execute('SELECT id, name, status FROM tasks')
    tasks = cursor.fetchall()

    response = "Tasks:\n"
    total_index = 1
    for task in tasks:
        task_id, task_name, task_status = task
        response += f"{total_index}. <b>{task_name}</b> - <b>{task_status}</b>\n"
        total_index += 1

    await message.reply(response, parse_mode='HTML')

    await message.answer('To see the full info about a task, enter its number.')
    await message.answer('To cancel, enter "/stop".')
    await state.update_data(tasks=tasks)
    await state.set_state(ListTask.show_full_task)


@dp.message(ListTask.show_full_task)
async def show_info(message: types.Message, state: FSMContext):
    conn, cursor = await user_db(message.from_user.id)
    data = await state.get_data()
    tasks = data.get('tasks')

    if message.text == '/stop':
        await message.answer('Cancelled.')
        await state.clear()
        return

    try:
        task_number = int(message.text)
    except ValueError:
        await message.answer("Please enter a valid task number.")
        return

    if 1 <= task_number <= len(tasks):
        task_id, task_name, task_status = tasks[task_number - 1]

        cursor.execute('SELECT description, file_id, file_type FROM tasks WHERE id = ?', (task_id,))
        task_info = cursor.fetchone()
        task_description, file_id, file_type = task_info

        response = f"""
Task: {task_name}
Status: {task_status}
Description: {task_description}
Files:"""

        await message.answer(response)

        if file_type == 'document':
            await message.answer_document(file_id)
        elif file_type == 'photo':
            await message.answer_photo(file_id)
        elif file_type == 'audio':
            await message.answer_audio(file_id)
        elif file_type == 'voice':
            await message.answer_voice(file_id)
        else:
            await message.answer("No files attached.")

        await state.clear()
    else:
        await message.answer("Invalid task number.")

@dp.message(Command('delete'))
async def delete_task(message: types.Message, state: FSMContext):
    conn, cursor = await user_db(message.from_user.id)
    cursor.execute('SELECT id, name, status FROM tasks ')
    tasks = cursor.fetchall()

    if not tasks:
        await message.reply(f"there is not a single task")
        return

    response = "Tasks:\n"
    total_index = 1
    for task in tasks:
        task_id, task_name, task_status = task
        response += f"{total_index}. <b>{task_name}</b> - <b>{task_status}</b>\n"
        total_index += 1

    response += "enter the number of the task you want to delete:"
    await message.reply(response, parse_mode="HTML")
    await message.answer('write "/stop" to stop')
    await state.update_data(tasks=tasks)
    await state.set_state(DeleteTask.waiting_for_delete)


@dp.message(DeleteTask.waiting_for_delete)
async def process_task_number(message: types.Message, state: FSMContext):
    conn, cursor = await user_db(message.from_user.id)
    if message.text == '/stop':
        await message.answer('okay, bye')
        await state.clear()
        return

    try:
        task_number = int(message.text)
    except ValueError:
        await message.answer("Please enter a valid task number.")
        return

    data = await state.get_data()
    tasks = data.get('tasks')

    if 1 <= task_number <= len(tasks):
        task_id_to_delete = tasks[task_number - 1][0]
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id_to_delete,))
        conn.commit()
        await message.reply(f"task - '{tasks[task_number - 1][1]}' deleted successfully!")
        await state.clear()
    else:
        await message.reply("invalid task number.")


@dp.message(Command('move'))
async def move_task(message: types.Message, state: FSMContext):
    conn, cursor = await user_db(message.from_user.id)
    cursor.execute('SELECT id, name, status FROM tasks ')
    tasks = cursor.fetchall()

    if not tasks:
        await message.reply(f"there is not a single task")
        return

    response = "Tasks:\n"
    total_index = 1
    for task in tasks:
        task_id, task_name, task_status = task
        response += f"{total_index}. <b>{task_name}</b> - <b>{task_status}</b>\n"
        total_index += 1



    response += "enter the number of the task you want to move:"
    await message.reply(response, parse_mode='HTML')
    await message.answer('write "/stop" to stop')
    await state.update_data(tasks=tasks)
    await state.set_state(MoveTask.move_choose)


@dp.message(MoveTask.move_choose)
async def move_choose(message: types.Message, state: FSMContext):
    if message.text == '/stop':
        await message.answer('okay, bye')
        await state.clear()
        return

    try:
        task_number = int(message.text)
    except ValueError:
        await message.answer("Please enter a valid task number.")
        return

    data = await state.get_data()
    tasks = data.get('tasks')
    if 1 <= task_number <= len(tasks):
        await message.answer('enter the new status for the task')
        await state.update_data(tasks=tasks)
        await state.update_data(task_number=task_number)
        await state.set_state(MoveTask.move_finish)
    else:
        await message.reply("invalid task number.")


@dp.message(MoveTask.move_finish)
async def move_finish(message: types.Message, state: FSMContext):
    conn, cursor = await user_db(message.from_user.id)
    new_status = message.text.lower()

    if message.text == '/stop':
        await message.answer('okay, bye')
        await state.clear()
        return
    data = await state.get_data()
    tasks = data.get('tasks')
    task_number = data.get('task_number')
    task_id_to_move = tasks[task_number - 1][0]

    cursor.execute('SELECT name FROM tasks WHERE id = ?', (task_id_to_move,))
    task_name = cursor.fetchone()[0]
    cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id_to_move))
    conn.commit()
    await message.reply(f"task '{task_name}' moved to {new_status} successfully!")
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
