import os
import telebot
from telebot import types
from telebot import types
from telebot.apihelper import ApiTelegramException
from flask import Flask, request

# Your Telegram Bot Token
TOKEN = "7817448023:AAEnKpTuxfu8uz9hV-mJVjmqBvtBeDiauGQ"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/' + bot.token, methods=['POST'])
def get_message():
    json_str = request.stream.read().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route("/", methods=['GET'])
def index():
    return "Bot is running!"
    
    
gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjR3Y3JldDhodHBhdXg4bTZyd2k4Nmt6MnQxOWhrdDR2cnJtajN1YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/B1Lopnwqs9WIr3GtnQ/giphy.gif"

# A dictionary to store user-specific data
user_data = {}


# Replace these with actual usernames of your channels
CHANNEL_ID_1 = '@bhainkargiveaway'
CHANNEL_ID_2 = '@crunchyrollacc'

@bot.message_handler(commands=['start'])
def start(message):
    first_name = message.from_user.first_name or "User"
    username = message.from_user.username
    user_id = message.from_user.id

    # Create a clickable link to the user's profile
    if username:
        profile_link = f'<a href="https://t.me/{username}">{first_name}</a>'
    else:
        profile_link = f'<a href="tg://user?id={user_id}">{first_name}</a>'
    
    # Inline keyboard with join buttons and a "Check" button
    markup = types.InlineKeyboardMarkup()
    join_btn1 = types.InlineKeyboardButton("Join ", url=f"https://t.me/{CHANNEL_ID_1[1:]}")
    join_btn2 = types.InlineKeyboardButton("Join ", url=f"https://t.me/{CHANNEL_ID_2[1:]}")
    check_btn = types.InlineKeyboardButton("Verify ✅", callback_data="check_joined")

    markup.add(join_btn1, join_btn2)
    markup.add(check_btn)

    # Send join instructions to the user
    bot.send_animation(user_id, gif_url, caption= f"👮‍♂️Hey {profile_link}\n\n"
    "Wᴇʟᴄᴏᴍᴇ Tᴏ 𝗕𝗛𝗔𝗜𝗡𝗞𝗔𝗥 𝗖𝗢𝗠𝗕𝗢-𝗘𝗗𝗜𝗧𝗢𝗥\n"
    "Fʀᴇᴇ ᴄᴏᴍʙᴏ ᴇᴅɪᴛᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ ᴡʜɪᴄʜ ɪs ғᴀsᴛ ᴀɴᴅ ᴇᴀsʏ ᴛᴏ ᴜsᴇ\n\n"
    
    "🚫 Jᴏɪɴ ᴀʟʟ ᴄʜᴀɴɴᴇʟs ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴠᴇʀɪғʏ✅", reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == "check_joined")
def check_joined_channels(call):
    user_id = call.from_user.id

    try:
        # Check if the user is a member of both channels
        is_member_channel1 = bot.get_chat_member(CHANNEL_ID_1, user_id).status in ['member', 'administrator', 'creator']
        is_member_channel2 = bot.get_chat_member(CHANNEL_ID_2, user_id).status in ['member', 'administrator', 'creator']

        if is_member_channel1 and is_member_channel2:
            bot.send_message(user_id, "✅ Thank you for joining both channels!")
            # Send welcome message
            bot.send_animation(user_id, gif_url, caption=( "<b>𝗪𝗘𝗟𝗖𝗢𝗠𝗘! 𝗧𝗢 𝗕𝗛𝗔𝗜𝗡𝗞𝗔𝗥 𝗖𝗢𝗠𝗕𝗢-𝗘𝗗𝗜𝗧𝗢𝗥</b>\n\n"
        "Sᴇɴᴅ ʏᴏᴜʀ ᴄᴏᴍʙᴏ ғɪʟᴇ ɪɴ <code>.txt</code> ғᴏʀᴍᴀᴛ.\n\n"
        "<b>𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦:</b>\n"
        "/r_dupe - Rᴇᴍᴏᴠᴇ Dᴜᴘʟɪᴄᴀᴛᴇs\n"
        "/r_cap - Rᴇᴍᴏᴠᴇ Cᴀᴘᴛᴜʀᴇ"
        "\n\n"
        "Bᴏᴛ Bʏ @bhainkar"), parse_mode='HTML')
        else:
            bot.send_message(user_id, "🚫 Please make sure to join both channels to proceed.")
    
    except ApiTelegramException as e:
        # Handle errors related to invalid chat IDs or bot permissions
        bot.answer_callback_query(call.id, "An error occurred. Please ensure the bot is an admin in the required channels.")
        print(f"Error: {e}")



