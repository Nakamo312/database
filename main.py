import sqlite3
db_name = 'quiz.sqlite'
conn = None
cursor = None


def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()


def close():
    cursor.close()
    conn.close()


def do(query):
    cursor.execute(query)
    conn.commit()

def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')


    do('''CREATE TABLE IF NOT EXISTS quiz (
           id INTEGER PRIMARY KEY,
           name VARCHAR)''')


    do('''CREATE TABLE IF NOT EXISTS question (
               id INTEGER PRIMARY KEY,
               question VARCHAR,
               answer VARCHAR,
               wrong1 VARCHAR,
               wrong2 VARCHAR,
               wrong3 VARCHAR)''')


    do('''CREATE TABLE IF NOT EXISTS quiz_content (
               id INTEGER PRIMARY KEY,
               quiz_id INTEGER,
               question_id INTEGER,
               FOREIGN KEY (quiz_id) REFERENCES quiz (id),
               FOREIGN KEY (question_id) REFERENCES question (id) )''')
    close()

def add_questions():
    questions =   [('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
        ('Каким станет зелёный утёс, если упадёт в Красное море?', 'Мокрым', 'Красным', 'Не изменится', 'Фиолетовым'),
        ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
        ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
        ('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
        ('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако')]  
    open()
    cursor.executemany('''INSERT INTO question(question,answer,wrong1,wrong2,wrong3) VALUES (?,?,?,?,?)''',questions)
    conn.commit()
    close()

def add_quiz():
    quizes = [('Своя игра', ),
        ('Кто хочет стать миллионером?', ),
        ('Самый умный', )]
    open()
    cursor.executemany('''INSERT INTO quiz(name) VALUES (?)''',quizes)
    conn.commit()
    close()

def clear_db():
    open()
    querry = "DROP TABLE IF EXISTS quiz_content"
    do(querry)

    querry = "DROP TABLE IF EXISTS quiz"
    do(querry)

    querry = "DROP TABLE IF EXISTS question"
    do(querry)
    close()

def add_links():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    querry = "INSERT INTO quiz_content(quiz_id,question_id) VALUES (?,?)"
    answer = input('Добавить связь?(y/n)') 
    while answer != "n":
        quiz_id = int(input("id викторины"))
        question_id = int(input("id вопроса"))    
        cursor.execute(querry,[quiz_id,question_id])
        conn.commit()
        answer = input('Добавить связь?(y/n)') 
    close()    

def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    add_links()
def get_guestion_after(id_quiz=0,id_quest=1):
    open()
    querry = '''
           SELECT quiz_content.id,question.question, question.answer,question.wrong1,
           question.wrong2, question.wrong3 FROM question,quiz_content
           WHERE quiz_content.question_id == question.id
           AND quiz_content.id > ? AND quiz_content.quiz_id == ?
           ORDER BY quiz_content.id

    '''
    cursor.execute(querry,[id_quest,id_quiz])
    result = cursor.fetchone()
    close()
    return result
