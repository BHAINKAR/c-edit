import os
import logging
from telegram import Update, Document
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram Bot Token
TOKEN = "7817448023:AAEnKpTuxfu8uz9hV-mJVjmqBvtBeDiauGQ"

# Command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("<b>𝗪𝗘𝗟𝗖𝗢𝗠𝗘! 𝗧𝗢 𝗕𝗛𝗔𝗜𝗡𝗞𝗔𝗥 𝗖𝗢𝗠𝗕𝗢-𝗘𝗗𝗜𝗧𝗢𝗥</b>\n\n"
        "Sᴇɴᴅ ʏᴏᴜʀ ᴄᴏᴍʙᴏ ғɪʟᴇ ɪɴ <code>.txt</code> ғᴏʀᴍᴀᴛ.\n\n"
        "<b>𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦:</b>\n"
        "/r_dupe - Rᴇᴍᴏᴠᴇ Dᴜᴘʟɪᴄᴀᴛᴇs\n"
        "/r_cap - Rᴇᴍᴏᴠᴇ Cᴀᴘᴛᴜʀᴇ\n\n"
        "Bᴏᴛ Bʏ @bhainkar",
        parse_mode='HTML'
        )

# Function to remove duplicates
def remove_duplicates(file_path: str) -> str:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Remove duplicate lines while preserving order
    unique_lines = list(dict.fromkeys(lines))
    
    # Save the processed content to a new file
    processed_file_path = "combo.txt"
    with open(processed_file_path, 'w') as file:
        file.writelines(unique_lines)

    return processed_file_path

# Function to remove capture after the first space
def remove_capture(file_path: str) -> str:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Remove anything after the first space in each line
    processed_lines = [line.split(" ")[0] + '\n' for line in lines]

    # Save the processed content to a new file
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

    # Send the processed file
    with open(processed_file_path, 'rb') as processed_file:
        await update.message.reply_document(processed_file, filename="combo.txt")

    # Clean up files
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

    # Send the processed file
    with open(processed_file_path, 'rb') as processed_file:
        await update.message.reply_document(processed_file, filename="combo.txt")

    # Clean up files
    os.remove(file_path)
    os.remove(processed_file_path)
    context.user_data.pop('document_path', None)

# Handler for receiving documents
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    document: Document = update.message.document

    # Ensure the file is a .txt file
    if document.mime_type != 'text/plain':
        await update.message.reply_text("Pʟᴇᴀsᴇ sᴇɴᴅ ᴛᴇxᴛ (.txt) Fɪʟᴇ.")
        return

    # Download the file
    file = await document.get_file()
    file_path = os.path.join("downloads", document.file_name)
    os.makedirs("downloads", exist_ok=True)
    await file.download_to_drive(file_path)
    
    # Save file path in user data
    context.user_data['document_path'] = file_path
    await update.message.reply_text("Fɪʟᴇ ʀᴇᴄᴇɪᴠᴇᴅ. Usᴇ /r_dupe ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴅᴜᴘʟɪᴄᴀᴛᴇs Oʀ /r_cap ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴄᴀᴘᴛᴜʀᴇ.")

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    # Initialize the bot with the given token
    application = Application.builder().token(TOKEN).build()
    
    # Handlers for commands and document
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("r_dupe", r_dupe))
    application.add_handler(CommandHandler("r_cap", r_cap))
    application.add_handler(MessageHandler(filters.Document.TEXT & filters.Document.MimeType("text/plain"), handle_document))

    # Log all errors
    application.add_error_handler(error)
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