# Function to remove duplicates
def remove_duplicates(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    unique_lines = list(dict.fromkeys(lines))
    processed_file_path = "combo.txt"
    with open(processed_file_path, 'w') as file:
        file.writelines(unique_lines)
    return processed_file_path

# Function to remove capture after the first space
def remove_capture(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    processed_lines = [line.split(" ")[0] + '\n' for line in lines]
    processed_file_path = "combo.txt"
    with open(processed_file_path, 'w') as file:
        file.writelines(processed_lines)
    return processed_file_path

# Handler for the /r_dupe command to remove duplicates
@bot.message_handler(commands=['r_dupe'])
def r_dupe(message):
    user_id = message.from_user.id
    if user_id not in user_data or 'document_path' not in user_data[user_id]:
        bot.reply_to(message, "Pʟᴇᴀsᴇ sᴇɴᴅ ᴄᴏᴍʙᴏ ғɪʟᴇ ғɪʀsᴛ.")
        return
    
    file_path = user_data[user_id]['document_path']
    processed_file_path = remove_duplicates(file_path)

    bot.reply_to(message, "Rᴇᴍᴏᴠɪɴɢ Dᴜᴘʟɪᴄᴀᴛᴇs...")
    with open(processed_file_path, 'rb') as processed_file:
        bot.send_document(message.chat.id, processed_file, visible_file_name="combo.txt")
    
    # Clean up files
    os.remove(file_path)
    os.remove(processed_file_path)
    del user_data[user_id]['document_path']

# Handler for the /r_cap command to remove capture
@bot.message_handler(commands=['r_cap'])
def r_cap(message):
    user_id = message.from_user.id
    if user_id not in user_data or 'document_path' not in user_data[user_id]:
        bot.reply_to(message, "Pʟᴇᴀsᴇ sᴇɴᴅ ᴄᴏᴍʙᴏ ғɪʟᴇ ғɪʀsᴛ.")
        return
    
    file_path = user_data[user_id]['document_path']
    processed_file_path = remove_capture(file_path)

    bot.reply_to(message, "Rᴇᴍᴏᴠɪɴɢ Cᴀᴘᴛᴜʀᴇ...")
    with open(processed_file_path, 'rb') as processed_file:
        bot.send_document(message.chat.id, processed_file, visible_file_name="combo.txt")
    
    # Clean up files
    os.remove(file_path)
    os.remove(processed_file_path)
    del user_data[user_id]['document_path']

@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Attempt to retrieve the document file from different sources
    document = message.document
    if document is None:
        # Check if the message is a reply and contains a document
        if message.reply_to_message and message.reply_to_message.document:
            document = message.reply_to_message.document
        # Check if the message is a forward from another user or from the bot itself
        elif message.forward_from or message.forward_from_chat:
            forwarded_message = message.forward_from_chat or message.forward_from
            if forwarded_message and message.forward_from_message_id:
                document = message.document or (message.reply_to_message and message.reply_to_message.document)

    # If we still don’t have a document, inform the user
    if document is None:
        bot.reply_to(message, "Cᴏᴜʟᴅɴ'ᴛ ᴅᴇᴛᴇᴄᴛ ᴛʜᴇ ғɪʟᴇ. Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴛᴇᴛx (.txt) Fɪʟᴇ.")
        return

    # Check if it’s a .txt file
    if document.mime_type != 'text/plain':
        bot.reply_to(message, "Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴛᴇxᴛ (.txt) Fɪʟᴇ.")
        return

    user_id = message.from_user.id

    try:
        # Retrieve the file and save it locally
        file_info = bot.get_file(document.file_id)
        file_path = os.path.join("downloads", document.file_name)
        os.makedirs("downloads", exist_ok=True)

        # Download and save the file
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Store file path in user data
        user_data[user_id] = {'document_path': file_path}
        bot.reply_to(message, "Fɪʟᴇ ʀᴇᴄᴇɪᴠᴇᴅ. Usᴇ /r_dupe ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴅᴜᴘʟɪᴄᴀᴛᴇs Oʀ /r_cap ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴄᴀᴘᴛɪᴏɴs.")
    
    except telebot.apihelper.ApiHTTPException as e:
        bot.reply_to(message, "Fᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ғɪʟᴇ. Pʟᴇᴀsᴇ ᴛʀʏ sᴇɴᴅɪɴɢ ɪᴛ ᴀɢᴀɪɴ.")
        print("Download failed:", e)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://c-edit.onrender.com/" + bot.token)  # Replace with your server URL
    app.run(host="0.0.0.0", port=5000)  # You can change the port number if needed
      
