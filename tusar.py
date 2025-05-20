import os
import re
import sys
import json
import time
import aiohttp
import asyncio
import requests
import subprocess
import urllib.parse
import cloudscraper
import datetime
import random
import ffmpeg
import logging 
import yt_dlp
from aiohttp import web
from core import *
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
import yt_dlp as youtube_dl
import cloudscraper
import m3u8
import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
cookies_file_path = os.getenv("COOKIES_FILE_PATH", "youtube_cookies.txt")

pwimg = "https://graph.org/file/8add8d382169e326f67e0-3bf38f92e52955e977.jpg"
#ytimg = "https://graph.org/file/3aa806c302ceec62e6264-60ced740281395f68f.jpg"
cpimg = "https://graph.org/file/5ed50675df0faf833efef-e102210eb72c1d5a17.jpg"  


async def show_random_emojis(message):
    emojis = ['🪄', '⏳', '😎', '⚡️', '🚀', '✨', '💥', '🎉', '🥂', '🍾', '🦠', '🪄', '☄️', '🕊️', '🪩', '🦚','🐅','🦁']
    emoji_message = await message.reply_text(' '.join(random.choices(emojis, k=1)))
    return emoji_message
    
# Define the owner's user ID
OWNER_ID = 6764661699 # Replace with the actual owner's user ID

# List of sudo users (initially empty or pre-populated)
SUDO_USERS = [6764661699]

AUTH_CHANNEL = -1002309542762

# Function to check if a user is authorized
def is_authorized(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in SUDO_USERS or user_id == AUTH_CHANNEL

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)

# Sudo command to add/remove sudo users
@bot.on_message(filters.command("sudo"))
async def sudo_command(bot: Client, message: Message):
    user_id = message.chat.id
    if user_id != OWNER_ID:
        await message.reply_text("**🚫 You are not authorized to use this command.**")
        return

    try:
        args = message.text.split(" ", 2)
        if len(args) < 2:
            await message.reply_text("**Usage:** `/sudo add <user_id>` or `/sudo remove <user_id>`")
            return

        action = args[1].lower()
        target_user_id = int(args[2])

        if action == "add":
            if target_user_id not in SUDO_USERS:
                SUDO_USERS.append(target_user_id)
                await message.reply_text(f"**✅ User {target_user_id} added to sudo list.**")
            else:
                await message.reply_text(f"**⚠️ User {target_user_id} is already in the sudo list.**")
        elif action == "remove":
            if target_user_id == OWNER_ID:
                await message.reply_text("**🚫 The owner cannot be removed from the sudo list.**")
            elif target_user_id in SUDO_USERS:
                SUDO_USERS.remove(target_user_id)
                await message.reply_text(f"**✅ User {target_user_id} removed from sudo list.**")
            else:
                await message.reply_text(f"**⚠️ User {target_user_id} is not in the sudo list.**")
        else:
            await message.reply_text("**Usage:** `/sudo add <user_id>` or `/sudo remove <user_id>`")
    except Exception as e:
        await message.reply_text(f"**Error:** {str(e)}")

import random

# Inline keyboard for start command
keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🧑‍💻 𝗗ᴇᴠᴇʟᴏᴘᴇʀ 🧑‍💻", url="https://t.me/hariom_singh_001") ],
                    [
                    InlineKeyboardButton("🪄 𝗨ᴘᴅᴀᴛᴇ 𝗖ʜᴀɴɴᴇʟ 🪄", url="https://t.me/HariOM5328_bot") ],
                    [
                    InlineKeyboardButton("🛠️ 𝗛ᴇʟᴘ 🛠️", url="https://t.me/hariom_singh_001")                              
                ],           
            ]
      )
    
# Image URLs for the random image feature
image_urls = [
    "https://graph.org/file/48166c70111547ffc35d5-643697eeb732a6557f.jpg",
    "https://graph.org/file/3fd6ead450f7c4b6f702d-cc93105da76125d9a8.jpg",
    "https://graph.org/file/9af9551adb6bab74ee658-71c2df47e429fec9a0.jpg",
    "https://graph.org/file/40dabc065bc6038fa08c9-e98660f27581af62c7.jpg",
    "https://graph.org/file/45bc0011c397739ae8320-b23d54d24acb53baf6.jpg",
    "https://graph.org/file/59ebdaf518e58ca55de4a-68d747aec42bef44e8.jpg",
    "https://graph.org/file/670366b7aa9cb732115b0-21dced7fac7b29156b.jpg",
    # Add more image URLs as needed
]
    
