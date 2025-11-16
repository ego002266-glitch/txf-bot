import requests
import pandas as pd
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
import asyncio

TOKEN = "8345537306:AAFdQUPIxh5bUaAOoGjAhpwRYwDKiYxAy4g"

# 簡單價格警報字典
alerts = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "TXFAlertBot 上線囉！\n"
        "使用指令：\n"
        "/txf - 查詢台指期現價\n"
        "/alert <價格> - 設定價格警報"
    )

async def get_txf_price():
    # 日期格式 YYYYMMDD
    import datetime
    today = datetime.datetime.now().strftime("%Y%m%d")
    url = f"https://www.taifex.com.tw/cht/3/futDataDown?down_type=1&commodity_id=TXF&queryDate={today}"
    try:
        res = requests.get(url)
        df = pd.read_csv(pd.compat.StringIO(res.text))
        # 取得最後成交價 (示範抓第一列)
        price = df.iloc[0]['最後成交價']
        return float(price.replace(',', ''))
    except Exception as e:
        print("抓取錯誤:", e)
        return None

async def txf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = await get_txf_price()
    if price:
        await update.message.reply_text(f"TXF 現價：{price}")
        # 檢查警報
        chat_id = update.message.chat_id
        if chat_id in alerts:
            alert_price = alerts[chat_id]
            if price >= alert_price:
                await update.message.reply_text(f"⚠️ TXF 達到警報價 {alert_price}！現價 {price}")
                del alerts[chat_id]
    else:
        await update.message.reply_text("抓取行情失敗，請稍後再試。")

async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    try:
        price = float(context.args[0])
        alerts[chat_id] = price
        await update.message.reply_text(f"已設定價格警報：{price}")
    except:
        await update.message.reply_text("用法錯誤：/alert <價格>")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("txf", txf))
    app.add_handler(CommandHandler("alert", alert))

    app.run_polling()


