# Документація TodoListBot UA ver.

## Огляд:
TodoListBot - це Telegram-бот, призначений для допомоги користувачам ефективно керувати своїми списками справ. Він надає функціонал, такий як додавання, видалення та переміщення завдань між різними статусами у списку справ. Цей бот спрощує управління завданнями, надаючи зручний інтерфейс користувача в додатку Telegram.

## Початок роботи:
1. **Запуск бота**: Розпочніть, шукаючи `@liltodolistbot` у Telegram та розпочніть розмову, відправивши команду `/start`.
2. **Команди**:
    - `/add [завдання] [статус]`: Додати нове завдання до списку справ із вказаним статусом.
    - `/delete [завдання] [статус]`: Видалити завдання зі списку справ за описом та статусом.
    - `/move [завдання] [новий_статус]`: Перемістіть завдання у новий статус у списку справ.
    - `/help` або `/commands`: Показати доступні команди та інструкції з використання.

## Деталі команд:
1. **/add [завдання] [статус]**:
    - Приклад: `/add Переглянути-зворотній-зв'язок doing`
    - Опис: Додає нове завдання з вказаним описом та присвоює йому вказаний статус.

2. **/delete [завдання] [статус]**:
    - Приклад: `/delete Переглянути-зворотній-зв'язок doing`
    - Опис: Видаляє завдання з вказаним описом та статусом із списку справ.

3. **/move [завдання] [новий_статус]**:
    - Приклад: `/move Переглянути-зворотній-зв'язок done`
    - Опис: Переміщує завдання з вказаним описом у новий статус у списку справ.

4. **/help** або **/commands**:
    - Опис: Показати список доступних команд разом із інструкціями їх використання.

## Приклад використання:
- **Додавання завдання**: `/add Переглянути-зворотній-зв'язок doing`
- **Видалення завдання**: `/delete Переглянути-зворотній-зв'язок doing`
- **Переміщення завдання**: `/move Переглянути-зворотній-зв'язок done`

## Примітка:
- Переконайтеся, що завдання описані точно, щоб уникнути непорозумінь під час операцій з керування завданнями.
- Використовуйте відповідні ключові слова статусу (наприклад, У розробці, В процесі, Завершено), щоб ефективно класифікувати завдання.

## Зворотній зв'язок та підтримка:
- Для будь-яких запитань, зауважень або допомоги не соромтеся зв'язатися з розробником бота безпосередньо через Telegram.

## Автор:
- TodoListBot розроблений та підтримується lilfinniiii.

## Відмова від відповідальності:
- TodoListBot надається "як є" без будь-яких гарантій. Користувачі несуть відповідальність за свої взаємодії та управління даними з ботом.

# TodoListBot Documentation ENG ver.

## Overview:
TodoListBot is a Telegram bot designed to help users manage their to-do lists effectively. It provides functionalities such as adding, deleting, and moving tasks across different statuses in the to-do list. This bot simplifies task management by providing a user-friendly interface within the Telegram app.

## Getting Started:
1. **Start the Bot**: Begin by searching for `@liltodolistbot` on Telegram and initiating a conversation by sending the `/start` command.
2. **Commands**:
    - `/add [task] [status]`: Add a new task to the to-do list with the specified status.
    - `/delete [task] [status]`: Delete a task from the to-do list based on its description and status.
    - `/move [task] [new_status]`: Move a task to a new status in the to-do list.
    - `/help` or `/commands`: Display available commands and usage instructions.

## Command Details:
1. **/add [task] [status]**:
    - Example: `/add  Review-user-feedback doing`
    - Description: Adds a new task with the provided description and assigns it to the specified status.

2. **/delete [task] [status]**:
    - Example: `/delete  Review-user-feedback doing`
    - Description: Deletes the task matching the provided description and status from the to-do list.

3. **/move [task] [new_status]**:
    - Example: `/move  Review-user-feedback done`
    - Description: Moves the task matching the provided description to the new status in the to-do list.

4. **/help** or **/commands**:
    - Description: Displays a list of available commands along with their usage instructions.

## Example Usage:
- **Adding a Task**: `/add Review-user-feedback doing`
- **Deleting a Task**: `/delete Review-user-feedback doing`
- **Moving a Task**: `/move Review-user-feedback done`

## Note:
- Ensure that tasks are described accurately to avoid confusion during task management operations.
- Use appropriate status keywords (e.g., Pending, In Progress, Done) to categorize tasks effectively.

## Feedback and Support:
- For any inquiries, feedback, or assistance, please feel free to contact the bot developer directly via Telegram.

## Credits:
- TodoListBot is developed and maintained by lilfinniiii.

## Disclaimer:
- TodoListBot is provided as-is without any warranties. Users are responsible for their interactions and data management with the bot.
