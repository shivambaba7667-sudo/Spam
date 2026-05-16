import asyncio
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.constants import ChatType
from telegram.error import RetryAfter, TimedOut, NetworkError
import logging
import re
import random

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.WARNING
)

OWNER_ID = int(os.getenv("OWNER_ID", "6343729611"))
BOT_TOKENS = [
    os.getenv("8618313310:AAEhqm0_g5aq5ID79hPtr-dGP2tBcdBgKUM", ""),
    os.getenv("8948863617:AAEb7Sbo9WTRtOv0M45krX_NfNVff3u1AZc", ""),
    os.getenv("BOT_TOKEN_3", ""),
    os.getenv("BOT_TOKEN_4", ""),
    os.getenv("BOT_TOKEN_5", ""),
    os.getenv("BOT_TOKEN_6", ""),
    os.getenv("BOT_TOKEN_7", ""),
    os.getenv("BOT_TOKEN_8", ""),
    os.getenv("BOT_TOKEN_9", ""),
    os.getenv("BOT_TOKEN_10", ""),
    os.getenv("BOT_TOKEN_11", ""),
    os.getenv("BOT_TOKEN_12", ""),
    os.getenv("BOT_TOKEN_13", ""),
    os.getenv("BOT_TOKEN_14", ""),
]

BOT_TOKENS = [t for t in BOT_TOKENS if t]

if not BOT_TOKENS:
    print("ERROR: No bot tokens found! Set BOT_TOKEN_1, BOT_TOKEN_2, etc. environment variables")
    exit(1)

HEART_EMOJIS = ['❤️', '🧡', '💛', '💚', '💙', '💜', '🤎', '🖤', '🤍', '💘', '💝', '💖', '💗', '💓', '💞', '💌', '💕', '💟', '♥️', '❣️', '💔']

MOON_EMOJIS = ['🌙', '🌛', '🌜', '🌝', '🌚', '🌕', '🌖', '🌗', '🌘', '🌑', '🌒', '🌓', '🌔', '✨', '⭐', '🌟', '💫', '🌠']

NC_MOON_MESSAGES = [
    "{target} DOTZ ابو🌙",
    "🌓{target} 30 Bᴀᴀᴘ ʙᴀɴᴀ ᴋᴇ ɴᴀʜɪ ʙᴀᴄʜᴇɢᴀ ᴛᴜ 🌓",
    "🌑{target} Aᴀᴊᴀ ᴛᴜᴊʜᴇ ᴛɢ ʟᴇɴɢ ʙɴᴀᴜ🌑",
    "🌕{target} Tᴇʀɪ Mᴜᴍᴍʏ ᴋᴏ ʙʜᴏsᴅᴇ ᴍ ᴅʜᴀʀᴛɪ🌕",
    "🌖{target} Tᴇʀɪ ᴅᴀᴅᴅɪ Dᴏᴛᴢ Kɪ ᴅᴇᴇᴡᴀɴɪ🌖",
    "🌗{target} Tᴇʀɪ Mᴀᴀ Cʜᴜᴅᴇ 🌗",
    "🌘{target} ᴛᴇʀᴀ ʙᴀᴀᴘ ᴄʜᴋᴋᴀ🌘",
]

FLAG_EMOJIS = ['🏳️', '🏴', '🚩', '🎌', '🏁', '🇮🇳', '🏳️‍🌈', '🏴‍☠️', '⛳', '🎏', '🇦🇨', '🇧🇭', '🇧🇬', '🇦🇶', '🇦🇴', '🇦🇮', '🇦🇲', '🇦🇽', '🇦🇱', '🇦🇷','🏳️', '🏴', '🚩', '🎌', '🏁', '🇮🇳', '🏳️‍🌈', '🏴‍☠️', '⛳', '🎏']

NC_FLAG_MESSAGES = [
    "{target} 🚩",
    "{target} 🏳️🏴",
    "{target} 🎌🚩🎌",
    "{target} 🏁⛳🏁",
    "{target} 🎏🚩🎏",
    "{target} 🏴🚩🏴",
    "{target} ⛳🎌⛳",
]

NC_CURLY_MESSAGES = [
    "{{ {target} }}",
    "{{- {target} -}}",
    "{{★ {target} ★}}",
    "{{🔥 {target} 🔥}}",
    "{{🔱 {target} 🔱}}",
    "{{✨ {target} ✨}}",
    "{{🥀 {target} 🥀}}",
]

DOTZKENG_MESSAGES = [
    "⚡ {target} DOTZ KENG ABU ⚡",
    "🔥 {target} Tᴇʀɪ Mᴀᴀ Kɪ Cʜᴜᴛ Mᴇ Aᴀɢ 🔥",
    "👑 {target} DOTZ KENG Bᴀᴀᴘ Hᴀɪ Tᴇʀᴀ 👑",
    "💀 {target} Kʜᴀᴍᴏsʜɪ Sᴇ Cʜᴜᴅ Jᴀ 💀",
    "💥 {target} DOTZ KENG Sᴇ Pᴀɴɢᴀ Mᴀᴛ Lᴇ 💥",
    "🚀 {target} Tᴇʀɪ Bᴇʜɴ Kɪ Cʜᴜᴛ Mᴇ Rᴏᴄᴋᴇᴛ 🚀",
    "🦾 {target} DOTZ KENG Pᴏᴡᴇʀ 🦾",
]

FLOWER_NC_MESSAGES = [
    "༄˖°.🥀.ೃ࿔*:･{target} ",
    "༄˖°.💮.ೃ࿔*:･{target} ",
    "༄˖°.💠.ೃ࿔*:･{target} ",
    "༄˖°.🌻.ೃ࿔*:･{target} ",
    "༄˖°.🌺.ೃ࿔*:･{target} ",
    "༄˖°.🌸.ೃ࿔*:･{target} ",
    "༄˖°.🌷.ೃ࿔*:･{target} ",
]

UNAUTHORIZED_MESSAGE = "- 𝐍ꫝɢꫝsᴀᴋɪ⋆͙🐉 अब्बू की कॉपी करेगा Bsᴅᴋ"

