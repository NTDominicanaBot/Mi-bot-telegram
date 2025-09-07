from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes,
    ChatMemberHandler, MessageHandler, filters
)
import json, os

TOKEN = os.getenv("TOKEN", "7516787034:AAFbPPgYUbCrBL_1Zv2mWFhX2_QnK6zWsT8")
DB_FILE = "bot_data.json"

# ---------- UTILS ----------
def load_data():
    try:
        with open(DB_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"welcome_msg": "👋 ¡Bienvenido al grupo!", "buttons": []}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------- START / PANEL ----------
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("📢 Ver bienvenida", callback_data="show_welcome")],
        [InlineKeyboardButton("➕ Agregar botón", callback_data="add_btn")],
        [InlineKeyboardButton("🗑️ Borrar botones", callback_data="del_btn")]
    ]
    await update.message.reply_text(
        f"Hola {user.first_name}, usa los botones:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------- SHOW WELCOME ----------
async def show_welcome(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = load_data()
    keyboard = [[InlineKeyboardButton(btn["text"], url=btn.get("url"))] for btn in data["buttons"]]
    await query.message.reply_text(data["welcome_msg"], reply_markup=InlineKeyboardMarkup(keyboard))

# ---------- ADD BUTTON ----------
async def add_btn(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "Envíame el nuevo botón en este formato:\n"
        "texto | url\n"
        "Ejemplo: 📢 Canal | https://t.me/micanal"
    )
    ctx.user_data["expect"] = "new_button"

# ---------- CAPTURE NEW BUTTON ----------
async def capture(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if ctx.user_data.get("expect") != "new_button":
        return
    try:
        text, url = update.message.text.split(" | ", 1)
    except ValueError:
        await update.message.reply_text("❌ Formato inválido. Usa: texto | url")
        return
    data = load_data()
    data["buttons"].append({"text": text.strip(), "url": url.strip()})
    save_data(data)
    await update.message.reply_text("✅ Botón guardado.")
    ctx.user_data.clear()

# ---------- DELETE BUTTONS ----------
async def del_btn(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = load_data()
    data["buttons"] = []
    save_data(data)
    await query.message.reply_text("🗑️ Todos los botones borrados.")

# ---------- MAIN ----------
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_welcome, pattern="^show_welcome$"))
    app.add_handler(CallbackQueryHandler(add_btn,      pattern="^add_btn$"))
    app.add_handler(CallbackQueryHandler(del_btn,      pattern="^del_btn$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, capture))
    print("Bot PLUS iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()