# Start command handler
@bot.on_message(filters.command(["Hariom1"]))
async def start_command(bot: Client, message: Message):
    # Send a loading message
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Loading... ⏳🔄"
    )
  
    # Choose a random image URL
    random_image_url = random.choice(image_urls)
    
    # Caption for the image
    caption = (
        
        "🌟 Hello Boss 😎 {0} 🌟\n\n"
        "➽ **I am nom drm uploader bot 📥**\n\n"
        "➽ **/Help ⚔️For Help Use Command**\n\n"
        "➽ **/e2t - Edit txt file📝**\n\n"
        "➽ **/t2t - Txt to Txt file📝**\n\n"
        "➽ **/cookies - Upload cookies file🍪**\n\n"
        "➽ **/y2t - Create txt of yt playlist**\n\n"
        "➽ **/stop working process Command**\n\n"
        "➽ **Use /hariom Command To Download  Data From TXT File 🗃️ \n\n\n"
        "**🤖 𝐌𝐚𝐝𝐞 𝐁𝐲 ➤<pre><code>╭━━━━━━━━━━━━━╮\n👨🏻‍💻『𝙃𝘼𝙍𝙄𝙊𝙈 𝙎𝙄𝙉𝙂𝙃』\n╰━━━━━━━━━━━━━╯\n</code></pre>**"
    
      )

    await asyncio.sleep(1)
    await loading_message.edit_text(
        "Initializing Uploader bot... 🤖\n\n"
        "Progress: ⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%\n\n"
    )

    await asyncio.sleep(1)
    await loading_message.edit_text(
        "Loading features... ⏳\n\n"
        "Progress: 🟥🟥⬜⬜⬜⬜⬜⬜ 25%\n\n"
    )
    
    await asyncio.sleep(1)
    await loading_message.edit_text(
        "This may take a moment, sit back and relax! 😊\n\n"
        "Progress: 🟧🟧🟧🟧⬜⬜⬜⬜ 50%\n\n"
    )

    await asyncio.sleep(1)
    await loading_message.edit_text(
        "Checking Bot Status... 🔍\n\n"
        "Progress: 🟨🟨🟨🟨🟨🟨⬜⬜ 75%\n\n"
    )

    await asyncio.sleep(1)
    await loading_message.edit_text(
        "Checking Bot Status... 🔍\n\n"
        "Progress:🟩🟩🟩🟩🟩🟩🟩🟩🟩 100%\n\n"
    )
        
    # Send the image with caption and buttons
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption.format(message.from_user.mention),
        reply_markup=keyboard
    )

    # Delete the loading message
    await loading_message.delete()

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("Contact", url="https://t.me/hariom_singh_001")],
   
    [InlineKeyboardButton("Owner", url="https://t.me/hariom_singh_001")],
])

#=================== TELEGRAM ID INFORMATION =============
@bot.on_message(filters.private & filters.command(["info"]))
async def info(bot: Client, update: Message):    
    text = (
        f"╭────────────────╮\n"
        f"│✨ **__Your Telegram Info__**✨ \n"
        f"├────────────────\n"
        f"├🔹**Name :** `{update.from_user.first_name} {update.from_user.last_name if update.from_user.last_name else 'None'}`\n"
        f"├🔹**User ID :** @{update.from_user.username}\n"
        f"├🔹**TG ID :** `{update.from_user.id}`\n"
        f"├🔹**Profile :** {update.from_user.mention}\n"
        f"╰────────────────╯"
    )    
    await update.reply_text(        
        text=text,
        disable_web_page_preview=True,
        reply_markup=BUTTONS
    )
BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton(text="📞 Contact", url=f"https://t.me/+-UUAslfhnugyZjZl")]])
# /id Command - Show Group/Channel ID
@bot.on_message(filters.command(["id"]))
async def id_command(client, message: Message):
    chat_id = message.chat.id
    await message.reply_text(f"**ID : `{chat_id}`**\n\n")