NAME_CHANGE_MESSAGES = [
    "{target} ᴛʀʏᴍᴀ ʀɴᴅᴏ ♥️",
    "{target} ᴛʀʏᴍᴀ ʀɴᴅᴏ ❌",
    "{target} ᴛʀʏᴍᴀ ʀɴᴅᴏ 🚫",
    "{target} ᴛʀʏᴍᴀ ʀɴᴅᴏ 🛑",
    "{target} ᴛʀʏᴍᴀ ʀɴᴅᴏ ⛔",
    "{target} ᴛʀʏᴍᴀ ʀɴᴅᴏ ♨️",
    "{target} ᴛʀʏᴍᴀ ʀɴᴅᴏ ⭕",
]

REPLY_MESSAGES = [
    "{target} Tᴇʀɪ ᴍᴀᴀ ɢᴜʟᴀᴍ ʜ ʙᴇᴛᴇ🐣",
    "{target} Cᴜᴅ Cᴜᴅ Cᴜᴅ -!🩴🔥",
    "Aʟᴏᴏ Kʜᴀᴋᴇ {target} Tᴇʀɪ ᴍᴏᴍ Cᴏᴍ Qᴜᴇᴇɴ 👑♥️",
    "{target} Hɪᴊᴅᴀ Tᴇʀᴇ Bᴀᴀᴘ ᴋɪ Cʜᴜᴛ🤳🏻👋🏻",
    "{target} Tᴇʀᴇ Bᴀᴀᴘ Kɪ ʙᴋʙ🔥✨",
    "{target} Tᴜ ᴋʀᴇɢᴀ Sᴘᴀᴍ Hᴀssɪ🔃💠",
    "{target} Tᴇʀɪ Bʜᴇɴ Cʜᴏᴅᴇ Dɪɴᴀsᴀᴜʀ🦖😈",
    "{target} Aᴛᴍᴋʙғᴛᴊɢ🖤🙊",
    "{target} Kᴜᴛɪʏᴀ Kᴇ ʟᴀᴅᴋᴇ🌷😭",
    "{target} Tᴇʀᴀ ʙᴀᴀᴘ Tᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴇ Bʙᴄ Bᴀɴᴋᴇ😨♥️",
    "{target} Sɪʟᴀɪ Wᴀʟʏ ᴋᴇ ʟᴀᴅᴋᴇ Tʀʏ Mᴀᴀ ᴋᴀ ʙʜᴏsᴅᴀ Sɪʟ ᴅᴜ? 💀🥵",
    "{target} Tʀʏ ᴍᴀᴀ ᴘᴀᴅʜᴇ Bᴏᴏᴋ Wᴏʜ Hᴏᴋᴇ ᴄʜᴜᴅᴇɢɪ Cᴏᴏᴋ 🥧🧑🏻‍🍳",
    "{target} Eᴠᴇʀʏᴛʜɪɴɢ Is Tᴇᴍᴘᴏʀᴀʀʏ Bᴜᴛ Tʀɪ Cʜᴜᴅᴀɪ Is ᴘᴇʀᴍᴀɴᴇɴᴛ 🦠🦷",
    "{target} ᴋᴀʜᴀ ᴛᴇ ʙʜᴀɢᴇɢᴀ Eᴋ ʀᴇʜᴘᴀᴛ ᴍ ᴛᴇʀᴀ Rᴀᴘᴇ ʜᴏᴊʏᴇɢᴀ Bʜᴇɴɢᴇ🦘🪽",
    "{target} Tᴇʀɪ Mᴀᴀ ᴘᴇsᴇ ᴋᴀᴍᴀᴛᴇ ᴋᴀᴍᴀᴛᴇ ɴᴀɴɢɪ Hᴜɪ 👩🏻‍⚕️👩🏻‍🎤",
    "{target} Tᴇʀɪ ᴍᴀᴀ ᴋᴏ Mᴇʀᴇ FᴀʀᴍHᴏᴜsᴇ P ʙʜᴇᴊᴅᴇ🥩🍏",
    "{target} Kᴜᴛɪʏᴀ Kᴇ ʙʜᴏsᴅᴇ Kɪ ᴀᴜʟᴀᴅ😈👋🏻",
    "{target} ʙᴏʟᴇ ɴᴀɢᴀsᴀᴋɪ Kɪ ᴊᴀɪ Hᴏ🕳️🔥",
    "{target} ʜɪᴊᴅᴀ ʜ ᴛᴜ ɢʀᴇᴇʙ💮🥀",
    "{target} ᴛᴇʀɪ ᴍᴀᴀ ʙᴏʟᴇ ɴᴀɢᴀsᴀᴋɪ अब्बू ʜᴀɪ ᴍᴇʀᴇ🩴🔥",
]

