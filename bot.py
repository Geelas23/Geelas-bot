    from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os, random

TOKEN = os.getenv("TOKEN")

antrian = []
pasangan = {}
gender = {} # simpan gender user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Selamat datang di Bot Cari Kenalan\n\n"
        "Perintah:\n"
        "/cari - Cari teman random\n"
        "/cewe - Cari teman cewe\n"
        "/cowo - Cari teman cowo\n"
        "/next - Ganti pasangan\n"
        "/stop - Berhenti ngobrol"
    )

async def set_gender(update: Update, context: ContextTypes.DEFAULT_TYPE, g):
    user_id = update.message.from_user.id
    gender[user_id] = g
    await update.message.reply_text(f"Gender kamu diset ke {g}. Sekarang ketik /cari")

async def cewe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_gender(update, context, "cewe")

async def cowo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_gender(update, context, "cowo")

async def cari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in pasangan:
        await update.message.reply_text("Kamu udah ada pasangan. Ketik /next atau /stop")
        return

    # cari di antrian
    for i, partner_id in enumerate(antrian):
        # kalau pake filter gender
        if context.args:
            target = context.args[0]
            if gender.get(partner_id)!= target: continue

        partner_id = antrian.pop(i)
        pasangan[user_id] = partner_id
        pasangan[partner_id] = user_id
        await context.bot.send_message(partner_id, "Dapet pasangan! Silakan ngobrol 😊")
        await update.message.reply_text("Dapet pasangan! Silakan ngobrol 😊")
        return

    antrian.append(user_id)
    await update.message.reply_text("Mencari teman... mohon tunggu")

async def next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await stop(update, context)
    await cari(update, context)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in pasangan:
        partner_id = pasangan[user_id]
        del pasangan[user_id]
        del pasangan[partner_id]
        await context.bot.send_message(partner_id, "Pasangan kamu udah keluar.")
        await update.message.reply_text("Kamu udah keluar dari obrolan.")
    elif user_id in antrian:
        antrian.remove(user_id)
        await update.message.reply_text("Keluar dari antrian.")
    else:
        await update.message.reply_text("Kamu gak lagi ngobrol.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in pasangan:
        partner_id = pasangan[user_id]
        await context.bot.send_message(partner_id, update.message.text)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cari", cari))
    app.add_handler(CommandHandler("cewe", cewe))
    app.add_handler(CommandHandler("cowo", cowo))
    app.add_handler(CommandHandler("next", next))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot jalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
