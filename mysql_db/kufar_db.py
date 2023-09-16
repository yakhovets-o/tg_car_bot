from mysql_db.connect_to_db import my_db, cursor


def kuf_create_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS  kufar
    (
        user_id INT ,
        brand VARCHAR(20),
        model VARCHAR(20),
        year_production VARCHAR(40),
        engine_type VARCHAR(40),
        engine_volume VARCHAR(40),
        region VARCHAR(40),
        city VARCHAR(40),
        price_usd INT DEFAULT 0,
        price_byn INT DEFAULT 0,
        link VARCHAR(255) PRIMARY KEY,
        date_time_post DATETIME,
        date_time_now DATETIME DEFAULT CURRENT_TIMESTAMP
        )'''
                   )
    my_db.commit()


def kuf_insert_table(attributes):
    sql = ''' INSERT INTO kufar
    (user_id, brand, model, year_production, engine_type, engine_volume, region, city, price_usd, price_byn, link, date_time_post)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    cursor.execute(sql, attributes)

    my_db.commit()


def kuf_select_table(user_id):
    sql = ('''SELECT * 
              FROM kufar
              WHERE  user_id = %s''')

    cursor.execute(sql, (user_id,))
    res = cursor.fetchall()
    return res


def kuf_del_table(user_id):
    sql = f'''DELETE FROM kufar
            WHERE user_id = %s'''

    cursor.execute(sql, (user_id,))
    my_db.commit()
