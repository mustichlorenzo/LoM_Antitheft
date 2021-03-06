from telegram.ext import Updater, CommandHandler

TOKEN_ONOFF = "YOUR_TOKEN" 

telegram_act = None

#Start the bot
def start(update, context):
    update.message.reply_text("/attiva: attiva l\'antifurto\n/disattiva: disattiva l\'antifurto\n/help: visualizza i comandi")

#Print available commands
def help_command(update, context):
    update.message.reply_text("/attiva: attiva l\'antifurto\n/disattiva: disattiva l\'antifurto\n/help: visualizza i comandi")

#Turn on the system
def attiva(update, context):
    global telegram_act 

    update.message.reply_text("Antifurto attivato!")
    telegram_act = True

#Turn off the system    
def disattiva(update, context):
    global telegram_act

    update.message.reply_text("Antifurto disattivato!")
    telegram_act = False

def update_bot():
    updater = Updater(TOKEN_ONOFF, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CommandHandler('attiva', attiva))
    updater.dispatcher.add_handler(CommandHandler('disattiva', disattiva))

    updater.start_polling()
