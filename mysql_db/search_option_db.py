from mysql_db.connect_to_db import my_db, cursor


def option_create_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS  search_option
    (
        cars  BOOL DEFAULT FALSE,
        truck_cars BOOL DEFAULT FALSE,
        price_min  INT,
        price_max  INT,
        tracking_time DATETIME,
        update_period_min INT,
        user_id INT  PRIMARY KEY NOT NULL
        )'''
                   )
    my_db.commit()


async def option_insert_table(state):
    async with state.proxy() as data:
        sql = ''' INSERT INTO search_option
        (cars, truck_cars, price_min, price_max, tracking_time, update_period_min, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE cars = VALUES(cars), truck_cars = VALUES(truck_cars),
        price_min = VALUES(price_min), price_max = VALUES(price_max), 
        tracking_time = VALUES(tracking_time), update_period_min = VALUES(update_period_min)'''

        cursor.execute(sql, (data["cars"], data["truck_cars"], data["price_min"], data["price_max"],
                             data["tracking_time"], data["update_period_min"], data["user_id"],))

        my_db.commit()


def option_update_table(time, user_id):
    sql = f'''UPDATE search_option
            SET tracking_time = %s
            WHERE user_id = %s'''
    cursor.execute(sql, (time, user_id,))
    my_db.commit()


def option_select_table(user_id):
    sql = (f'''SELECT * 
              FROM search_option
              WHERE  user_id = %s''')

    cursor.execute(sql, (user_id,))
    res = cursor.fetchall()
    return res

