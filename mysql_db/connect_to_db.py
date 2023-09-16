import mysql.connector as mc

from create_bot import db_host, db_port, db_user, db_database, db_password

my_db = mc.connect(
    host=db_host,
    port=db_port,
    user=db_user,
    password=db_password,
    database=db_database
)

cursor = my_db.cursor(buffered=True)


def check_connect():
    if my_db:
        print('Data base connected OK!')