SPAM_MESSAGE_TEMPLATE = """ {target} ˙ Tᴜ 2ᴅɪɴ Pᴇʜʟᴇ Aʏᴀ Sᴘᴀᴍᴍᴇʀ 1 Sᴀᴀʟ Tɪᴋɴᴇ Kɪ ʙᴀᴀᴛ ᴋʀʀʜᴀ ? तेज वाली हस्सी Yᴀʀʀ Mᴛᴛ Cʀᴏᴡ Tᴜᴍ Nᴇᴡɢᴇɴ ʜᴏ  . ꒷ 🥀 . 𖦹˙— 💠 {target} ˙ Tᴜ 2ᴅɪɴ Pᴇʜʟᴇ Aʏᴀ Sᴘᴀᴍᴍᴇʀ 1 Sᴀᴀʟ Tɪᴋɴᴇ Kɪ ʙᴀᴀᴛ ᴋʀʀʜᴀ ? तेज वाली हस्सी Yᴀʀʀ Mᴛᴛ Cʀᴏᴡ Tᴜᴍ Nᴇᴡɢᴇɴ ʜᴏ  . ꒷ 🥀 . 𖦹˙— 💠{target} ˙ Tᴜ 2ᴅɪɴ Pᴇʜʟᴇ Aʏᴀ Sᴘᴀᴍᴍᴇʀ 1 Sᴀᴀʟ Tɪᴋɴᴇ Kɪ ʙᴀᴀᴛ ᴋʀʀʜᴀ ? तेज वाली हस्सी Yᴀʀʀ Mᴛᴛ Cʀᴏᴡ Tᴜᴍ Nᴇᴡɢᴇɴ ʜᴏ  . ꒷ 🥀 . 𖦹˙— 💠{target} ˙ Tᴜ 2ᴅɪɴ Pᴇʜʟᴇ Aʏᴀ Sᴘᴀᴍᴍᴇʀ 1 Sᴀᴀʟ Tɪᴋɴᴇ Kɪ ʙᴀᴀᴛ ᴋʀʀʜᴀ ? तेज वाली हस्सी Yᴀʀʀ Mᴛᴛ Cʀᴏᴡ Tᴜᴍ Nᴇᴡɢᴇɴ ʜᴏ  . ꒷ 🥀 . 𖦹˙— 💠{target} ˙ Tᴜ 2ᴅɪɴ Pᴇʜʟᴇ Aʏᴀ Sᴘᴀᴍᴍᴇʀ 1 Sᴀᴀʟ Tɪᴋɴᴇ Kɪ ʙᴀᴀᴛ ᴋʀʀʜᴀ ? तेज वाली हस्सी Yᴀʀʀ Mᴛᴛ Cʀᴏᴡ Tᴜᴍ Nᴇᴡɢᴇɴ ʜᴏ  . ꒷ 🥀 . 𖦹˙— 💠{target} ˙ Tᴜ 2ᴅɪɴ Pᴇʜʟᴇ Aʏᴀ Sᴘᴀᴍᴍᴇʀ 1 Sᴀᴀʟ Tɪᴋɴᴇ Kɪ ʙᴀᴀᴛ ᴋʀʀʜᴀ ? तेज वाली हस्सी Yᴀʀʀ Mᴛᴛ Cʀᴏᴡ Tᴜᴍ Nᴇᴡɢᴇɴ ʜᴏ  . ꒷ 🥀 . 𖦹˙— 💠{target} ˙ Tᴜ 2ᴅɪɴ Pᴇʜʟᴇ Aʏᴀ Sᴘᴀᴍᴍᴇʀ 1 Sᴀᴀʟ Tɪᴋɴᴇ Kɪ ʙᴀᴀᴛ ᴋʀʀʜᴀ ? तेज वाली हस्सी Yᴀʀʀ Mᴛᴛ Cʀᴏᴡ Tᴜᴍ Nᴇᴡɢᴇɴ ʜᴏ  . ꒷ 🥀 . 𖦹˙— 💠{target} ˙ Tᴜ 2ᴅɪɴ Pᴇʜʟᴇ Aʏᴀ Sᴘᴀᴍᴍᴇʀ 1 Sᴀᴀʟ Tɪᴋɴᴇ Kɪ ʙᴀᴀᴛ ᴋʀʀʜᴀ ? तेज वाली हस्सी Yᴀʀʀ Mᴛᴛ Cʀᴏᴡ Tᴜᴍ Nᴇᴡɢᴇɴ ʜᴏ  . ꒷ 🥀 . 𖦹˙— 💠 {target} ˙ Tᴜ 2ᴅɪɴ Pᴇʜʟᴇ Aʏᴀ Sᴘᴀᴍᴍᴇʀ 1 Sᴀᴀʟ Tɪᴋɴᴇ Kɪ ʙᴀᴀᴛ ᴋʀʀʜᴀ ? तेज वाली हस्सी Yᴀʀʀ Mᴛᴛ Cʀᴏᴡ Tᴜᴍ Nᴇᴡɢᴇɴ ʜᴏ  . ꒷ 🥀 . 𖦹˙— 💠{target} ˙ Tᴜ 2ᴅɪɴ Pᴇʜʟᴇ Aʏᴀ Sᴘᴀᴍᴍᴇʀ 1 Sᴀᴀʟ Tɪᴋɴᴇ Kɪ ʙᴀᴀᴛ ᴋʀʀʜᴀ ? तेज वाली हस्सी Yᴀʀʀ Mᴛᴛ Cʀᴏᴡ Tᴜᴍ Nᴇᴡɢᴇɴ ʜᴏ  . ꒷ 🥀 . 𖦹˙— 💠{target} ˙ Tᴜ 2ᴅɪɴ Pᴇʜʟᴇ Aʏᴀ Sᴘᴀᴍᴍᴇʀ 1 Sᴀᴀʟ Tɪᴋɴᴇ Kɪ ʙᴀᴀᴛ ᴋʀʀʜᴀ ? तेज वाली हस्सी Yᴀʀʀ Mᴛᴛ Cʀᴏᴡ Tᴜᴍ Nᴇᴡɢᴇɴ ʜᴏ  . ꒷ 🥀 . 𖦹˙— 💠{target} ˙ Tᴜ 2ᴅɪɴ Pᴇʜʟᴇ Aʏᴀ Sᴘᴀᴍᴍᴇʀ 1 Sᴀᴀʟ Tɪᴋɴᴇ Kɪ ʙᴀᴀᴛ ᴋʀʀʜᴀ ? तेज वाली हस्सी Yᴀʀʀ Mᴛᴛ Cʀᴏᴡ Tᴜᴍ Nᴇᴡɢᴇɴ ʜᴏ  . ꒷ 🥀 . 𖦹˙— 💠{target} ˙ Tᴜ 2ᴅɪɴ Pᴇʜʟᴇ Aʏᴀ Sᴘᴀᴍᴍᴇʀ 1 Sᴀᴀʟ Tɪᴋɴᴇ Kɪ ʙᴀᴀᴛ ᴋʀʀʜᴀ ? तेज वाली हस्सी Yᴀʀʀ Mᴛᴛ Cʀᴏᴡ Tᴜᴍ Nᴇᴡɢᴇɴ ʜᴏ  . ꒷ 🥀 . 𖦹˙— 💠{target} ˙ Tᴜ 2ᴅɪɴ Pᴇʜʟᴇ Aʏᴀ Sᴘᴀᴍᴍᴇʀ 1 Sᴀᴀʟ Tɪᴋɴᴇ Kɪ ʙᴀᴀᴛ ᴋʀʀʜᴀ ? तेज वाली हस्सी Yᴀʀʀ Mᴛᴛ Cʀᴏᴡ Tᴜᴍ Nᴇᴡɢᴇɴ ʜᴏ  . ꒷ 🥀 . 𖦹˙— 💠 """


