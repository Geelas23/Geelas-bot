    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes

    TOKEN = "MASUKIN_TOKEN_BOT_KAMU_DISINI"

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Halo! Bot udah online di Railway 🚀")

    def main():
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.run_polling()

    if __name__ == "__main__":
        main()
