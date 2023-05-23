import os
import feedparser
import requests
from telegram import Bot

bot_token = os.environ.get('BOT_TOKEN')
chat_ids = os.environ.get('CHAT_IDS').split(',')
rss_urls = os.environ.get('RSS_URLS').split(',')

def post_new_feed_items():
    last_fetched_item_id = os.environ.get('LAST_FETCHED_ITEM_ID')

    for rss_url in rss_urls:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            item_id = entry.get('id')
            if item_id == last_fetched_item_id:
                break
            
            title = entry.get('title')
            description = entry.get('description')
            link = entry.get('link')

            message = f'<b>{title}</b>\n{description}\n{link}'
            for chat_id in chat_ids:
                bot = Bot(token=bot_token)
                bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')

            # Update last fetched item ID
            os.environ['LAST_FETCHED_ITEM_ID'] = item_id

# Run the bot
post_new_feed_items()
