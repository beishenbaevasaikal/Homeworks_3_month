INSERT_USER = '''
INSERT OR IGNORE INTO telegramm_users VALUES (?, ?, ?)
'''
CREATE_PROFILE_TABLE_QUERY = '''
CREATE TABLE IF NOT EXISTS profiles
(
ID INTEGER PRIMARY KEY,
TELEGRAM_ID INTEGER,
NICKNAME CHAR(50),
BIO CHAR(50),
PHOTO TEXT,
BIRTHDAY DATA,
GENDER TEXT,
UNIQUE (TELEGRAM_ID)
)
'''

