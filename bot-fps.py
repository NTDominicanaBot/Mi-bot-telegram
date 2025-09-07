from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "7516787034:AAFbPPgYUbCrBL_1Zv2mWFhX2_QnK6zWsT8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot de gestión activo.")

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📌 Reglas:\n1. Sé respetuoso.\n2. No spam.\n3. No temas prohibidas.")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat = update.effective_chat
    if not update.message.reply_to_message:
        await update.message.reply_text("Responde al mensaje del usuario a expulsar.")
        return
    victim = update.message.reply_to_message.from_user
    await bot.ban_chat_member(chat.id, victim.id)
    await update.message.reply_text(f"🚫 @{victim.username or victim.first_name} expulsado.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("ban", ban))
    print("Bot iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()
