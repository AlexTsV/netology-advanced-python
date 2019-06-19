import psycopg2


class Postgres:
    connect_params = "dbname=postgres user=postgres password=123"

    def create_db(self):  # создает таблицы
        with psycopg2.connect(Postgres.connect_params) as conn:
            with conn.cursor() as cur:
                cur.execute('create table IF NOT EXISTS students ('
                            'id SERIAL PRIMARY KEY,'
                            'name CHARACTER VARYING(30),'
                            'gpa numeric(10,2),'
                            'birth timestamp with time zone);')

                cur.execute('create table IF NOT EXISTS courses ('
                            'id SERIAL PRIMARY KEY,'
                            'name CHARACTER VARYING(30));')

                cur.execute('create table IF NOT EXISTS student_course ('
                            'id serial PRIMARY KEY,'
                            'student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,'
                            'course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE);')

                cur.execute('CREATE UNIQUE INDEX i_students ON students USING btree(name, birth);')

    def add_course(self, name_course):
        with psycopg2.connect(Postgres.connect_params) as conn:
            with conn.cursor() as curs:
                curs.execute("""select name from courses where name = %s""", (name_course,))
                courses = curs.fetchone()
                if courses is None:
                    curs.execute("""insert into courses (name) values (%s) returning name""", (name_course,))
                else:
                    if name_course in courses:
                        curs.execute('rollback;')

    def get_students(self, course_id):  # возвращает студентов определенного курса
        with psycopg2.connect(Postgres.connect_params) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """select students.name from students join student_course on students.id = student_course.student_id
                    where course_id = %s""", (course_id,))
                res = curs.fetchall()
                return res

    def add_students(self, course_id, students):  # создает студентов и записывает их на курс
        with psycopg2.connect(Postgres.connect_params) as conn:
            with conn.cursor() as curs:
                curs.execute("""select id from courses where id = %s""", (course_id,))
                if curs.fetchone() is None:
                    return None
                for item in students:
                    curs.execute(self.insert_student(), (item['name'], item['birth'], item['gpa']))
                    curs.execute("""select id from students where name = (%s)""", (item['name'],))
                    student_id = curs.fetchone()[0]
                    curs.execute("""insert into student_course (course_id, student_id) values (%s, %s)""",
                                 (course_id, student_id))
                    curs.execute("""select name from courses where id=(%s)""", (course_id,))

    def insert_student(self):
        query = """insert into students (name, birth, gpa) values (%s, %s, %s) returning id"""
        return query

    def add_student(self, student):  # просто создает студента
        with psycopg2.connect(Postgres.connect_params) as conn:
            with conn.cursor() as curs:
                curs.execute(self.insert_student(), (student['name'], student['birth'], student['gpa']))

    def get_student(self, student_id):
        with psycopg2.connect(Postgres.connect_params) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """select students.name from students join student_course on students.id = student_course.student_id
                    where student_id=(%s)""", (student_id,))
                res = curs.fetchone()
                if not res:
                    return f'Студент с id="{student_id}" не записан на курсы'
                else:
                    return res[0]


study = Postgres()
# study.create_db()
# print(study.add_course('Marketing'))
print(study.add_students(1, [{'name': 'n Ivv', 'birth': '1990-11-11', 'gpa': 4.5},
                             {'name': 'yayyy Vasin', 'birth': '1990-10-10', 'gpa': 3.5}]))
# print(study.get_student(4))
# print(study.add_student({'name': 'Ivaa Ivanov', 'birth': '1990-12-12', 'gpa': 4.0}))
# print(study.get_students(1))
# print(study.add_student_without_conn({'name': 'Ivaa Ivanov', 'birth': '1990-12-12', 'gpa': 4.0}))
# print(study.get_student(1))