def extract_retry_after(error_str):
    match = re.search(r'retry after (\d+)', error_str.lower())
    if match:
        return int(match.group(1))
    return None


class BotInstance:
    def __init__(self, bot_number, owner_id):
        self.bot_number = bot_number
        self.owner_id = owner_id
        self.sudo_users = set()
        self.active_spam_tasks = {}
        self.active_name_change_tasks = {}
        self.active_ncmoon_tasks = {}
        self.active_ncflag_tasks = {}
        self.active_dotzkeng_tasks = {}
        self.active_curly_tasks = {}
        self.active_reply_tasks = {}
        self.active_reply_targets = {}
        self.pending_replies = {}
        self.chat_delays = {}
        self.chat_threads = {}
        self.locks = {}

    def get_lock(self, chat_id):
        if chat_id not in self.locks:
            self.locks[chat_id] = asyncio.Lock()
        return self.locks[chat_id]

    def is_owner(self, user_id):
        return user_id == self.owner_id or user_id in self.sudo_users

    async def sudo_command(self, update, context):
        if update.effective_user.id != self.owner_id:
            return

        if not context.args and not update.message.reply_to_message:
            await update.message.reply_text("Usage: -sudo @username or reply to a message with -sudo")
            return

        user_to_sudo = None
        if update.message.reply_to_message:
            user_to_sudo = update.message.reply_to_message.from_user.id
        else:
            # Try to get user from mention or ID
            arg = context.args[0]
            if arg.startswith("@"):
                # Note: CommandHandler doesn't resolve usernames to IDs automatically
                # This usually requires the user to be in the bot's cache
                await update.message.reply_text("Please reply to the user's message with -sudo to grant sudo.")
                return
            else:
                try:
                    user_to_sudo = int(arg)
                except ValueError:
                    await update.message.reply_text("Invalid User ID.")
                    return

        if user_to_sudo:
            self.sudo_users.add(user_to_sudo)
            await update.message.reply_text(f"User {user_to_sudo} granted SUDO powers! ✅")

    async def refresh_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        await update.message.reply_text(f"Bot {self.bot_number} is active and refreshed! ⚡")

    async def check_owner(self, update):
        user_id = update.effective_user.id
        if not self.is_owner(user_id):
            try:
                await update.message.reply_text(UNAUTHORIZED_MESSAGE)
            except Exception:
                pass
            return False
        return True

    async def start(self, update, context):
        if not await self.check_owner(update):
            return

        help_text = f"""
𓆩 𝐁𝐎𝐓 {self.bot_number} 𓆪 - 𝐓𝐇𝐄 𝐆𝐑𝐄𝐀𝐓 𝐍ꫝɢꫝsᴀ𝐊𝐢⋆͙🐉 अब्बू'𝐒 𝐁𝐎𝐓 

𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:
-target <target> Spam+Ncs Loops With Threads ✅
-nc <target> Name Change Loop With Threads ✅
-dotzkeng <name> Themed Name Change Loop ✅
-nccurly <name> Double Curly Loop ✅
-flowernc <name> Flower Name Change Loop ✅
-ncmoon <target> Name Change With Moon Loop ✅
-ncflag <target> Name Change With Flag Loop ✅
-ncemo <target> Name Change With Emojis Loop ✅
-spam <target> Spam Loops With Threads ✅
-reply <target> Replys All Targeted Loop ✅!
-ping Check Bot Latency/Speed ✅
-gc Automatic Group Image Change Loop ✅
-setgc <1 or 2> Set image slot 1 or 2 ✅

-delay <milliseconds> Set between <0-10> ✅
-threads <1-50> Set Threads For Nc + Spams ✅

-stopnc Stops All Name Change Loops ✅
-stopdotzkeng Stops DOTZKENG Loop ✅
-stopnccurly Stops Double Curly Loop ✅
-stopncmoon Stops NC Moon Loop ✅
-stopncflag Stops NC Flag Loop ✅
-stopspam Stops All Spam Loops ✅
-stopreply Stops All Reply Loops ✅
-stopall Stops All Spam - Ncs ✅

Threads: 1-50 All (Actions run in Loops - for (Owner-Sudo) ✅)
"""
        await update.message.reply_text(help_text)

    async def name_change_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(NAME_CHANGE_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] Name change LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = NAME_CHANGE_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    # Base delay of 0.1s to avoid immediate flood, plus user delay
                    await asyncio.sleep(max(delay, 0.1))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    # Add extra buffer to satisfy Telegram's cooling period
                    await asyncio.sleep(wait_time + 1.0)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(1.0)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 1.0)
                    else:
                        await asyncio.sleep(1.0)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] Name change LOOP #{worker_id} stopped after {success_count} changes")

    async def flower_nc_loop(self, chat_id, base_name, context):
        msg_index = 0
        num_messages = len(FLOWER_NC_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] FLOWER NC LOOP started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = FLOWER_NC_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] FLOWER NC LOOP stopped after {success_count} changes")

    async def nc_emo_loop(self, chat_id, base_name, context):
        success_count = 0
        print(f"[Bot {self.bot_number}] NC EMO LOOP started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    emoji = random.choice(HEART_EMOJIS)
                    display_name = f"{emoji} {base_name} {emoji}"
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except Exception:
                    await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] NC EMO LOOP stopped after {success_count} changes")

    async def nc_moon_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(NC_MOON_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] NC MOON LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = NC_MOON_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] NC MOON LOOP #{worker_id} stopped after {success_count} changes")

    async def nc_flag_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(NC_FLAG_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] NC FLAG LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = NC_FLAG_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] NC FLAG LOOP #{worker_id} stopped after {success_count} changes")

    async def dotzkeng_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(DOTZKENG_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] DOTZKENG LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = DOTZKENG_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] DOTZKENG LOOP #{worker_id} stopped after {success_count} changes")

    async def curly_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(NC_CURLY_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] CURLY LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = NC_CURLY_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] CURLY LOOP #{worker_id} stopped after {success_count} changes")

    async def gc_loop(self, chat_id, context):
        success_count = 0
        print(f"[Bot {self.bot_number}] GC LOOP started for chat {chat_id}")
        image_paths = ["gc_image_1.png", "gc_image_2.png"]
        msg_index = 0
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    # Find which images exist
                    available_images = [p for p in image_paths if os.path.exists(p)]
                    
                    if available_images:
                        current_path = available_images[msg_index % len(available_images)]
                        with open(current_path, 'rb') as photo:
                            await context.bot.set_chat_photo(chat_id=chat_id, photo=photo)
                        success_count += 1
                        msg_index += 1
                        # Base delay for photo changes should be slightly higher to avoid immediate ban
                        await asyncio.sleep(max(delay, 2.0))
                    else:
                        await asyncio.sleep(5.0)
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 1.0)
                except Exception as e:
                    print(f"[Bot {self.bot_number}] GC Error: {e}")
                    await asyncio.sleep(5.0)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] GC LOOP stopped after {success_count} changes")

    async def set_gc_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        message = update.message
        photo = None
        
        if message.reply_to_message and message.reply_to_message.photo:
            photo = message.reply_to_message.photo[-1]
        elif message.photo:
            photo = message.photo[-1]
            
        if not photo:
            await update.message.reply_text("Usage: Reply to a photo with -setgc [1 or 2] or send a photo with -setgc [1 or 2] caption")
            return
            
        # Determine slot
        slot = "1"
        if context.args:
            if context.args[0] in ["1", "2"]:
                slot = context.args[0]
            
        filename = f"gc_image_{slot}.png"
        file = await context.bot.get_file(photo.file_id)
        await file.download_to_drive(filename)
        await update.message.reply_text(f"Group image saved to Slot {slot}! ✅ Use -gc to start the loop cycling between available images.")

    async def ping_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        import time
        start_time = time.time()
        sent_message = await update.message.reply_text("Pinging...")
        end_time = time.time()
        
        latency = (end_time - start_time) * 1000
        await sent_message.edit_text(f"Bot {self.bot_number} Ping: {latency:.2f}ms ⚡")

    async def spam_loop(self, chat_id, target_name, context, worker_id):
        success_count = 0
        print(f"[Bot {self.bot_number}] Spam LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    spam_msg = SPAM_MESSAGE_TEMPLATE.format(target=target_name)
                    await context.bot.send_message(chat_id=chat_id, text=spam_msg)
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.1))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 1.0)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(1.0)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 1.0)
                    else:
                        await asyncio.sleep(1.0)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] Spam LOOP #{worker_id} stopped after {success_count} messages")

    async def reply_loop(self, chat_id, target_name, context):
        success_count = 0
        print(f"[Bot {self.bot_number}] Reply LOOP started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                if chat_id in self.pending_replies and self.pending_replies[chat_id]:
                    async with self.get_lock(chat_id):
                        messages_to_reply = self.pending_replies[chat_id].copy()
                        self.pending_replies[chat_id] = []

                    for msg_id in messages_to_reply:
                        try:
                            reply_msg = random.choice(REPLY_MESSAGES).format(target=target_name)
                            await context.bot.send_message(
                                chat_id=chat_id, 
                                text=reply_msg,
                                reply_to_message_id=msg_id
                            )
                            success_count += 1
                            await asyncio.sleep(max(delay, 0.05))
                        except asyncio.CancelledError:
                            raise
                        except RetryAfter as e:
                            wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                            await asyncio.sleep(wait_time + 0.1)
                        except Exception:
                            await asyncio.sleep(0.5)
                else:
                    await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] Reply LOOP stopped after {success_count} replies")

    async def message_collector(self, update, context):
        if not update.message or not update.message.text:
            return

        text = update.message.text.lower()
        chat_id = update.effective_chat.id

        # Trigger for taixochutiya
        if "taixochutiya" in text:
            await update.message.reply_text("TAIXO Tᴇʀɪ ᴍᴏᴍ Cᴏᴍ Qᴜᴇᴇɴ 👑♥️")
            return

        if chat_id in self.active_reply_targets:
            msg_id = update.message.message_id
            async with self.get_lock(chat_id):
                if chat_id not in self.pending_replies:
                    self.pending_replies[chat_id] = []
                self.pending_replies[chat_id].append(msg_id)

    async def nc_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /nc <name>")
            return

        base_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_name_change_tasks:
            old_tasks = self.active_name_change_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.name_change_loop(chat_id, base_name, context, i+1))
            tasks.append(task)

        self.active_name_change_tasks[chat_id] = tasks

        await update.message.reply_text(f"[Bot {self.bot_number}] ⚡ Name change LOOP started with {num_threads} threads!")

    async def stop_nc_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        if chat_id in self.active_name_change_tasks:
            tasks = self.active_name_change_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_name_change_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] Name change LOOP stopped!")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active name change loop!")

    async def spam_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /spam <target>")
            return

        target_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_spam_tasks:
            tasks = self.active_spam_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.spam_loop(chat_id, target_name, context, i+1))
            tasks.append(task)

        self.active_spam_tasks[chat_id] = tasks
        await update.message.reply_text(f"[Bot {self.bot_number}] 💣 Spam LOOP started with {num_threads} threads! Running continuously...")

    async def stop_spam_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        if chat_id in self.active_spam_tasks:
            tasks = self.active_spam_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_spam_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] Spam LOOP stopped!")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active spam loop!")

    async def target_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /target <name>")
            return

        target_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_name_change_tasks:
            old_tasks = self.active_name_change_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        if chat_id in self.active_spam_tasks:
            tasks = self.active_spam_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        num_threads = self.chat_threads.get(chat_id, 1)

        nc_tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.name_change_loop(chat_id, target_name, context, i+1))
            nc_tasks.append(task)
        self.active_name_change_tasks[chat_id] = nc_tasks

        spam_tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.spam_loop(chat_id, target_name, context, i+1))
            spam_tasks.append(task)
        self.active_spam_tasks[chat_id] = spam_tasks

        total_threads = num_threads * 2
        await update.message.reply_text(f"[Bot {self.bot_number}] 🎯 TARGET MODE: NC ({num_threads}) + SPAM ({num_threads}) = {total_threads} threads running!")

    async def reply_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /reply <target>")
            return

        target_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_reply_tasks:
            old_task = self.active_reply_tasks[chat_id]
            old_task.cancel()
            try:
                await old_task
            except asyncio.CancelledError:
                pass

        self.active_reply_targets[chat_id] = target_name
        self.pending_replies[chat_id] = []

        task = asyncio.create_task(self.reply_loop(chat_id, target_name, context))
        self.active_reply_tasks[chat_id] = task

        await update.message.reply_text(f"[Bot {self.bot_number}] 💬 Reply LOOP activated! Replying to every message...")

    async def stop_reply_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        if chat_id in self.active_reply_tasks:
            task = self.active_reply_tasks[chat_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.active_reply_tasks[chat_id]

        if chat_id in self.active_reply_targets:
            del self.active_reply_targets[chat_id]

        if chat_id in self.pending_replies:
            del self.pending_replies[chat_id]

        await update.message.reply_text(f"[Bot {self.bot_number}] Reply LOOP stopped!")

    async def delay_command(self, update, context):
        if not await self.check_owner(update):
            return

        if not context.args:
            await update.message.reply_text("Usage: /delay <seconds>")
            return

        try:
            delay = float(context.args[0])
            if delay < 0:
                await update.message.reply_text("Delay must be >= 0")
                return

            chat_id = update.effective_chat.id
            self.chat_delays[chat_id] = delay
            await update.message.reply_text(f"[Bot {self.bot_number}] Delay set to {delay}s (applies to all loops)")
        except ValueError:
            await update.message.reply_text("Invalid delay value!")

    async def threads_command(self, update, context):
        if not await self.check_owner(update):
            return

        if not context.args:
            await update.message.reply_text("Usage: /threads <number>")
            return

        try:
            threads = int(context.args[0])
            if threads < 1 or threads > 50:
                await update.message.reply_text("Threads must be between 1 and 50")
                return

            chat_id = update.effective_chat.id
            self.chat_threads[chat_id] = threads
            await update.message.reply_text(f"[Bot {self.bot_number}] Threads set to {threads} (applies to NC + SPAM)")
        except ValueError:
            await update.message.reply_text("Invalid threads value!")

    async def stop_all_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id
        stopped = []

        # List of all task categories to stop
        task_categories = [
            (self.active_name_change_tasks, "name change loop"),
            (self.active_ncmoon_tasks, "nc moon loop"),
            (self.active_ncflag_tasks, "nc flag loop"),
            (self.active_dotzkeng_tasks, "dotzkeng loop"),
            (self.active_curly_tasks, "curly loop"),
            (self.active_spam_tasks, "spam loop")
        ]

        for task_dict, label in task_categories:
            if chat_id in task_dict:
                tasks = task_dict[chat_id]
                # Handle both list of tasks and single task
                if not isinstance(tasks, list):
                    tasks = [tasks]
                for task in tasks:
                    task.cancel()
                for task in tasks:
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
                del task_dict[chat_id]
                stopped.append(label)

        if chat_id in self.active_reply_tasks:
            task = self.active_reply_tasks[chat_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.active_reply_tasks[chat_id]
            stopped.append("reply loop")

        if chat_id in self.active_reply_targets:
            del self.active_reply_targets[chat_id]

        if chat_id in self.pending_replies:
            del self.pending_replies[chat_id]

        if hasattr(self, 'active_gc_tasks') and chat_id in self.active_gc_tasks:
            task = self.active_gc_tasks[chat_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.active_gc_tasks[chat_id]
            stopped.append("gc loop")

        if stopped:
            await update.message.reply_text(f"[Bot {self.bot_number}] Stopped: {', '.join(stopped)} ✅")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active loops to stop!")

    async def flower_nc_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: -flowernc <name>")
            return
        base_name = " ".join(context.args)
        chat_id = chat.id
        
        # Stop existing loops in this category
        if chat_id in self.active_name_change_tasks:
            tasks = self.active_name_change_tasks[chat_id]
            for task in tasks: task.cancel()
            del self.active_name_change_tasks[chat_id]
            
        task = asyncio.create_task(self.flower_nc_loop(chat_id, base_name, context))
        self.active_name_change_tasks[chat_id] = [task]
        await update.message.reply_text(f"[Bot {self.bot_number}] 🌸 FLOWER NC LOOP started!")

    async def nc_emo_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: /ncemo <name>")
            return
        base_name = " ".join(context.args)
        chat_id = chat.id
        if chat_id in self.active_name_change_tasks:
            tasks = self.active_name_change_tasks[chat_id]
            for task in tasks: task.cancel()
            del self.active_name_change_tasks[chat_id]
        task = asyncio.create_task(self.nc_emo_loop(chat_id, base_name, context))
        self.active_name_change_tasks[chat_id] = [task]
        await update.message.reply_text(f"[Bot {self.bot_number}] ⚡ NC EMO LOOP started!")

    async def ncmoon_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: /ncmoon <name>")
            return
        base_name = " ".join(context.args)
        chat_id = chat.id
        if chat_id in self.active_ncmoon_tasks:
            old_tasks = self.active_ncmoon_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.nc_moon_loop(chat_id, base_name, context, i+1))
            tasks.append(task)
        self.active_ncmoon_tasks[chat_id] = tasks
        await update.message.reply_text(f"[Bot {self.bot_number}] 🌙 NC MOON LOOP started with {num_threads} threads!")

    async def stop_ncmoon_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat_id = update.effective_chat.id
        if chat_id in self.active_ncmoon_tasks:
            tasks = self.active_ncmoon_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_ncmoon_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] NC MOON LOOP stopped!")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active NC Moon loop!")

    async def ncflag_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: /ncflag <name>")
            return
        base_name = " ".join(context.args)
        chat_id = chat.id
        if chat_id in self.active_ncflag_tasks:
            old_tasks = self.active_ncflag_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.nc_flag_loop(chat_id, base_name, context, i+1))
            tasks.append(task)
        self.active_ncflag_tasks[chat_id] = tasks
        await update.message.reply_text(f"[Bot {self.bot_number}] 🚩 NC FLAG LOOP started with {num_threads} threads!")

    async def stop_ncflag_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat_id = update.effective_chat.id
        if chat_id in self.active_ncflag_tasks:
            tasks = self.active_ncflag_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_ncflag_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] NC FLAG LOOP stopped!")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active NC Flag loop!")

    async def dotzkeng_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: -dotzkeng <name>")
            return

        base_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_dotzkeng_tasks:
            old_tasks = self.active_dotzkeng_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.dotzkeng_loop(chat_id, base_name, context, i+1))
            tasks.append(task)

        self.active_dotzkeng_tasks[chat_id] = tasks
        await update.message.reply_text(f"[Bot {self.bot_number}] ⚡ DOTZKENG LOOP started with {num_threads} threads!")

    async def stop_dotzkeng_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat_id = update.effective_chat.id
        if chat_id in self.active_dotzkeng_tasks:
            tasks = self.active_dotzkeng_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_dotzkeng_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] DOTZKENG LOOP stopped!")
        else:
            await update.message.reply_text("No active DOTZKENG LOOP found.")

    async def nccurly_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: -nccurly <name>")
            return
        
        target_name = " ".join(context.args)
        chat_id = chat.id
        threads = self.chat_threads.get(chat_id, 1)

        if chat_id in self.active_curly_tasks:
            for task in self.active_curly_tasks[chat_id]:
                task.cancel()
        
        self.active_curly_tasks[chat_id] = []
        for i in range(threads):
            task = asyncio.create_task(self.curly_loop(chat_id, target_name, context, i+1))
            self.active_curly_tasks[chat_id].append(task)
        
        await update.message.reply_text(f"[Bot {self.bot_number}] Double Curly loop started for '{target_name}' with {threads} threads! 🌀")

    async def stop_nccurly_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat_id = update.effective_chat.id
        if chat_id in self.active_curly_tasks:
            for task in self.active_curly_tasks[chat_id]:
                task.cancel()
            for task in self.active_curly_tasks[chat_id]:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_curly_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] Double Curly loop stopped! 🛑")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active Double Curly loop!")

    async def gc_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        chat_id = chat.id
        task = asyncio.create_task(self.gc_loop(chat_id, context))
        # Store in a new dict or reuse active_spam_tasks if appropriate
        if not hasattr(self, 'active_gc_tasks'): self.active_gc_tasks = {}
        self.active_gc_tasks[chat_id] = task
        await update.message.reply_text(f"[Bot {self.bot_number}] 🖼️ Group Image Change LOOP started!")


