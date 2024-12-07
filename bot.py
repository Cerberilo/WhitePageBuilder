import os
import shutil
from zipfile import ZipFile
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random
import logging
from api_key import API_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

blocks = {
    "header": "Шапка сайта",
    "banner": "Баннер с кнопкой",
    "info_text": "Информационный текст",
    "advantages": "Преимущества",
    "gallery": "Галерея",
    "two_columns": "Текст в две колонки",
    "text_banner": "Текст + Баннер",
    "desc_img_1": "Описание и фото 1",
    "desc_img_2": "Описание и фото 2",
    "article": "Текст с заголовком",
    "knowledge": "Колонка автора",
    "form": "Форма заявки",
    "footer": "Футер",
}

selected_blocks = []

def generate_random_pastel_colors():
    """Генерирует случайные пастельные цвета."""
    def random_pastel_color():
        base = random.randint(200, 255)
        return f"#{base:02x}{random.randint(180, base):02x}{random.randint(180, base):02x}"
    
    return {
        "background-header": random_pastel_color(),
        "background-intro": random_pastel_color(),
        "background-center-info": random_pastel_color(),
        "background-features": random_pastel_color(),
        "background-gallery": random_pastel_color(),
        "background-knowledge": random_pastel_color(),
        "background-subscribe": random_pastel_color(),
        "background-footer": random_pastel_color(),
    }

# Клавиатура с кнопками для управления ботом
def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [["/start Запустить бота 🚀", "/restart Перезапустить бота 🔄"]],
        resize_keyboard=True
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Отправка изображения с описанием блоков
    try:
        with open("sitemap.png", "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption="Вот схема блоков, доступных для создания сайта. Выберите нужные блоки и настройте сайт по своему усмотрению."
            )
    except FileNotFoundError:
        logging.error("Файл sitemap.png не найден в корне проекта")
        await update.message.reply_text("Ошибка: файл sitemap.png не найден.")
    
    # Отправка приветственного сообщения и меню
    await update.message.reply_text(
        "Добро пожаловать! Управляйте блоками для создания сайта.",
        reply_markup=main_menu_keyboard()
    )
    await show_block_options(update, context, new_message=True)

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Бот успешно перезапущен! Вы можете продолжить работу с ботом.",
        reply_markup=main_menu_keyboard()
    )
    selected_blocks.clear()
    # Автоматический запуск команды start
    await start(update, context)

async def show_block_options(update: Update, context: ContextTypes.DEFAULT_TYPE, new_message=False) -> None:
    add_buttons = [
        [InlineKeyboardButton(f"Добавить: {name}", callback_data=f"add_{key}")] for key, name in blocks.items()
    ]

    remove_buttons = [
        [InlineKeyboardButton(f"❌ Удалить: {blocks[block]}", callback_data=f"remove_{i}")] for i, block in enumerate(selected_blocks)
    ]

    keyboard = add_buttons + [[InlineKeyboardButton("⬇ Удаление блоков ⬇", callback_data="separator")]] + remove_buttons
    keyboard.append([InlineKeyboardButton("Готово", callback_data="done")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        f"Выбранные блоки:\n{format_selected_blocks()}\n\n"
        f"Добавьте или удалите блоки. Нажмите 'Готово', когда закончите."
        if selected_blocks
        else "Выберите блоки для вашего сайта:"
    )

    if new_message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)

def format_selected_blocks():
    return "\n".join([f"{i + 1}. {blocks[block]}" for i, block in enumerate(selected_blocks)])

async def handle_block_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("add_"):
        block = data.split("_", 1)[1]
        if block not in blocks:
            logging.warning(f"Invalid block key: {block}")
            await query.message.reply_text(f"Ошибка: блок '{block}' недействителен.")
            return

        selected_blocks.append(block)
        logging.info(f"Block '{blocks[block]}' added by user")

        # Отправка изображения выбранного блока
        block_image_path = f"img_blocks/{block}.png"
        if os.path.exists(block_image_path):
            try:
                with open(block_image_path, "rb") as photo:
                    await query.message.reply_photo(
                        photo=photo,
                        caption=f"Вы добавили блок: {blocks[block]}"
                    )
            except Exception as e:
                logging.error(f"Ошибка при отправке изображения для блока '{block}': {e}")
        else:
            logging.warning(f"Изображение для блока '{block}' не найдено: {block_image_path}")
            await query.message.reply_text(f"Изображение для блока '{blocks[block]}' отсутствует.")

        await show_block_options(update, context)

    elif data.startswith("remove_"):
        index = int(data.split("_", 1)[1])
        if 0 <= index < len(selected_blocks):
            removed_block = selected_blocks.pop(index)
            logging.info(f"Block '{blocks[removed_block]}' removed by user")
        else:
            logging.warning(f"Invalid index for removal: {index}")
        await show_block_options(update, context)

    elif data == "done":
        await generate_site(update, context)

