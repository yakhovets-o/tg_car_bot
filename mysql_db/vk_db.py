from mysql_db.connect_to_db import my_db, cursor


def vk_create_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS  vk
    (
        user_id INT,
        link_post VARCHAR(255) PRIMARY KEY,
        link_user VARCHAR(255),
        body_post MEDIUMTEXT,
        date_time_post DATETIME,
        date_time_now DATETIME DEFAULT CURRENT_TIMESTAMP
        )'''
                   )
    my_db.commit()


def vk_insert_table(attributes):
    sql = ''' INSERT INTO vk
    (user_id, link_post, link_user, body_post, date_time_post)
    VALUES (%s, %s, %s, %s, %s)'''
    cursor.execute(sql, attributes)

    my_db.commit()


def vk_select_table(user_id):
    sql = ('''SELECT * 
              FROM vk
              WHERE  user_id = %s''')

    cursor.execute(sql, (user_id,))
    res = cursor.fetchall()
    return res


def vk_del_table(user_id):
    sql = f'''DELETE FROM vk
    WHERE user_id = %s'''

    cursor.execute(sql, (user_id,))
    my_db.commit()
