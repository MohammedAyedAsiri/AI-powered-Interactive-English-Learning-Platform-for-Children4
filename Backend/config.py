import os
class Config:
    # Configuration for MySQL Database
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ' '
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'language_app'  