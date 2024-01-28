import os
import datetime
from telegram.ext import Updater, MessageHandler, Filters
from telegram import ChatPermissions
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TELEGRAM_BOT_TOKEN')

class WordTracker:
    def __init__(self):
        self.words = ["Опустить", "Завалить сосало", "Выебать", "опустить", "выебать", "трахнуть", "Трахнуть", "Харкнуть", "харкнуть"]
        
        self.counts = {}
        self.user_limits = {474934703: 3}  # Данный айди принадлежит долбоебу канадскому, остальным лимит 8 смс

    def track(self, user_id, message):
        if user_id not in self.counts:
            self.counts[user_id] = {word: 0 for word in self.words}

        for word in self.words:
            self.counts[user_id][word] += message.count(word)

    def check_mute(self, user_id):
        limit = self.user_limits.get(user_id, 5)  # лимит слов долбаеба фраера
        for count in self.counts[user_id].values():
            if count > limit:
                return True
        return False

def handle_message(update, context):
    message = update.message.text
    user_id = update.message.from_user.id

    tracker.track(user_id, message)

    if tracker.check_mute(user_id):
        mute_duration = datetime.datetime.now() + datetime.timedelta(minutes=15)  # минуты мута
        mute_until = int(mute_duration.timestamp())  # конвертация в какой то хуюникс

        context.bot.restrict_chat_member(
            chat_id=update.message.chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=mute_until  # размьют
        )

tracker = WordTracker()

updater = Updater(token=token, use_context=True)

message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
updater.dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()
