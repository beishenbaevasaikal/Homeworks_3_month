APPLE_USER = '''CREATE TABLE IF NOT EXISTS telegramm_users(
id INTEGER PRIMARY KEY,
first_name TEXT,
tg_id INTEGER,
UNIQUE(tg_id))'''

INSERT_USER = '''INSERT OR IGNORE INTO telegramm_users VALUES (?, ?, ?, ?, ?)'''

SELECT_USER = '''SELECT * FROM telegramm_users WHERE TG_ID = ?'''

CREATE_PROFILE_TABLE_QUERY = '''
CREATE TABLE IF NOT EXISTS profiles
(
ID INTEGER PRIMARY KEY,
TELEGRAM_ID INTEGER,
NICKNAME CHAR(50),
BIO CHAR(50),
PHOTO TEXT,
BIRTHDAY TEXT,
GENDER TEXT,
UNIQUE (TELEGRAM_ID)
)
'''
INSERT_PROFILE_TABLE_QUERY = '''
INSERT INTO profiles VALUES (?, ?, ?, ?, ?, ?, ?)'''

SELECT_PROFILE_TABLE_QUERY = '''
SELECT * FROM profiles WHERE TELEGRAM_ID = ?'''

SELECT_ALL_PROFILES = '''
SELECT * FROM profiles p
WHERE p.TELEGRAM_ID NOT IN (
        SELECT ld.OWNER_TELEGRAM_ID
        FROM like_dislike ld
        WHERE ld.LIKER_TELEGRAM_ID = ?
        AND ld.LIKE_DISLIKE_STATUS IS NOT NULL
)
AND p.TELEGRAM_ID != ?
'''
CREATE_LIKE_DISLIKE_TABLE_QUERY = '''
CREATE TABLE IF NOT EXISTS like_dislike
(
ID INTEGER PRIMARY KEY,
OWNER_TELEGRAM_ID INTEGER,
LIKER_TELEGRAM_ID INTEGER,
LIKE_DISLIKE_STATUS INTEGER,
UNIQUE (OWNER_TELEGRAM_ID, LIKER_TELEGRAM_ID)
)
'''

INSERT_LIKE_QUERY = '''
INSERT INTO like_dislike VALUES (?, ?, ?, ?)
'''

SELECT_PROFILE_QUERY = '''
SELECT * FROM profiles WHERE TELEGRAM_ID = ?
'''

UPDATE_PROFILE_QUERY = '''
UPDATE profiles SET NICKNAME = ?, BIO = ?, PHOTO = ?, BIRTHDAY = ?, GENDER = ? WHERE TELEGRAM_ID = ?
'''

ALTER_APPLE_USER_V1 = '''
ALTER TABLE telegramm_users ADD COLUMN REFERENCE_LINK TEXT
'''

ALTER_APPLE_USER_V2 = '''
ALTER TABLE telegramm_users ADD COLUMN BALANCE INTEGER
'''

CREATE_TABLE_REFERENCE_QUERY = """
CREATE TABLE IF NOT EXISTS reference
(
ID INTEGER PRIMARY KEY,
OWNER_TELEGRAM_ID INTEGER,
REFERENCE_TELEGRAM_ID INTEGER,
UNIQUE (OWNER_TELEGRAM_ID, REFERENCE_TELEGRAM_ID)
)
"""

INSERT_REFERENCE_USER_QUERY = '''
INSERT INTO reference VALUES (?, ?, ?)
'''

UPDATE_USER_LINK_QUERY = '''
UPDATE telegramm_users SET REFERENCE_LINK = ? WHERE TG_ID = ?
'''

UPDATE_USER_BALANCE_QUERY = '''
UPDATE telegramm_users SET BALANCE = COALESCE(BALANCE, 0) + 100 WHERE TG_ID = ?
'''

SELECT_USEER_BY_LINK_QUERY = '''
SELECT * FROM telegramm_users WHERE REFERENCE_LINK = ?
'''
SELECT_REFERENCES_LIST = '''
SELECT * FROM references
WHERE owner_telegram_id = ?
'''