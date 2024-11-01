import os
import logging
from telegram import Update, Document
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram Bot Token
TOKEN = "7817448023:AAEnKpTuxfu8uz9hV-mJVjmqBvtBeDiauGQ"
WEBHOOK_URL = "https://c-edit.onrender.com"

# Initialize the bot application
bot_app = Application.builder().token(TOKEN).build()

# Command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("<b>𝗪𝗘𝗟𝗖𝗢𝗠𝗘! 𝗧𝗢 𝗕𝗛𝗔𝗜𝗡𝗞𝗔𝗥 𝗖𝗢𝗠𝗕𝗢-𝗘𝗗𝗜𝗧𝗢𝗥</b>\n\n"
                                    "Sᴇɴᴅ ʏᴏᴜʀ ᴄᴏᴍʙᴏ ғɪʟᴇ ɪɴ <code>.txt</code> ғᴏʀᴍᴀᴛ.\n\n"
                                    "<b>𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦:</b>\n"
                                    "/r_dupe - Rᴇᴍᴏᴠᴇ Dᴜᴘʟɪᴄᴀᴛᴇs\n"
                                    "/r_cap - Rᴇᴍᴏᴠᴇ Cᴀᴘᴛᴜʀᴇ",
                                    parse_mode='HTML'
    )

# Function to remove duplicates
def remove_duplicates(file_path: str) -> str:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    unique_lines = list(dict.fromkeys(lines))
    processed_file_path = "combo.txt"
    with open(processed_file_path, 'w') as file:
        file.writelines(unique_lines)
    return processed_file_path

# Function to remove capture after the first space
def remove_capture(file_path: str) -> str:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    processed_lines = [line.split(" ")[0] + '\n' for line in lines]
    processed_file_path = "combo.txt"
    with open(processed_file_path, 'w') as file:
        file.writelines(processed_lines)
    return processed_file_path

# Handler for the /r_dupe command to remove duplicates
async def r_dupe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'document_path' not in context.user_data:
        await update.message.reply_text("Pʟᴇᴀsᴇ sᴇɴᴅ ᴄᴏᴍʙᴏ ғɪʟᴇ ғɪʀsᴛ.")
        return
    file_path = context.user_data['document_path']
    processed_file_path = remove_duplicates(file_path)
    await update.message.reply_text("Rᴇᴍᴏᴠɪɴɢ Dᴜᴘʟɪᴄᴀᴛᴇs...")
    with open(processed_file_path, 'rb') as processed_file:
        await update.message.reply_document(processed_file, filename="combo.txt")
    os.remove(file_path)
    os.remove(processed_file_path)
    context.user_data.pop('document_path', None)

# Handler for the /r_cap command to remove capture
async def r_cap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'document_path' not in context.user_data:
        await update.message.reply_text("Pʟᴇᴀsᴇ sᴇɴᴅ ᴄᴏᴍʙᴏ ғɪʟᴇ ғɪʀsᴛ.")
        return
    file_path = context.user_data['document_path']
    processed_file_path = remove_capture(file_path)
    await update.message.reply_text("Rᴇᴍᴏᴠɪɴɢ Cᴀᴘᴛᴜʀᴇ...")
    with open(processed_file_path, 'rb') as processed_file:
        await update.message.reply_document(processed_file, filename="combo.txt")
    os.remove(file_path)
    os.remove(processed_file_path)
    context.user_data.pop('document_path', None)

# Handler for receiving documents
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    document: Document = update.message.document
    if document.mime_type != 'text/plain':
        await update.message.reply_text("Pʟᴇᴀsᴇ sᴇɴᴅ ᴛᴇxᴛ (.txt) Fɪʟᴇ.")
        return
    file = await document.get_file()
    file_path = os.path.join("downloads", document.file_name)
    os.makedirs("downloads", exist_ok=True)
    await file.download_to_drive(file_path)
    context.user_data['document_path'] = file_path
    await update.message.reply_text("Fɪʟᴇ ʀᴇᴄᴇɪᴠᴇᴅ. Usᴇ /r_dupe ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴅᴜᴘʟɪᴄᴀᴛᴇs Oʀ /r_cap ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴄᴀᴘᴛᴜʀᴇ.")

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Set up handlers for commands and document
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("r_dupe", r_dupe))
bot_app.add_handler(CommandHandler("r_cap", r_cap))
bot_app.add_handler(MessageHandler(filters.Document.TEXT & filters.Document.MimeType("text/plain"), handle_document))
bot_app.add_error_handler(error)

# Flask route for webhook
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook() -> str:
    """Process incoming updates from Telegram."""
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.process_update(update)
    return "ok"

# Main function
async def set_webhook():
    """Set the webhook URL for the bot."""
    await bot_app.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

if __name__ == '__main__':
    bot_app.loop.run_until_complete(set_webhook())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
