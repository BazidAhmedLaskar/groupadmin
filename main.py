import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ChatJoinRequestHandler,
    MessageHandler,
    filters,
)

BOT_TOKEN = "7277335379:AAGz9nULd4lcZ_egjNOvLplhnZWm4GAw4uA"  # 🛑 Keep private!

promotion_responses = [
    "💔 Team Tasmina says: No promotions here... Respect the vibe, not the spam 😢",
    "🛑 Bro, we trying to keep it clean! No links allowed – Team Tasmina is watching 👀",
    "😤 Whoa! Promotion is not allowed in Team Tasmina's zone. Keep it real or keep it out.",
    "🚫 Links = No Love 😢 Keep this space pure – Team Tasmina style 💫",
    "🤐 Chill! Don’t spam the chat. Team Tasmina wants a peaceful world 🌍"
]

join_welcome_responses = [
    "🎉 Welcome {first_name}! You're officially part of Team Tasmina now 💖 No promotions, just emotions!",
    "🌟 Hi {first_name}, welcome to the drama-free zone! Team Tasmina says behave 🤞",
    "❤️ {first_name}, you've joined a loyal squad – Team Tasmina. Be kind, no spam, only vibes.",
    "🔥 Yo {first_name}, you made it to the gang! Team Tasmina appreciates real ones 🫶"
]

async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    await update.chat_join_request.approve()
    welcome = random.choice(join_welcome_responses).format(first_name=user.first_name or "Friend")
    await context.bot.send_message(chat_id=update.chat_join_request.chat.id, text=welcome)

async def block_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    if any(bad in text.lower() for bad in ["http", "https", "t.me", "@", ".com", "joinchat"]):
        try:
            await update.message.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")
        warn = random.choice(promotion_responses)
        await context.bot.send_message(chat_id=update.message.chat.id, text=warn)

async def main():
    print("🤖 Team Tasmina Bot is starting...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, block_links))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
