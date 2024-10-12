from dotenv import load_dotenv
import os

load_dotenv()

class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = os.getenv('DB_PASS')
    MYSQL_DB = 'felicitaciones'


config = {
    'development': DevelopmentConfig
}