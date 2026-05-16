# mafia_bot_multi.py
import asyncio, json, os, random, time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging

# ---------------------------
# CONFIG
# ---------------------------
TOKENS = [
    "8618313310:AAEhqm0_g5aq5ID79hPtr-dGP2tBcdBgKUM",
    "8948863617:AAEb7Sbo9WTRtOv0M45krX_NfNVff3u1AZc",
    "8006032539:AAFm3BrY4yTRRQpVJX66IgZ4_Zv4wzEqM-I",
    "8414116802:AAFz_SNR6yqdzhm-UZqU3Oaz1srSs0NxuNs",
    "8321061569:AAEEGdBCzWbh-ExBgkOmMymNT9akof9AiwA",
    "8265020706:AAHqecD2CyZvVHrxjsmMLq0qXZajE4q9vAI",
    "8231617858:AAFWee-oX4hIH5-TqeuIgcxJzJeaV1xLqz8",
    "7702151071:AAGit1A1_Za4xawCetZMZhr8gbE0rXTCATI",
    "8200627998:AAEwI6qsOECZVCoDB1wTfF3JUXupIdd8abs",
    "8360762424:AAEeaMBffEwRgNot_vMWYzShdWopAXtOWpc",
]

OWNER_ID = 6343729611
SUDO_FILE = "6343729611"

# ---------------------------
# RAID TEXTS
# ---------------------------
RAID_TEXTS = [
    "DICKHEAD ➿",
    "RND ➿",
    "CHUD ➿",
    "HAKLE ➿",
    "MF ➿",
    "HIJDE ➿",
    "GAWAR ➿",
    "JHATU ➿",
    "GAY ➿",
    "KACHRE WALA ➿",
    "BITCH ➿",
    "ASSHOLE ➿",
    "DICKLESS ➿",
    "COCK SUCKER ➿",
    "TMKC ➿",
    "BAUNA ➿",
    "DICKWEED ➿",
    "MKL ➿",
    "KALUWA ➿",
    "FUCKED ➿",
    "BIHARI ➿",
    "TMKB ➿",
    "BULLY KENDRA ➿",
    "LUN TE VAJ ➿",
]

# ---------------------------
# NCEMO EMOJIS
# ---------------------------
NCEMO_EMOJIS = [
    "😋","😝","😜","🤪","😑","🤫","🤭","🥱","🤗","😡","😠","😤",
    "😮‍💨","🙄","😒","🥶","🥵","🤢","😎","🥸",
    "😹","💫","😼","😽","🙀","😿","😾",
    "🙈","🙉","🙊",
    "⭐","🌟","✨","⚡","💥","💨",
    "💛","💙","💜","🤎","🤍","💘","💝"
]

# ---------------------------
# GLOBAL STATE
# ---------------------------
if os.path.exists(SUDO_FILE):
    try:
        with open(SUDO_FILE, "r") as f:
            _loaded = json.load(f)
            SUDO_USERS = set(int(x) for x in _loaded)
    except Exception:
        SUDO_USERS = {OWNER_ID}
else:
    SUDO_USERS = {OWNER_ID}
with open(SUDO_FILE, "w") as f: json.dump(list(SUDO_USERS), f)

def save_sudo():
    with open(SUDO_FILE, "w") as f: json.dump(list(SUDO_USERS), f)

group_tasks = {}         
slide_targets = set()    
slidespam_targets = set()
swipe_mode = {}
apps, bots = [], []
delay = 1

logging.basicConfig(level=logging.INFO)

# ---------------------------
# DECORATORS
# ---------------------------
def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid not in SUDO_USERS:
            return await update.message.reply_text("bot use krne ki aukat bna pille 🤮👞.")
        return await func(update, context)
    return wrapper

def only_owner(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid != OWNER_ID:
            return await update.message.reply_text("ye sirf tera baap REXXY krr skta hai 😂🔥.")
        return await func(update, context)
    return wrapper

# ---------------------------
# LOOP FUNCTION
# ---------------------------
async def bot_loop(bot, chat_id, base, mode):
    i = 0
    while True:
        try:
            if mode == "raid":
                text = f"{base} {RAID_TEXTS[i % len(RAID_TEXTS)]}"
            else:
                text = f"{base} {NCEMO_EMOJIS[i % len(NCEMO_EMOJIS)]}"
            await bot.set_chat_title(chat_id, text)
            i += 1
            await asyncio.sleep(delay)
        except Exception as e:
            print(f"[WARN] Bot error in chat {chat_id}: {e}")
            await asyncio.sleep(2)

# ---------------------------
# COMMANDS
# ---------------------------
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💗 Welcome to REXXY Bot!\nUse /help to see all commands.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖REXXY Bot Help Menu\n\n"
        "⚡ GC Loops:\n"
        "/gcnc <text>\n/ncemo <text>\n/stopgcnc\n/stopall\n/delay <sec>\n/status\n\n"
        "🎯 Slide & Spam:\n"
        "/targetslide (reply)\n/stopslide (reply)\n/slidespam (reply)\n/stopslidespam (reply)\n\n"
        "⚡ Swipe Mode:\n"
        "/swipe <name>\n/stopswipe\n\n"
        "👑 SUDO Management:\n"
        "/addsudo (reply)\n/delsudo (reply)\n/listsudo\n\n"
        "🛠 Misc:\n/myid\n/ping"
    )

