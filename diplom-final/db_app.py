import psycopg2


class Postgres:

    def __init__(self, dbname, user, password, host='localhost'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host

    def connect_params(self):
        return f'dbname={self.dbname} user={self.user} password={self.password}'

    def create_db(self):  # создает таблицы
        with psycopg2.connect(self.connect_params()) as conn:
            with conn.cursor() as cur:
                cur.execute('create table IF NOT EXISTS result (id serial primary key, user_id integer, data jsonb);')

                cur.execute(
                    'create table IF NOT EXISTS user_info (id serial primary key, user_id integer, vk_offset integer);')

    def insert_user(self, user_id, offset):
        with psycopg2.connect(self.connect_params()) as conn:
            with conn.cursor() as cur:
                cur.execute("""insert into user_info (user_id, vk_offset) values (%s, %s) returning id""",
                            (user_id, offset))
                return cur.fetchall()

    def result(self, user_id, data):
        with psycopg2.connect(self.connect_params()) as conn:
            with conn.cursor() as cur:
                cur.execute("""insert into result (user_id, data) values (%s, %s) returning id""", (user_id, data,))
                return cur.fetchall()

    def get_offset(self, user_id):
        with psycopg2.connect(self.connect_params()) as conn:
            with conn.cursor() as cur:
                cur.execute("""select vk_offset from user_info where user_id=(%s)""", (user_id,))
                return cur.fetchall()

    def update_offset(self, offset):
        with psycopg2.connect(self.connect_params()) as conn:
            with conn.cursor() as cur:
                cur.execute("""update user_info set vk_offset=(%s) returning id""", (offset,))
                return cur.fetchall()

    def user_info(self, user_id, offset):
        with psycopg2.connect(self.connect_params()) as conn:
            with conn.cursor() as cur:
                cur.execute("""insert into user_info (user_id, vk_offset) values (%s, %s) returning id""",
                            (user_id, offset))
                return cur.fetchall()
