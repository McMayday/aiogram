from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()
# '914674179'
ALLOWED_USERS = []
ADMINS = [914674179, ]
DATABASE = 'windr14'
PGUSER ='postgres'
PGPASSWORD = 1
BOT_TOKEN = '1506550581:AAEJ36pTQZlyCPAqz4OkwsARdwOKug-XSYA'  # Забираем значение типа str
IP = 'localhost'  # Тоже str, но для айпи адреса хоста

aiogram_redis = {
    'host': IP,
}

redis = {
    'address': (IP, 6379),
    'encoding': 'utf8'
}