async def generate_site(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    colors = generate_random_pastel_colors()

    css_content = f"""
:root {{
    --background-header: {colors['background-header']};
    --background-intro: {colors['background-intro']};
    --background-center-info: {colors['background-center-info']};
    --background-features: {colors['background-features']};
    --background-gallery: {colors['background-gallery']};
    --background-knowledge: {colors['background-knowledge']};
    --background-subscribe: {colors['background-subscribe']};
    --background-footer: {colors['background-footer']};
}}
"""

    html_content = "<!DOCTYPE html>\n<html>\n<head>\n<style>\n" + css_content + "\n</style>\n"
    html_content += '<link rel="stylesheet" href="styles.css">\n'
    html_content += '<script src="cookies.js" defer></script>\n'
    html_content += '<script src="menu.js" defer></script>\n</head>\n<body>\n'

    # Добавление баннера для кук
    html_content += """
    <div id="cookie-banner" style="display: none; position: fixed; bottom: 0; width: 100%; background: #333; color: #fff; text-align: center; padding: 10px;">
        <p> We use cookies to improve your experience on the website. <a href="privacy_policy.html" style="color: #4CAF50;">Learn more</a></p>
        <button id="accept-cookies" style="background: #4CAF50; color: #fff; border: none; padding: 10px; cursor: pointer;">Accept</button>
    </div>
    """

    for block in selected_blocks:
        if block not in blocks:
            continue
        try:
            with open(f"blocks/{block}.html", "r", encoding="utf-8") as file:
                html_content += file.read() + "\n"
        except FileNotFoundError:
            logging.error(f"File for block '{block}' not found")
            await update.callback_query.message.reply_text(f"Файл блока '{blocks[block]}' не найден.")
            return
        except Exception as e:
            logging.error(f"Ошибка обработки блока '{block}': {e}")
            await update.callback_query.message.reply_text(f"Ошибка при обработке блока '{blocks[block]}': {e}")
            return

    html_content += "</body>\n</html>"

    project_dir = "site_project"
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    os.makedirs(project_dir)

    with open(os.path.join(project_dir, "index.html"), "w", encoding="utf-8") as file:
        file.write(html_content)

    # Копирование стилей и скриптов
    for static_file in ["styles.css", "cookies.js", "menu.js"]:
        if os.path.exists(static_file):
            shutil.copy(static_file, os.path.join(project_dir, static_file))

    if os.path.exists("img"):
        shutil.copytree("img", os.path.join(project_dir, "img"))

    # Копирование дополнительных файлов из корня проекта
    additional_files = ["contact.html", "privacy_policy.html", "terms_of_service.html"]
    for file_name in additional_files:
        if os.path.exists(file_name):
            shutil.copy(file_name, os.path.join(project_dir, file_name))
        else:
            logging.warning(f"Файл {file_name} не найден в корне проекта.")

    # Создание ZIP-архива
    zip_filename = "site_project.zip"
    with ZipFile(zip_filename, "w") as zipf:
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, project_dir)
                zipf.write(filepath, arcname)

    # Отправка ZIP-архива
    try:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(zip_filename, "rb"))
        logging.info("ZIP-архив отправлен пользователю")

        # Отправка дополнительного сообщения
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "😎 Теперь осталось заменить стоковые фото на те, которые вы хотите видеть на своем сайте, "
                "а стоковый текст — на тот, который соответствует вашей тематике.\n\n"
                "Спасибо, что воспользовались ботом! Если хотите создать еще один сайт, нажмите /restart"
            )
        )
    except Exception as e:
        logging.error(f"Ошибка при отправке файла: {e}")
        await update.callback_query.message.reply_text("Произошла ошибка при отправке ZIP-архива.")
    finally:
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        if os.path.exists(zip_filename):
            os.remove(zip_filename)

    reset_selections()

def reset_selections():
    global selected_blocks
    selected_blocks = []

def main() -> None:
    application = Application.builder().token(API_KEY).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("restart", restart))
    application.add_handler(CallbackQueryHandler(handle_block_selection))
    application.run_polling()

if __name__ == "__main__":
    main()
























