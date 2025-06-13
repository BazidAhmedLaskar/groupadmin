import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ChatJoinRequestHandler,
    MessageHandler,
    filters
)

BOT_TOKEN = "7277335379:AAGz9nULd4lcZ_egjNOvLplhnZWm4GAw4uA"  # Replace with your bot token

# 🔥 Team Tasmina Emotional Warnings
promotion_responses = [
    "💔 Team Tasmina says: No promotions here... Respect the vibe, not the spam 😢",
    "🛑 Bro, we trying to keep it clean! No links allowed – Team Tasmina is watching 👀",
    "😤 Whoa! Promotion is not allowed in Team Tasmina's zone. Keep it real or keep it out.",
    "🚫 Links = No Love 😢 Keep this space pure – Team Tasmina style 💫",
    "🤐 Chill! Don’t spam the chat. Team Tasmina wants a peaceful world 🌍"
]

# 🎉 Emotional Welcome by Team Tasmina
join_welcome_responses = [
    "🎉 Welcome {first_name}! You're officially part of Team Tasmina now 💖 No promotions, just emotions!",
    "🌟 Hi {first_name}, welcome to the drama-free zone! Team Tasmina says behave 🤞",
    "❤️ {first_name}, you've joined a loyal squad – Team Tasmina. Be kind, no spam, only vibes.",
    "🔥 Yo {first_name}, you made it to the gang! Team Tasmina appreciates real ones 🫶"
]

# 🔓 Auto-Approve Join Requests
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    join_request = update.chat_join_request
    await join_request.approve()
    first_name = join_request.from_user.first_name or "friend"
    welcome_message = random.choice(join_welcome_responses).format(first_name=first_name)
    await context.bot.send_message(chat_id=join_request.chat.id, text=welcome_message)
    print(f"✅ Approved {first_name} to Team Tasmina group.")

# 🧹 Detect and Delete Promo Links
async def block_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text.lower()
        if any(link in text for link in ['http', 't.me', '@']):
            try:
                await update.message.delete()
            except Exception as e:
                print("⚠️ Couldn't delete message:", e)
            warning = random.choice(promotion_responses)
            await context.bot.send_message(chat_id=update.message.chat.id, text=warning)
            print("❌ Deleted promo and warned user - Team Tasmina style.")

# 🧠 Main Bot Logic
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, block_links))

    print("🤖 Team Tasmina Bot is now running...")
    app.run_polling()

if __name__ == "__main__":
    main()