async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    msg = await update.message.reply_text("🏓 Pinging...")
    end_time = time.time()
    latency = int((end_time - start_time) * 1000)
    await msg.edit_text(f"REXXY/ZENO अब्बू  Ki Jay 🤍🌙")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Your ID: {update.effective_user.id}")

# --- GC Loops ---
@only_sudo
async def gcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /gcnc <text>")
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    group_tasks.setdefault(chat_id, {})
    for bot in bots:
        if bot.id not in group_tasks[chat_id]:
            task = asyncio.create_task(bot_loop(bot, chat_id, base, "raid"))
            group_tasks[chat_id][bot.id] = task
    await update.message.reply_text("🔄 Nc Majdury shuru 😈🔥.")

@only_sudo
async def ncemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /ncemo <text>")
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    group_tasks.setdefault(chat_id, {})
    for bot in bots:
        if bot.id not in group_tasks[chat_id]:
            task = asyncio.create_task(bot_loop(bot, chat_id, base, "emoji"))
            group_tasks[chat_id][bot.id] = task
    await update.message.reply_text("🔄 Nc majduri started with Emoji loop.")

@only_sudo
async def stopgcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id].values():
            task.cancel()
        group_tasks[chat_id] = {}
        await update.message.reply_text("⏹ iss GC me rokdia REXXY OP 🎀💞.")

@only_sudo
async def stopall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for chat_id in list(group_tasks.keys()):
        for task in group_tasks[chat_id].values():
            task.cancel()
        group_tasks[chat_id] = {}
    await update.message.reply_text("⏹ rokdia REXXY OP 🎀💞.")

@only_sudo
async def delay_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global delay
    if not context.args: return await update.message.reply_text(f"⏱ Current delay: {delay}s")
    try:
        delay = max(0.5, float(context.args[0]))
        await update.message.reply_text(f"✅ Ok , abb iski maa itne seconds me cudegi {delay}s")
    except: await update.message.reply_text("⚠️ Invalid number.")

@only_sudo
async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📊 Active Loops:\n"
    for chat_id, tasks in group_tasks.items():
        msg += f"Chat {chat_id}: {len(tasks)} bots running\n"
    await update.message.reply_text(msg)

# --- SUDO ---
@only_owner
async def addsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        SUDO_USERS.add(uid); save_sudo()
        await update.message.reply_text(f"✅ {uid} bnadia sudo.")

@only_owner
async def delsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        if uid in SUDO_USERS:
            SUDO_USERS.remove(uid); save_sudo()
            await update.message.reply_text(f"🗑 {uid} nekal madarchod 👍🏿👍🏿👍🏿👍🏿.")

@only_sudo
async def listsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 SUDO USERS:\n" + "\n".join(map(str, SUDO_USERS)))

# --- Slide / Spam / Swipe ---
@only_sudo
async def targetslide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slide_targets.add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("majduri start krdi iss gareeb pe 😂❌🔥.")

@only_sudo
async def stopslide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        slide_targets.discard(uid)
        await update.message.reply_text("majduri rokdi iss gareeb pe 🤢🔥 .")

@only_sudo
async def slidespam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slidespam_targets.add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("Slide se iski maa cudegi 🤣🤣.")

@only_sudo
async def stopslidespam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slidespam_targets.discard(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🛑 Slide spam rokdia.")

@only_sudo
async def swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /swipe <name>")
    swipe_mode[update.message.chat_id] = " ".join(context.args)
    await update.message.reply_text(f"⚡ Swipe se iski maa cudegi 🤪: {swipe_mode[update.message.chat_id]}")

@only_sudo
async def stopswipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    swipe_mode.pop(update.message.chat_id, None)
    await update.message.reply_text("🛑 Swipe mode rokdia.")

# --- Auto Replies ---
async def auto_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, chat_id = update.message.from_user.id, update.message.chat_id
    if uid in slide_targets:
        for text in RAID_TEXTS: await update.message.reply_text(text)
    if uid in slidespam_targets:
        for text in RAID_TEXTS: await update.message.reply_text(text)
    if chat_id in swipe_mode:
        for text in RAID_TEXTS: await update.message.reply_text(f"{swipe_mode[chat_id]} {text}")

# ---------------------------
# BUILD APP & RUN
# ---------------------------
def build_app(token):
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping_cmd))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("gcnc", gcnc))
    app.add_handler(CommandHandler("ncemo", ncemo))
    app.add_handler(CommandHandler("stopgcnc", stopgcnc))
    app.add_handler(CommandHandler("stopall", stopall))
    app.add_handler(CommandHandler("delay", delay_cmd))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("addsudo", addsudo))
    app.add_handler(CommandHandler("delsudo", delsudo))
    app.add_handler(CommandHandler("listsudo", listsudo))
    app.add_handler(CommandHandler("targetslide", targetslide))
    app.add_handler(CommandHandler("stopslide", stopslide))
    app.add_handler(CommandHandler("slidespam", slidespam))
    app.add_handler(CommandHandler("stopslidespam", stopslidespam))
    app.add_handler(CommandHandler("swipe", swipe))
    app.add_handler(CommandHandler("stopswipe", stopswipe))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_replies))
    return app

async def run_all_bots():
    global apps, bots
    for token in TOKENS:
        if token.strip():
            try:
                app = build_app(token)
                apps.append(app); bots.append(app.bot)
            except Exception as e:
                print("Failed building app:", e)

    for app in apps:
        try:
            await app.initialize(); await app.start(); await app.updater.start_polling()
        except Exception as e:
            print("Failed starting app:", e)

    print("🚀 Mafia Bot is running (all bots started).")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_all_bots())