@bot.on_message(filters.command('t2t'))
async def text_to_txt(client, message: Message):
    user_id = str(message.from_user.id)

    # Inform the user to send the text data and its desired file name
    await message.reply_text(
        "🎉 **Welcome to the Text to .txt Converter!**\n\n"
        "Please send the **text** you want to convert into a `.txt` file.\n\n"
        "Afterward, provide the **file name** you prefer for the .txt file (without extension)."
    )

    try:
        # Wait for the user to send the text data
        input_message: Message = await bot.listen(message.chat.id)

        # Ensure the message contains text
        if not input_message.text:
            await message.reply_text(
                "🚨 **Error**: Please send valid text data to convert into a `.txt` file."
            )
            return

        text_data = input_message.text.strip()

        # Ask the user for the custom file name
        await message.reply_text(
            "🔤 **Now, please provide the file name (without extension)**\n\n"
            "For example: **'output'** or **'document'**\n\n"
            "If you're unsure, we'll default to 'output'."
        )

        # Wait for the custom file name input
        file_name_input: Message = await bot.listen(message.chat.id)
        custom_file_name = file_name_input.text.strip()

        # If the user didn't provide a name, use the default one
        if not custom_file_name:
            custom_file_name = "output"

        await file_name_input.delete(True)

        # Create and save the .txt file with the custom name
        txt_file = os.path.join("downloads", f'{custom_file_name}.txt')
        os.makedirs(os.path.dirname(txt_file), exist_ok=True)  # Ensure the directory exists
        with open(txt_file, 'w') as f:
            f.write(text_data)

        # Send the generated text file to the user with a pretty caption
        await message.reply_document(
            document=txt_file,
            caption=f"🎉 **Here is your text file**: `{custom_file_name}.txt`\n\n"
                    "You can now download your content! 📥"
        )

        # Remove the temporary text file after sending
        os.remove(txt_file)

    except Exception as e:
        # In case of any error, send a generic error message
        await message.reply_text(
            f"🚨 **An unexpected error occurred**: {str(e)}.\nPlease try again or contact support if the issue persists."
        )

# Define paths for uploaded file and processed file
UPLOAD_FOLDER = '/path/to/upload/folder'
EDITED_FILE_PATH = '/path/to/save/edited_output.txt'

