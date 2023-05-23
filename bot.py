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

# Initialize the Telegram bot
bot = telegram.Bot(token=bot_token)

# Get previous feed items from the database
prev_items = []
get_prev_items_query = "SELECT published_time, title FROM feed_items"
cursor.execute(get_prev_items_query)
prev_items_results = cursor.fetchall()
for row in prev_items_results:
    prev_items.append((row[0], row[1]))

# Send message to Telegram
def post_to_telegram(chat_id, message):
    try:
	    bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML, disable_web_page_preview=False)
    except TelegramError as e:
        print(f"Failed to send message to chat ID {chat_id}: {str(e)}")              

# Store the new feed items in the database
def store_new_items(new_items):
    query = "INSERT INTO feed_items (published_time, title) VALUES (%s, %s)"
    cursor.executemany(query, new_items)
    db.commit()

# Delete old feed items from the database
def delete_old_items():
    cutoff_date = datetime.now() - timedelta(days=7)
    query = "DELETE FROM feed_items WHERE published_time < %s"
    cursor.execute(query, cutoff_date.strftime('%Y-%m-%d'))
    db.commit()

# Delete old feed items on Saturday before 2 AM
if datetime.now().weekday() == 5 and datetime.now().hour < 2:
    delete_old_items()
	
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
			
			# Send the message to Telegram
            for chat_id in chat_ids:
			    post_to_telegram(chat_id, message)
		
		    # Add the new item to the list
	        new_items.append(published_time, title)
			
# Save the new feed item
store_new_items(new_items)

# Close the database connection
db.close()
