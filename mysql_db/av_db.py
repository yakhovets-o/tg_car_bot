from mysql_db.connect_to_db import my_db, cursor


def av_create_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS  av
    (
        user_id INT,
        brand VARCHAR(255),
        model VARCHAR(255),
        year VARCHAR(255),
        engine_type VARCHAR(255),
        engine_capacity VARCHAR(255),
        cond VARCHAR(255),
        region VARCHAR(255),
        city VARCHAR(255),
        price_byn INT DEFAULT 0,
        price_usd INT DEFAULT 0,
        link VARCHAR(255) PRIMARY KEY,      
        date_time_post DATETIME,
        date_time_now DATETIME DEFAULT CURRENT_TIMESTAMP
        )'''
                   )
    my_db.commit()


def av_insert_table(attributes):
    sql = ''' INSERT INTO av
    (user_id, brand, model, year, engine_type, engine_capacity, cond, region, city, price_byn, price_usd, link,
    date_time_post)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    cursor.execute(sql, attributes)

    my_db.commit()


def av_select_table(user_id):
    sql = ('''SELECT * 
              FROM av
              WHERE  user_id = %s''')

    cursor.execute(sql, (user_id,))
    res = cursor.fetchall()
    return res


def av_del_table(user_id):
    sql = f'''DELETE FROM av
            WHERE user_id = %s'''

    cursor.execute(sql, (user_id,))
    my_db.commit()