# Stop command handler
@bot.on_message(filters.command("stop"))
async def restart_handler(_, m: Message):
    await m.reply_text("**𝗦𝘁𝗼𝗽𝗽𝗲𝗱**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("restart"))
async def restart_handler(_, m):
    if not is_authorized(m.from_user.id):
        await m.reply_text("**🚫 You are not authorized to use this command.**")
        return
    await m.reply_text("🔮Restarted🔮", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


COOKIES_FILE_PATH = "youtube_cookies.txt"

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    if not is_authorized(m.from_user.id):
        await m.reply_text("🚫 You are not authorized to use this command.")
        return
    """
    Command: /cookies
    Allows any user to upload a cookies file dynamically.
    """
    await m.reply_text(
        "𝗣𝗹𝗲𝗮𝘀𝗲 𝗨𝗽𝗹𝗼𝗮𝗱 𝗧𝗵𝗲 𝗖𝗼𝗼𝗸𝗶𝗲𝘀 𝗙𝗶𝗹𝗲 (.𝘁𝘅𝘁 𝗳𝗼𝗿𝗺𝗮𝘁).",
        quote=True
    )

    try:
        # Wait for the user to send the cookies file
        input_message: Message = await client.listen(m.chat.id)

        # Validate the uploaded file
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return

        # Download the cookies file
        downloaded_path = await input_message.download()

        # Read the content of the uploaded file
        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()

        # Replace the content of the target cookies file
        with open(COOKIES_FILE_PATH, "w") as target_file:
            target_file.write(cookies_content)

        await input_message.reply_text(
            "✅ 𝗖𝗼𝗼𝗸𝗶𝗲𝘀 𝗨𝗽𝗱𝗮𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆.\n\𝗻📂 𝗦𝗮𝘃𝗲𝗱 𝗜𝗻 youtube_cookies.txt."
        )

    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

# Define paths for uploaded file and processed file
UPLOAD_FOLDER = '/path/to/upload/folder'
EDITED_FILE_PATH = '/path/to/save/edited_output.txt'

@bot.on_message(filters.command('e2t'))
async def edit_txt(client, message: Message):
    

    # Prompt the user to upload the .txt file
    await message.reply_text(
        "🎉 **Welcome to the .txt File Editor!**\n\n"
        "Please send your `.txt` file containing subjects, links, and topics."
    )

    # Wait for the user to upload the file
    input_message: Message = await bot.listen(message.chat.id)
    if not input_message.document:
        await message.reply_text("🚨 **Error**: Please upload a valid `.txt` file.")
        return

    # Get the file name
    file_name = input_message.document.file_name.lower()

    # Define the path where the file will be saved
    uploaded_file_path = os.path.join(UPLOAD_FOLDER, file_name)

    # Download the file
    uploaded_file = await input_message.download(uploaded_file_path)

    # After uploading the file, prompt the user for the file name or 'd' for default
    await message.reply_text(
        "🔄 **Send your .txt file name, or type 'd' for the default file name.**"
    )

    # Wait for the user's response
    user_response: Message = await bot.listen(message.chat.id)
    if user_response.text:
        user_response_text = user_response.text.strip().lower()
        if user_response_text == 'd':
            # Handle default file name logic (e.g., use the original file name)
            final_file_name = file_name
        else:
            final_file_name = user_response_text + '.txt'
    else:
        final_file_name = file_name  # Default to the uploaded file name

    # Read and process the uploaded file
    try:
        with open(uploaded_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to read the file.\n\nDetails: {e}")
        return

    # Parse the content into subjects with links and topics
    subjects = {}
    current_subject = None
    for line in content:
        line = line.strip()
        if line and ":" in line:
            # Split the line by the first ":" to separate title and URL
            title, url = line.split(":", 1)
            title, url = title.strip(), url.strip()

            # Add the title and URL to the dictionary
            if title in subjects:
                subjects[title]["links"].append(url)
            else:
                subjects[title] = {"links": [url], "topics": []}

            # Set the current subject
            current_subject = title
        elif line.startswith("-") and current_subject:
            # Add topics under the current subject
            subjects[current_subject]["topics"].append(line.strip("- ").strip())

    # Sort the subjects alphabetically and topics within each subject
    sorted_subjects = sorted(subjects.items())
    for title, data in sorted_subjects:
        data["topics"].sort()

    # Save the edited file to the defined path with the final file name
    try:
        final_file_path = os.path.join(UPLOAD_FOLDER, final_file_name)
        with open(final_file_path, 'w', encoding='utf-8') as f:
            for title, data in sorted_subjects:
                # Write title and its links
                for link in data["links"]:
                    f.write(f"{title}:{link}\n")
                # Write topics under the title
                for topic in data["topics"]:
                    f.write(f"- {topic}\n")
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to write the edited file.\n\nDetails: {e}")
        return

    # Send the sorted and edited file back to the user
    try:
        await message.reply_document(
            document=final_file_path,
            caption="📥**𝗘𝗱𝗶𝘁𝗲𝗱 𝗕𝘆 ➤╰────⌈🌟『𝙃𝘼𝙍𝙄𝙊𝙈 𝙎𝙄𝙉𝙂𝙃』🌟⌋────╯**"
        )
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to send the file.\n\nDetails: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)

from pytube import Playlist
import youtube_dl

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Utility Functions ---

def sanitize_filename(name):
    """
    Sanitizes a string to create a valid filename.
    """
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')

def get_videos_with_ytdlp(url):
    """
    Retrieves video titles and URLs using `yt-dlp`.
    If a title is not available, only the URL is saved.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            if 'entries' in result:
                title = result.get('title', 'Unknown Title')
                videos = {}
                for entry in result['entries']:
                    video_url = entry.get('url', None)
                    video_title = entry.get('title', None)
                    if video_url:
                        videos[video_title if video_title else "Unknown Title"] = video_url
                return title, videos
            return None, None
    except Exception as e:
        logging.error(f"Error retrieving videos: {e}")
        return None, None

def save_to_file(videos, name):
    """
    Saves video titles and URLs to a .txt file.
    If a title is unavailable, only the URL is saved.
    """
    filename = f"{sanitize_filename(name)}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        for title, url in videos.items():
            if title == "Unknown Title":
                file.write(f"{url}\n")
            else:
                file.write(f"{title}: {url}\n")
    return filename

# --- Bot Command ---

@bot.on_message(filters.command('y2t'))
async def ytplaylist_to_txt(client: Client, message: Message):
    """
    Handles the extraction of YouTube playlist/channel videos and sends a .txt file.
    """
    user_id = message.chat.id
    if user_id != OWNER_ID:
        await message.reply_text("**🚫 You are not authorized to use this command.\n\n🫠 This Command is only for owner.**")
        return

    # Request YouTube URL
    await message.delete()
    editable = await message.reply_text("📥 **Please enter the YouTube Playlist Url :**")
    input_msg = await client.listen(editable.chat.id)
    youtube_url = input_msg.text
    await input_msg.delete()
    await editable.delete()

    # Process the URL
    title, videos = get_videos_with_ytdlp(youtube_url)
    if videos:
        file_name = save_to_file(videos, title)
        await message.reply_document(
            document=file_name, 
            caption=f"`{title}`\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤ ╰─────⌈🌟『𝙃𝘼𝙍𝙄𝙊𝙈 𝙎𝙄𝙉𝙂𝙃』🌟⌋─────╯"
        )
        os.remove(file_name)
    else:
        await message.reply_text("⚠️ **Unable to retrieve videos. Please check the URL.**")

        
# List users command
@bot.on_message(filters.command("userlist") & filters.user(SUDO_USERS))
async def list_users(client: Client, msg: Message):
    if SUDO_USERS:
        users_list = "\n".join([f"User ID : `{user_id}`" for user_id in SUDO_USERS])
        await msg.reply_text(f"SUDO_USERS :\n{users_list}")
    else:
        await msg.reply_text("No sudo users.")


# Help command
@bot.on_message(filters.command("help"))
async def help_command(client: Client, msg: Message):
    help_text = (
        "`/start` - Start the bot⚡\n\n"
        "`/hariom` - Download and upload files (sudo)🎬\n\n"
        "`/restart` - Restart the bot🔮\n\n" 
        "`/stop` - Stop ongoing process🛑\n\n"
        "`/cookies` - Upload cookies file🍪\n\n"
        "`/e2t` - Edit txt file📝\n\n"
        "`/y2t` - Create txt of yt playlist (owner)🗃️\n\n"
        "`/sudoadd` - Add user or group or channel (owner)🎊\n\n"
        "`/sudoremove` - Remove user or group or channel (owner)❌\n\n"
        "`/userlist` - List of sudo user or group or channel📜\n\n"
       
    )
    await msg.reply_text(help_text)

# Upload command handler
@bot.on_message(filters.command(["godlike1"]))
async def upload(bot: Client, m: Message):
    if not is_authorized(m.chat.id):
        await m.reply_text("**🚫You are not authorized to use this bot.**")
        return

    editable = await m.reply_text(f"**<pre><code>📲𝐇𝐢 𝐈 𝐚𝐦 𝐏𝐨𝐰𝐞𝐟𝐮𝐥 𝐓𝐗𝐓 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫👨‍💻 𝐁𝐨𝐭.**\n\n👨‍💻**𝐒𝐞𝐧𝐝 𝐦𝐞 𝐭𝐡𝐞 𝐓𝐗𝐓 𝐟𝐢𝐥𝐞 𝐚𝐧𝐝 𝐰𝐚𝐢𝐭. 🗃️</code></pre>**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    pdf_count = 0
    img_count = 0
    zip_count = 0
    video_count = 0
    
    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        
        links = []
        for i in content:
            if "://" in i:
                url = i.split("://", 1)[1]
                links.append(i.split("://", 1))
                if ".pdf" in url:
                    pdf_count += 1
                elif url.endswith((".png", ".jpeg", ".jpg")):
                    img_count += 1
                elif ".zip" in url:
                    zip_count += 1
                else:
                    video_count += 1
        os.remove(x)
    except:
        await m.reply_text("😶𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗶𝗹𝗲 𝗜𝗻𝗽𝘂𝘁😶")
        os.remove(x)
        return
        
    await editable.edit(f"**<pre><code>∝ 𝐓𝐨𝐭𝐚𝐥 𝐋𝐢𝐧𝐤 𝐅𝐨𝐮𝐧𝐝 𝐀𝐫𝐞 🔗** **{len(links)}**\n\n𝐒𝐞𝐧𝐝 𝐅𝐫𝐨𝐦 𝐖𝐡𝐞𝐫𝐞 𝐘𝐨𝐮 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐒𝐭𝐚𝐫𝐭 🔢</code></pre>**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)
    try:
        arg = int(raw_text)
    except:
        arg = 1


    await editable.edit("**<pre><code>𝗘𝗻𝘁𝗲𝗿 𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 𝗼𝗿 𝘀𝗲𝗻𝗱 `𝗱` 𝗳𝗼𝗿 𝗴𝗿𝗮𝗯𝗶𝗻𝗴 𝗳𝗿𝗼𝗺 𝘁𝗲𝘅𝘁 𝗳𝗶𝗹𝗲𝗻𝗮𝗺𝗲.</code></pre>**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == 'd':
        b_name = file_name
    else:
        b_name = raw_text0

    await editable.edit("**<pre><code>╭━━━━❰  𝗘𝗡𝗧𝗘𝗥  𝗥𝗘𝗦𝗢𝗟𝗨𝗧𝗜𝗢𝗡 🎥  ❱━➣\n┣━━⪼𝟭𝟰𝟰\n┣━━⪼𝟮𝟰𝟬\n┣━━⪼𝟯𝟲𝟬\n┣━━⪼𝟰𝟴𝟬\n┣━━⪼𝟳𝟮𝟬\n┣━━⪼𝟭𝟬𝟴𝟬\n╰━━⌈⚡️[『 𝐇ᴀʀɪᴏᴍ 🧑‍💻 』]⚡️⌋━━➣</code></pre>**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    

    await editable.edit("**<pre><code>𝗘𝗻𝘁𝗲𝗿 𝗬𝗼𝘂𝗿 𝗡𝗮𝗺𝗲 𝗼𝗿 𝘀𝗲𝗻𝗱 `𝗱𝗲` 𝗳𝗼𝗿 𝘂𝘀𝗲 𝗱𝗲𝗳𝗮𝘂𝗹𝘁</code></pre>**")
    # Listen for the user's response
    input3: Message = await bot.listen(editable.chat.id)

    # Get the raw text from the user's message
    raw_text3 = input3.text

    # Delete the user's message after reading it
    await input3.delete(True)

    # Default credit message
    credit = "️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'de':
        CR = '🇭‌🇦‌🇷‌🇮‌🇴‌🇲‌'
    elif raw_text3:
        CR = raw_text3
    else:
        CR = credit
  
   
    #await editable.edit("**<pre><code>𝐄𝐧𝐭𝐞𝐫 𝐘𝐨𝐮𝐫 𝐏𝐖 𝐓𝐨𝐤𝐞𝐧 𝐅𝐨𝐫 𝐌𝐏𝐃 𝐔𝐑𝐋  𝐨𝐫 𝐬𝐞𝐧𝐝 noo 𝐟𝐨𝐫 𝐮𝐬𝐞 𝐝𝐞𝐟𝐚𝐮𝐥𝐭</code></pre>**")
    #input4: Message = await bot.listen(editable.chat.id)
    #raw_text4 = input4.text
    #await input4.delete(True)
    #if raw_text4 == 'noo':
        #MR = token
    #else:
        #MR = raw_text4
    
    await editable.edit("**<pre><code>🌄 𝗡𝗼𝘄 𝘀𝗲𝗻𝗱 𝘁𝗵𝗲 𝗧𝗵𝘂𝗺𝗯 𝘂𝗿𝗹 𝗶𝗳 𝗱𝗼𝗻'𝘁 𝘄𝗮𝗻𝘁 𝘁𝗵𝘂𝗺𝗯𝗻𝗮𝗶𝗹 𝘀𝗲𝗻𝗱 `𝗻𝗼`.</code></pre>**")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"
    failed_count =0
    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):
            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
                        
            elif 'media-cdn.classplusapp.com/drm/' in url:
                url = f"https://dragoapi.vercel.app/video/{url}"

            elif 'videos.classplusapp' in url:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9'}).json()['url']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
            elif "tencdn.classplusapp" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "media-cdn.classplusapp" in url:
             headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
             params = (('url', f'{url}'),)
             response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
             url = response.json()['url']

            elif "https://appx-transcoded-videos.livelearn.in/videos/rozgar-data/" in url:
                url = url.replace("https://appx-transcoded-videos.livelearn.in/videos/rozgar-data/", "")
                name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "@").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                name = f'{str(count).zfill(3)}) {name1[:60]}'
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
                
            elif "https://appx-transcoded-videos-mcdn.akamai.net.in/videos/bhainskipathshala-data/" in url:
                url = url.replace("https://appx-transcoded-videos-mcdn.akamai.net.in/videos/bhainskipathshala-data/", "")
                name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "@").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                name = f'{str(count).zfill(3)}) {name1[:60]}'
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

            
            #elif '/master.mpd' in url:
             #id =  url.split("/")[-2]
             #url = f"https://player.muftukmall.site/?id={id}"
            #elif '/master.mpd' in url:
             #id =  url.split("/")[-2]
             #url = f"https://anonymouspwplayer-b99f57957198.herokuapp.com/pw?url={url}?token={raw_text4}"
            #url = f"https://madxapi-d0cbf6ac738c.herokuapp.com/{id}/master.m3u8?token={raw_text4}"
            elif '/master.mpd' in url:
             id =  url.split("/")[-2]
             url = f"https://dl.alphacbse.site/download/{id}/master.m3u8"
            
        
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            #if 'cpvod.testbook' in url:
                #CPVOD = url.split("/")[-2]
                #url = requests.get(f'https://extractbot.onrender.com/classplus?link=https://cpvod.testbook.com/{CPVOD}/playlist.m3u8', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'}).json()['url']
            
            #if 'cpvod.testbook' in url:
               #url = requests.get(f'https://mon-key-3612a8154345.herokuapp.com/get_keys?url=https://cpvod.testbook.com/{CPVOD}/playlist.m3u8', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'}).json()['url']
           
           
            if 'khansirvod4.pc.cdn.bitgravity.com' in url:               
               parts = url.split('/')               
               part1 = parts[1]
               part2 = parts[2]
               part3 = parts[3] 
               part4 = parts[4]
               part5 = parts[5]
               
               print(f"PART1: {part1}")
               print(f"PART2: {part2}")
               print(f"PART3: {part3}")
               print(f"PART4: {part4}")
               print(f"PART5: {part5}")
               url = f"https://kgs-v4.akamaized.net/kgs-cv/{part3}/{part4}/{part5}"
           
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
          
            if "edge.api.brightcove.com" in url:
                bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzUxMzUzNjIsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiYmt3cmVIWmxZMFUwVXpkSmJYUkxVemw2ZW5Oclp6MDkiLCJmaXJzdF9uYW1lIjoiY25GdVpVdG5kRzR4U25sWVNGTjRiVW94VFhaUVVUMDkiLCJlbWFpbCI6ImFFWllPRXhKYVc1NWQyTlFTazk0YmtWWWJISTNRM3BKZW1OUVdIWXJWWE0wWldFNVIzZFNLelE0ZHowPSIsInBob25lIjoiZFhSNlFrSm9XVlpCYkN0clRUWTFOR3REU3pKTVVUMDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJhVVZGZGpBMk9XSnhlbXRZWm14amF6TTBVazQxUVQwOSIsImRldmljZV90eXBlIjoid2ViIiwiZGV2aWNlX3ZlcnNpb24iOiJDaHJvbWUrMTE5IiwiZGV2aWNlX21vZGVsIjoiY2hyb21lIiwicmVtb3RlX2FkZHIiOiIyNDA5OjQwYzI6MjA1NTo5MGQ0OjYzYmM6YTNjOTozMzBiOmIxOTkifX0.Kifitj1wCe_ohkdclvUt7WGuVBsQFiz7eezXoF1RduDJi4X7egejZlLZ0GCZmEKBwQpMJLvrdbAFIRniZoeAxL4FZ-pqIoYhH3PgZU6gWzKz5pdOCWfifnIzT5b3rzhDuG7sstfNiuNk9f-HMBievswEIPUC_ElazXdZPPt1gQqP7TmVg2Hjj6-JBcG7YPSqa6CUoXNDHpjWxK_KREnjWLM7vQ6J3vF1b7z_S3_CFti167C6UK5qb_turLnOUQzWzcwEaPGB3WXO0DAri6651WF33vzuzeclrcaQcMjum8n7VQ0Cl3fqypjaWD30btHQsu5j8j3pySWUlbyPVDOk-g'
                url = url.split("bcov_auth")[0]+bcov
            
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            
            elif "webvideos.classplusapp." in url:
               cmd = f'yt-dlp --add-header "referer:https://web.classplusapp.com/" --add-header "x-cdn-tag:empty" -f "{ytf}" "{url}" -o "{name}.mp4"'
          
            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'
          
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                cc = f'`✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦`\n\n[🎥]𝐕ɪᴅᴇᴏ 𝐈𝐃 ➤{str(count).zfill(3)}\n├──𝐓ɪᴛʟᴇ:➤`{name1}`\n├── 𝗥𝗲𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻 ➤ [{res}]\n├── 𝗙𝗼𝗿𝗺𝗮𝘁 ➤ 🇭‌🇦‌🇷‌🇮‌🇴‌🇲‌🤗.mkv<pre><code>📘 𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n🚀 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 :➤ {CR}\n\n`✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦`**'
                cc1 = f'`✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦`\n\n[📕] 𝐅ɪʟᴇ 𝐈𝐃 ➤{str(count).zfill(3)}\n├──𝐓ɪᴛʟᴇ:➤`{name1}`\n├── 𝗙𝗼𝗿𝗺𝗮𝘁 ➤ 🇭‌🇦‌🇷‌🇮‌🇴‌🇲‌🤗.pdf\n<pre><code>📘 𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n🚀 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 :➤{CR}\n\n`✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦**'                          
                cczip = f'`✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦`\n\n[🎥]𝐕ɪᴅᴇᴏ 𝐈𝐃 ➤{str(count).zfill(3)}\n├──𝐓ɪᴛʟᴇ:➤`{name1}`\n├── 𝗥𝗲𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻 ➤ [{res}]\n├── 𝗙𝗼𝗿𝗺𝗮𝘁 ➤ 🇭‌🇦‌🇷‌🇮‌🇴‌🇲‌🤗.mkv<pre><code>📘 𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n🚀 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 :➤ {CR}\n\n`✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦`**'
                cczip= f'`✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦`\n\n[📕] 𝐅ɪʟᴇ 𝐈𝐃 ➤{str(count).zfill(3)}\n├──𝐓ɪᴛʟᴇ:➤`{name1}`\n├── 𝗙𝗼𝗿𝗺𝗮𝘁 ➤ 🇭‌🇦‌🇷‌🇮‌🇴‌🇲‌🤗.pdf\n<pre><code>📘 𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n🚀 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 :➤{CR}\n\n`✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦`**'                       
                        
                    
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif ".pdf" in url:
                    try:
                        await asyncio.sleep(4)
        # Replace spaces with %20 in the URL
                        url = url.replace(" ", "%20")
 
        # Create a cloudscraper session
                        scraper = cloudscraper.create_scraper()

        # Send a GET request to download the PDF
                        response = scraper.get(url)

        # Check if the response status is OK
                        if response.status_code == 200:
            # Write the PDF content to a file
                            with open(f'{name}.pdf', 'wb') as file:
                                file.write(response.content)

            # Send the PDF document
                            await asyncio.sleep(4)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1

            # Remove the PDF file after sending
                            os.remove(f'{name}.pdf')
                        else:
                            await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                        
                #elif "muftukmall" in url:
                    #try:
                        #await bot.send_photo(chat_id=m.chat.id, photo=pwimg, caption=cpw)
                        #count +=1
                    #except Exception as e:
                        #await m.reply_text(str(e))    
                        #time.sleep(1)    
                        #continue
                
                #elif "youtu" in url:
                    #try:
                        #await bot.send_photo(chat_id=m.chat.id, photo=ytimg, caption=cyt)
                        #count +=1
                    #except Exception as e:
                        #await m.reply_text(str(e))    
                        #time.sleep(1)    
                        #continue

                elif "media-cdn.classplusapp.com/drm/" in url:
                    try:
                        await bot.send_photo(chat_id=m.chat.id, photo=cpimg, caption=cpvod)
                        count +=1
                    except Exception as e:
                        await m.reply_text(str(e))    
                        time.sleep(1)    
                        continue          
                        
                elif ".jpg" in url or ".png" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.jpg" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_photo(chat_id=m.chat.id, document=f'{name}.jpg', caption=cimg)
                        count += 1
                        os.remove(f'{name}.jpg')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        continue
                
                elif ".zip" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.zip" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.zip', caption=cczip)
                        count += 1
                        os.remove(f'{name}.zip')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        continue
                        
                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    emoji_message = await show_random_emojis(message)
                    progress = (count / len(links)) * 100
                    remaining_links = len(links) - count
                    Show =(  f'<pre><code>🚀 𝐏𝐑𝐎𝐆𝐑𝐄𝐒𝐒 🚀{progress:.2f}%</code></pre>\n\n'
                           f'**┠📊 Total Links ➤ {len(links)}\n**'
                           f'**┠⚡ Currently on ➤ {str(count)}/{len(links)}\n**'
                           f'**┠⏳ Remaining links ➤ {remaining_links}\n\n**'
                           f'**🚧 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐈𝐍𝐆.....🚧**\n\n'
                           f'<pre><code>**📘 𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤** `{b_name}` </code></pre>\n\n'
                           f'**⏳ Uploading Your videos may take some time**\n\n'
                           f'**╭────────◆◇◆────────╮\n ⚡ MADE BY ➤[🇭‌🇦‌🇷‌🇮‌🇴‌🇲](t.me/hariom_singh_001)\n╰────────◆◇◆────────╯**\n\n')
   
                    
                    prog = await m.reply_text(Show, disable_web_page_preview=True)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await emoji_message.delete()
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)


            except Exception as e:
                await m.reply_text(f'😉  ❌𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝❌\n\n'
                                   f'💎𝗡𝗮𝗺𝗲 » `{name}`\n\n'
                                   f'🔗𝗨𝗿𝗹 » <a href="{url}">__**Click Here to See Link**__</a>`')
                                   
                count += 1
                failed_count += 1
                continue   
                

    except Exception as e:
        await m.reply_text(e)
    #await m.reply_text("**🥳𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗗𝗼𝗻𝗲🥳**")
    await m.reply_text(
        f"⋅🌟 𝐁𝐚𝐭𝐜𝐡 𝐒𝐮𝐦𝐦𝐚𝐫𝐲 🌟\n━━━━━━━━━━━━━━━━━━━━\n"
      f"🔢 𝐈𝐧𝐝𝐞𝐱 𝐑𝐚𝐧𝐠𝐞 ➤ (**{raw_text}**➡️ **{len(links)}**)\n<pre><code>**📘 𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤** {b_name}</code></pre>\n━━━━━━━━━━━━━━━━━━━━\n"
      f"**✅ 𝐒𝐭𝐚𝐭𝐮𝐬 ➤ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞𝐝**"
    )
    await m.reply_text("<pre><code>That's It ❤️</code></pre>")

                    

bot.run()
if __name__ == "__main__":
    asyncio.run(main())
