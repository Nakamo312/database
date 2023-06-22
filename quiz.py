from main import *
from random import randint
from flask import Flask, session,redirect,url_for

quiz = 1
last_question = 1

def index():
    global quiz,last_guestion
    max_quiz = 3
    session['quiz'] = randint(1,max_quiz)
    session['last_question'] = 0
    return '<a href = "/test"> Перейти к тесту </a>'
def test():
    result = get_guestion_after(session['last_question'],session['quiz'])
    if result is None or len(result) == 0:
        return redirect(url_for('finish'))
    else:
        session['last_question'] = result[0]
        return '<h1>'+ str(session["quiz"]) + '<br>' + str(result) + '</h1>'   


def finish():
    pass


app = Flask(__name__)
app.add_url_rule('/','index',index)
app.add_url_rule('/','test',test)
app.add_url_rule('/','finish',finish)
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'
if __name__ == "__main__":
    app.run()        
