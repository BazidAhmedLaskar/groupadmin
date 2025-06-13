import os
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ChatJoinRequestHandler,
    MessageHandler,
    filters
)
from dotenv import load_dotenv

# Load environment variables from .env file (for local testing)
load_dotenv()

# Securely fetch token
BOT_TOKEN = os.getenv("7277335379:AAGz9nULd4lcZ_egjNOvLplhnZWm4GAw4uA")
if not BOT_TOKEN:
    raise ValueError("Error: BOT_TOKEN environment variable not set.")

# 🚫 Promotion warning replies
promotion_responses = [
    "💔 Team Tasmina says: No promotions here... Respect the vibe, not the spam 😢",
    "🛑 Bro, we trying to keep it clean! No links allowed – Team Tasmina is watching 👀",
    "😤 Whoa! Promotion is not allowed in Team Tasmina's zone. Keep it real or keep it out.",
    "🚫 Links = No Love 😢 Keep this space pure – Team Tasmina style 💫",
    "🤐 Chill! Don’t spam the chat. Team Tasmina wants a peaceful world 🌍"
]

# ✨ Welcome responses
join_welcome_responses = [
    "🎉 Welcome {first_name}! You're officially part of Team Tasmina now 💖 No promotions, just emotions!",
    "🌟 Hi {first_name}, welcome to the drama-free zone! Team Tasmina says behave 🤞",
    "❤️ {first_name}, you've joined a loyal squad – Team Tasmina. Be kind, no spam, only vibes.",
    "🔥 Yo {first_name}, you made it to the gang! Team Tasmina appreciates real ones 🫶"
]

# 🔓 Auto-approve new join requests
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    join_request = update.chat_join_request
    await join_request.approve()
    first_name = join_request.from_user.first_name or "friend"
    welcome_message = random.choice(join_welcome_responses).format(first_name=first_name)
    await context.bot.send_message(chat_id=join_request.chat.id, text=welcome_message)

# 🧹 Detect and remove promotions
async def block_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    if any(word in text.lower() for word in ["http", "https", "t.me", "@", ".com", "joinchat"]):
        try:
            await update.message.delete()
        except Exception as e:
            print(f"⚠️ Couldn't delete message: {e}")
        warning = random.choice(promotion_responses)
        await context.bot.send_message(chat_id=update.message.chat.id, text=warning)

# 🧠 Main logic
async def main():
    print("🚀 Starting Team Tasmina bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, block_links))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
