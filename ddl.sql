CREATE TABLE IF NOT EXISTS feed_items (
        published_time DATETIME,
        title VARCHAR(255),
        PRIMARY KEY (published_time, title)
