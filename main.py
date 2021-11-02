import subprocess
import os
import conf
from git import Repo
import json
from telegram.base import TO
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

FEEDS_FILE = 'feed.json'

def begin(update,context):
    update.message.reply_text("""
    Bienvenue sur Fenrirbot 

    Commandes disponible :

    - /link pour renseigner le lien de l'article
    - /help pour avoir les commandes

    """)

def help(update,context):
    update.message.reply_text("""

        - /link + lien de l'article
        - /help pour avoir l'ensemble des commandes

    """)

def error_message(update,context):
    update.message.reply_text("Erreur de commande ")

   
def link(update,context): 
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    links = []

    if os.path.isfile(FEEDS_FILE):
        with open(FEEDS_FILE) as f:
            try:
                links = json.load(f)
            except Exception as e:
                print(e)
    if update.message.text[6:] not in links:
        links.append(update.message.text[6:])
    with open(FEEDS_FILE, "w+") as f:
        json.dump(links, f)

    # Git Update
    py2output = subprocess.check_output(['git', 'add' , 'feed.json'])
    try:
        output = subprocess.check_output(['git', 'commit' ,'-m' , 'update'], stderr=subprocess.STDOUT)
    except Exception as exc:
        print(exc)
        print("Status : FAIL", exc.returncode, exc.output)
    py2output = subprocess.check_output(['/home/fenrir/NewsFeed_Telegram_Bot/git.sh', 'push'])                    

def main():
    updater = Updater(conf.Token, use_context = True)
    dp = updater.dispatcher #Update the chat into telegram and send the text to handler
    dp.add_handler(CommandHandler("begin", begin)) #Add begin command  into the bot 
    dp.add_handler(CommandHandler("link", link))  #Add link command  into the bot 
    dp.add_handler(CommandHandler("help", help))  #Add help command  into the bot 
    dp.add_handler(MessageHandler(Filters.text, error_message)) #check the bad commands and send an erro_message
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()










