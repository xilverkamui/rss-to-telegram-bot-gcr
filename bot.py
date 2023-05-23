import os
import pymysql
import feedparser
import telegram
from telegram import ParseMode
from dotenv import load_dotenv

load_dotenv()

# Retrieve environment variables
bot_token = os.getenv("BOT_TOKEN")
chat_ids = os.getenv("CHAT_IDS").split(",")
rss_urls = os.getenv("RSS_URLS").split(",")
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect to the database
db = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name)
cursor = db.cursor()

# Get previous feed items from the database
prev_items = []
get_prev_items_query = "SELECT published_time, title FROM feed_items"
cursor.execute(get_prev_items_query)
prev_items_results = cursor.fetchall()
for row in prev_items_results:
    prev_items.append((row[0], row[1]))

# Initialize the Telegram bot
bot = telegram.Bot(token=bot_token)


def post_to_telegram(chat_id, message):
    bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML, disable_web_page_preview=False)


def save_feed_item(new_items):
    insert_item_query = 
    cursor.executemany('INSERT INTO feed_items (published_time, title) VALUES (%s, %s)',new_items)
    db.commit()


# Process each RSS feed URL
new_items = []
for rss_url in rss_urls:
    feed = feedparser.parse(rss_url)
    for entry in feed.entries:
        published_time = entry.published_parsed
        title = entry.title

        # Check if the feed item is new
        if (published_time, title) not in prev_items:
            # Post to Telegram
            message = f"<b>{title}</b>\n\n{entry.description}\n\n{entry.link}"
            for chat_id in chat_ids:
                post_to_telegram(chat_id, message)
			
			new_items.append(published_time, title)
			
# Save the new feed item
save_feed_item(new_items)

# Close the database connection
db.close()