def create_bot_application(token, bot_number, owner_id):
    application = Application.builder().token(token).build()
    bot_instance = BotInstance(bot_number, owner_id)

    # Standard command handlers
    application.add_handler(CommandHandler("start", bot_instance.start))
    application.add_handler(CommandHandler("nc", bot_instance.nc_command))
    application.add_handler(CommandHandler("ncemo", bot_instance.nc_emo_command))
    application.add_handler(CommandHandler("ncmoon", bot_instance.ncmoon_command))
    application.add_handler(CommandHandler("ncflag", bot_instance.ncflag_command))
    application.add_handler(CommandHandler("stopnc", bot_instance.stop_nc_command))
    application.add_handler(CommandHandler("stopncmoon", bot_instance.stop_ncmoon_command))
    application.add_handler(CommandHandler("stopncflag", bot_instance.stop_ncflag_command))
    application.add_handler(CommandHandler("spam", bot_instance.spam_command))
    application.add_handler(CommandHandler("stopspam", bot_instance.stop_spam_command))
    application.add_handler(CommandHandler("target", bot_instance.target_command))
    application.add_handler(CommandHandler("reply", bot_instance.reply_command))
    application.add_handler(CommandHandler("stopreply", bot_instance.stop_reply_command))
    application.add_handler(CommandHandler("delay", bot_instance.delay_command))
    application.add_handler(CommandHandler("threads", bot_instance.threads_command))
    application.add_handler(CommandHandler("stopall", bot_instance.stop_all_command))
    application.add_handler(CommandHandler("gc", bot_instance.gc_command))
    application.add_handler(CommandHandler("sudo", bot_instance.sudo_command))

    # Custom handler for prefix '-'
    async def prefix_handler(update, context):
        if not update.message or not update.message.text:
            return
        text = update.message.text
        if text.startswith('-'):
            parts = text[1:].split()
            if not parts:
                return
            command = parts[0].lower()
            context.args = parts[1:]
            
            cmd_map = {
                "start": bot_instance.start,
                "nc": bot_instance.nc_command,
                "stopnc": bot_instance.stop_nc_command,
                "spam": bot_instance.spam_command,
                "stopspam": bot_instance.stop_spam_command,
                "delay": bot_instance.delay_command,
                "threads": bot_instance.threads_command,
                "target": bot_instance.target_command,
                "stopall": bot_instance.stop_all_command,
                "ncmoon": bot_instance.ncmoon_command,
                "stopncmoon": bot_instance.stop_ncmoon_command,
                "ncflag": bot_instance.ncflag_command,
                "stopncflag": bot_instance.stop_ncflag_command,
                "dotzkeng": bot_instance.dotzkeng_command,
                "stopdotzkeng": bot_instance.stop_dotzkeng_command,
                "flowernc": bot_instance.flower_nc_command,
                "ncemo": bot_instance.nc_emo_command,
                "reply": bot_instance.reply_command,
                "stopreply": bot_instance.stop_reply_command,
                "gc": bot_instance.gc_command,
                "sudo": bot_instance.sudo_command,
                "refresh": bot_instance.refresh_command,
            }
            
            if command in cmd_map:
                await cmd_map[command](update, context)
            elif command == "flowernc":
                await bot_instance.flower_nc_command(update, context)

    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), prefix_handler))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, bot_instance.message_collector))

    return application


