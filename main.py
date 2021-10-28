import subprocess
import os
import conf
from git import Repo
import json
from telegram.base import TO
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


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
    path = 'C:/Users/Ray/Telegram_Bot_Python/test.json' #Don't forget to change the path 
    if os.stat(path).st_size == 0:
        print("Fichier Vide") 
    if os.path.isfile(path):
        websites = None
        with open(path,"r") as file:
             websites = json.load(file)
        with open(path,"w+") as file2:
            websites.append(update.message.text[6:])
            json.dump(websites,file2)
    else:
        websites = []
        websites.append(update.message.text[6:])
        file = open(path, 'w+')
        json.dump(websites,file)
        file.close()
    py2output = subprocess.check_output(['git', 'add' , 'test.json'])
    try:
        output = subprocess.check_output(['git', 'commit' ,'-m' , 'update'], stderr=subprocess.STDOUT, shell=True, timeout=3, universal_newlines=True);     
    except Exception as exc:
        print(exc)                                                                                                 
        print("Status : FAIL", exc.returncode, exc.output)
    py2output = subprocess.check_output(['git', 'push' ])                    

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










