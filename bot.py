from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "8345537306:AAFdQUPIxh5bUaAOoGjAhpwRYwDKiYxAy4g"

async def start(update, context):
    await update.message.reply_text("TXFAlertBot 上線囉！")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()