async def run_bot(token, bot_number, owner_id):
    max_retries = 30
    retry_delay = 15

    for attempt in range(max_retries):
        application = Application.builder().token(token).build()
        bot_instance = BotInstance(bot_number, owner_id)

        # Standard command handlers
        application.add_handler(CommandHandler("start", bot_instance.start))
        application.add_handler(CommandHandler("nc", bot_instance.nc_command))
        application.add_handler(CommandHandler("ncemo", bot_instance.nc_emo_command))
        application.add_handler(CommandHandler("ncmoon", bot_instance.ncmoon_command))
        application.add_handler(CommandHandler("ncflag", bot_instance.ncflag_command))
        application.add_handler(CommandHandler("nccurly", bot_instance.nccurly_command))
        application.add_handler(CommandHandler("stopnc", bot_instance.stop_nc_command))
        application.add_handler(CommandHandler("stopncmoon", bot_instance.stop_ncmoon_command))
        application.add_handler(CommandHandler("stopncflag", bot_instance.stop_ncflag_command))
        application.add_handler(CommandHandler("stopnccurly", bot_instance.stop_nccurly_command))
        application.add_handler(CommandHandler("dotzkeng", bot_instance.dotzkeng_command))
        application.add_handler(CommandHandler("stopdotzkeng", bot_instance.stop_dotzkeng_command))
        application.add_handler(CommandHandler("flowernc", bot_instance.flower_nc_command))
        application.add_handler(CommandHandler("spam", bot_instance.spam_command))
        application.add_handler(CommandHandler("stopspam", bot_instance.stop_spam_command))
        application.add_handler(CommandHandler("target", bot_instance.target_command))
        application.add_handler(CommandHandler("reply", bot_instance.reply_command))
        application.add_handler(CommandHandler("stopreply", bot_instance.stop_reply_command))
        application.add_handler(CommandHandler("delay", bot_instance.delay_command))
        application.add_handler(CommandHandler("threads", bot_instance.threads_command))
        application.add_handler(CommandHandler("stopall", bot_instance.stop_all_command))
        application.add_handler(CommandHandler("gc", bot_instance.gc_command))
        application.add_handler(CommandHandler("setgc", bot_instance.set_gc_command))
        application.add_handler(CommandHandler("ping", bot_instance.ping_command))
        application.add_handler(CommandHandler("sudo", bot_instance.sudo_command))
        application.add_handler(CommandHandler("refresh", bot_instance.refresh_command))

        # Custom handler for prefix '-'
        async def prefix_handler(update, context):
            if not update.message or not update.message.text:
                return
            text = update.message.text
            if text.startswith('-'):
                parts = text[1:].split()
                if not parts:
                    return
                command = parts[0].lower()
                context.args = parts[1:]
                
                cmd_map = {
                    "start": bot_instance.start,
                    "nc": bot_instance.nc_command,
                    "stopnc": bot_instance.stop_nc_command,
                    "spam": bot_instance.spam_command,
                    "stopspam": bot_instance.stop_spam_command,
                    "delay": bot_instance.delay_command,
                    "threads": bot_instance.threads_command,
                    "target": bot_instance.target_command,
                    "stopall": bot_instance.stop_all_command,
                    "ncmoon": bot_instance.ncmoon_command,
                    "stopncmoon": bot_instance.stop_ncmoon_command,
                    "ncflag": bot_instance.ncflag_command,
                    "stopncflag": bot_instance.stop_ncflag_command,
                    "nccurly": bot_instance.nccurly_command,
                    "stopnccurly": bot_instance.stop_nccurly_command,
                    "dotzkeng": bot_instance.dotzkeng_command,
                    "stopdotzkeng": bot_instance.stop_dotzkeng_command,
                    "flowernc": bot_instance.flower_nc_command,
                    "ncemo": bot_instance.nc_emo_command,
                    "reply": bot_instance.reply_command,
                    "stopreply": bot_instance.stop_reply_command,
                    "ping": bot_instance.ping_command,
                    "gc": bot_instance.gc_command,
                    "setgc": bot_instance.set_gc_command,
                    "sudo": bot_instance.sudo_command,
                    "refresh": bot_instance.refresh_command,
                }
                
                if command in cmd_map:
                    await cmd_map[command](update, context)
            else:
                await bot_instance.message_collector(update, context)

        application.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), prefix_handler))

        try:
            await application.initialize()
            await application.start()
            if application.updater:
                # Removed large stagger per user request for 1s startup
                await asyncio.sleep(0.1)
                await application.updater.start_polling(drop_pending_updates=True)
            print(f"Bot {bot_number} started successfully!")

            while True:
                await asyncio.sleep(3600)

        except Exception as e:
            error_str = str(e).lower()
            if "conflict" in error_str:
                print(f"Bot {bot_number} conflict (attempt {attempt + 1}/{max_retries}), retrying in {retry_delay}s...")
                try:
                    if application.updater:
                        await application.updater.stop()
                    await application.stop()
                    await application.shutdown()
                except Exception:
                    pass
                await asyncio.sleep(retry_delay)
                # More aggressive exponential backoff for conflicts
                retry_delay = min(retry_delay + 15, 300)
                continue
            else:
                print(f"Bot {bot_number} error: {e}")
                break
        finally:
            try:
                if application.updater:
                    await application.updater.stop()
                await application.stop()
                await application.shutdown()
            except Exception:
                pass
        break
    else:
        print(f"Bot {bot_number} failed after {max_retries} attempts - token may be used elsewhere")

async def main():
    print(f"Starting {len(BOT_TOKENS)} bots for owner ID: {OWNER_ID}")
    print("All actions (name change, spam, reply) run in LOOPS!")

    tasks = []
    for i, token in enumerate(BOT_TOKENS, 1):
        task = asyncio.create_task(run_bot(token, i, OWNER_ID))
        tasks.append(task)
        # Stagger slightly to allow some breathing room but fast enough for 1s total
        await asyncio.sleep(0.05)

    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\nShutting down all bots...")


if __name__ == "__main__":
    asyncio.run(main())