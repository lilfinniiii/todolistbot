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
            status TEXT
        )
    ''')
    conn.commit()
    return conn, cursor






logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN_API)
dp = Dispatcher()

valid_statuses = ['todo', 'doing', 'done']



class AddTaskStates(StatesGroup):
    task = State()
    status = State()

class DeleteTask(StatesGroup):
    waiting_for_status = State()
    waiting_for_delete = State()

class MoveTask(StatesGroup):
    move_status = State()
    move_number = State()
    move_choose = State()
    move_finish = State()

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
async def add_task(message: types.Message, state: FSMContext):
    await message.answer('write ur task')
    await state.set_state(AddTaskStates.task)
@dp.message(AddTaskStates.task)
async def process_task(message: types.Message, state: FSMContext):
    task = message.text
    if task:
        await state.update_data(task=task)
        await message.answer('write the status of the task')
        await state.set_state(AddTaskStates.status)
    else:
        await message.answer("task cannot be empty. please write your task again.")
@dp.message(AddTaskStates.status)
async def process_status(message: types.Message, state: FSMContext):
    conn, cursor = await user_db(message.from_user.id)
    status = message.text
    if status in valid_statuses:
        await state.update_data(status=status)
        data = await state.get_data()
        task = data.get('task')
        cursor.execute('SELECT name FROM tasks WHERE name = ?', (task,))
        existing_task  = cursor.fetchall()
        if existing_task:
            await message.answer('theres already such a task.')
            await state.clear()
            return
        cursor.execute('INSERT INTO tasks (name, status) VALUES (?, ?)', (task, status))
        conn.commit()
        await message.answer('task added successfully!')
        await state.clear()
    else:
        await message.answer(f"'status '{status}' not found'")
@dp.message(Command('list'))
async def show_tasks(message: types.Message):
    conn, cursor = await user_db(message.from_user.id)
    cursor.execute('SELECT name, status FROM tasks')
    tasks = cursor.fetchall()

    response = ""
    for status in valid_statuses:
        response += f"<b>**{status.capitalize()}**</b>:\n"
        for task in tasks:
            if task[1] == status:
                response += f"- {task[0]}\n"

    await message.reply(response, parse_mode='HTML')


@dp.message(Command('delete'))
async def delete_task(message: types.Message, state: FSMContext):
    await message.answer('write status for delete')
    await state.set_state((DeleteTask.waiting_for_status))

@dp.message(DeleteTask.waiting_for_status)
async def process_delete(message: types.Message, state: FSMContext):
    conn, cursor = await user_db(message.from_user.id)
    status = message.text.lower()

    if status not in valid_statuses:
        await message.reply("invalid status. please enter one of: 'todo', 'doing', 'done'.")
        return

    cursor.execute('SELECT id, name FROM tasks WHERE status = ?', (status,))
    tasks = cursor.fetchall()

    if not tasks:
        await message.reply(f"no tasks in the {status} status.")
        return

    response = f"Tasks in {status} status:\n"
    for index, task in enumerate(tasks, start=1):
        task_id, task_name = task
        response += f"{index}. {task_name}\n"

    response += "enter the number of the task you want to delete:"
    await message.reply(response)
    await state.update_data(tasks=tasks)
    await state.set_state(DeleteTask.waiting_for_delete)

@dp.message(DeleteTask.waiting_for_delete)
async def process_task_number(message: types.Message, state: FSMContext):
    conn, cursor = await user_db(message.from_user.id)
    task_number = int(message.text)
    data = await state.get_data()
    tasks = data.get('tasks')

    if 1 <= task_number <= len(tasks):
        task_id_to_delete = tasks[task_number - 1][0]
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id_to_delete,))
        conn.commit()
        await message.reply(f"task - {tasks[task_number - 1][0]} deleted successfully!")
        await state.clear()
    else:
        await message.reply("invalid task number.")



@dp.message(Command('move'))
async def move_task(message: types.Message, state: FSMContext):
    await message.answer('write status for move')
    await state.set_state((MoveTask.move_status))

@dp.message(MoveTask.move_status)
async def move_status(message: types.Message, state: FSMContext):
    conn, cursor = await user_db(message.from_user.id)
    status = message.text.lower()

    if status not in valid_statuses:
        await message.reply("invalid status. please enter one of: 'todo', 'doing', 'done'.")
        return

    cursor.execute('SELECT id, name FROM tasks WHERE status = ?', (status,))
    tasks = cursor.fetchall()

    if not tasks:
        await message.reply(f"No tasks in the {status} status.")
        return

    response = f"tasks in {status} status:\n"
    for index, task in enumerate(tasks, start=1):
        task_id, task_name = task
        response += f"{index}. {task_name}\n"

    response += "enter the number of the task you want to move:"
    await message.reply(response)
    await state.update_data(tasks=tasks)
    await state.set_state(MoveTask.move_choose)

@dp.message(MoveTask.move_choose)
async def move_choose(message: types.Message, state: FSMContext):
    task_number = int(message.text)
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
    data = await state.get_data()
    tasks = data.get('tasks')
    task_number = data.get('task_number')

    if new_status in valid_statuses:
        task_id_to_move = tasks[task_number - 1][0]
        cursor.execute('SELECT name FROM tasks WHERE id = ?', (task_id_to_move,))
        task_name = cursor.fetchone()[0]
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id_to_move))
        conn.commit()
        await message.reply(f"task {task_name} moved to {new_status} successfully!")
        await state.clear()
    else:
        await message.reply("invalid new status.")











async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
