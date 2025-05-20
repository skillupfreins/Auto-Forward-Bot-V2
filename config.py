from os import environ 

class Config:
    API_ID = environ.get("API_ID", "8d0fe8b5ae8149455681681253b2ef17")
    API_HASH = environ.get("API_HASH", "21601817")
    BOT_TOKEN = environ.get("BOT_TOKEN", "70955...") 
    BOT_SESSION = environ.get("BOT_SESSION", "bot") 
    DATABASE_URI = environ.get("DATABASE", "mongodb+srv://chhjgjkkjhkjhkjh@cluster0.xowzpr4.mongodb.net/")
    DATABASE_NAME = environ.get("DATABASE_NAME", "forward-bot")
    BOT_OWNER_ID = [int(id) for id in environ.get("BOT_OWNER_ID", '6764661699').split()]

class temp(object): 
    lock = {}
    CANCEL = {}
    forwardings = 0
    BANNED_USERS = []
    IS_FRWD_CHAT = []
    
