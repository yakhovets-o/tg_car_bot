import sqlite3 as sq

#  функция регистрация  базы данных
def db_start():
    global base, cur

    base = sq.connect('search_option.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')

    base.execute('CREATE TABLE IF NOT EXISTS url('
                 'cars TEXT, '
                 'price_min INTEGER, '
                 'price_max INTEGER,'
                 'publ INTEGER, '
                 'id INTEGER )')
    base.commit()

#  функция добавления в  базу данных
async def db_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO url VALUES(?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()

#  функция удаления из базы данных
async def db_del_user(id):
    cur.execute('DELETE FROM url WHERE id == ?', (id,))
    base.commit()
